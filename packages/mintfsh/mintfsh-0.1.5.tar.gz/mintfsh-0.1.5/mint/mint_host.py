from flask import Flask, request, send_file, jsonify
import os
import base64
import hashlib
import time
import threading
import shutil
import argparse
import sys

def base64url_encode(s):
    return base64.urlsafe_b64encode(s.encode()).rstrip(b'=').decode()

def get_available_disk_space(path):
    total, used, free = shutil.disk_usage(path)
    return free

def run_cleaner(upload_dir, auto_delete_time, clean_interval_seconds):
    def cleaner():
        while True:
            now = int(time.time() * 1000)
            for fname in os.listdir(upload_dir):
                parts = fname.split('_')
                if len(parts) < 3:
                    continue
                try:
                    timestamp = int(parts[1])
                    file_hash = parts[2]
                except ValueError:
                    continue
                if len(file_hash) != 64:
                    continue
                if auto_delete_time != -1 and (now - timestamp > auto_delete_time * 1000):
                    try:
                        os.remove(os.path.join(upload_dir, fname))
                        print(f"deleted expired file: {fname}")
                    except Exception as e:
                        print(f"failed to delete expired file {fname}: {e}")
            time.sleep(clean_interval_seconds)

    thread = threading.Thread(target=cleaner, daemon=True)
    thread.start()

def main():
    parser = argparse.ArgumentParser(description='Mint File Host')
    parser.add_argument('port', type=int, nargs='?', default=3000, help='Port to run server on (default: 3000)')
    parser.add_argument('--maxfs', type=int, default=750, help='Max file size in MB (default: 750)')
    parser.add_argument('--autodel', type=int, default=7, help='Auto delete after N days (-1 for never)')
    parser.add_argument('--cleaninterval', type=int, default=5, help='Cleaner run interval in minutes')

    args = parser.parse_args()

    port = args.port
    max_file_size = args.maxfs * 1024 * 1024
    auto_delete_time = -1 if args.autodel == -1 else args.autodel * 24 * 60 * 60
    clean_interval = args.cleaninterval * 60
    upload_dir = './.minthost/uploads'

    os.makedirs(upload_dir, exist_ok=True)

    app = Flask(__name__)

    @app.route('/upload', methods=['POST'])
    def upload():
        original_name = request.headers.get('Mint-Filename')
        file = request.files.get('file')

        if not file or not original_name:
            return "Missing file or Mint-Filename", 418

        filename_b64 = base64url_encode(original_name)
        existing = [f for f in os.listdir(upload_dir) if f.startswith(filename_b64 + '_')]

        if existing:
            return "Filename already exists", 409

        file_bytes = file.read()
        if len(file_bytes) > max_file_size:
            return "File too large", 413

        try:
            if len(file_bytes) > get_available_disk_space(upload_dir):
                return "Insufficient storage space", 507
        except Exception as e:
            print("Disk space check failed:", e)
            return "Server error during disk space check", 500

        file_hash = hashlib.sha256(file_bytes).hexdigest()
        timestamp = int(time.time() * 1000)
        filename = f"{filename_b64}_{timestamp}_{file_hash}"
        path_out = os.path.join(upload_dir, filename)

        with open(path_out, 'wb') as f:
            f.write(file_bytes)

        print(f"Uploaded {original_name} as {file_hash}")

        return jsonify({
            "hash": file_hash,
            "status": "stored",
            "filename": original_name
        })

    @app.route('/<hash>', methods=['GET'])
    def download(hash):
        if not (len(hash) == 64 and all(c in "0123456789abcdef" for c in hash)):
            return "Invalid SHA256", 418

        matches = [f for f in os.listdir(upload_dir) if f.endswith(f"_{hash}")]
        if not matches:
            return "File not found", 404

        selected = sorted(matches, reverse=True)[0]
        parts = selected.split('_')

        if len(parts) < 3:
            return "Malformed file name", 500

        try:
            timestamp = int(parts[1])
        except ValueError:
            return "Invalid timestamp", 500

        age = int(time.time() * 1000) - timestamp
        file_path = os.path.join(upload_dir, selected)

        if auto_delete_time != -1 and age > auto_delete_time * 1000:
            try:
                os.remove(file_path)
                print(f"Deleted expired file: {selected}")
            except Exception as e:
                print(f"Failed to delete expired file {selected}: {e}")
            return "File expired", 410

        return send_file(file_path, as_attachment=True, download_name=hash)

    run_cleaner(upload_dir, auto_delete_time, clean_interval)

    print(f"congratulations! you successfully got a mint host running at http://localhost:{port}. note that you'll need to set up port forwarding (or run this on a service that assigns a domain name) to make it accessible to the world")
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    main()
