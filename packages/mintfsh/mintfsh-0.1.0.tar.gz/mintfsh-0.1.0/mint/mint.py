import json
import os
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
import argparse

RESET = "\033[0m"

#aaf0d1
MINT = "\033[38;2;170;240;209m"
MINT_BOLD = "\033[1;38;2;170;240;209m"

#ffff00
YELLOW = "\033[38;2;255;255;0m"
YELLOW_BOLD = "\033[1;38;2;255;255;0m"

WHITE = "\033[38;2;255;255;255m"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def fSha256(f):
    h = hashlib.sha256()
    for chunk in iter(lambda: f.read(8192), b''):
        h.update(chunk)
    return h.hexdigest()

def printm(*args, **kwargs):
    print(MINT + " ".join(map(str, args)) + RESET, **kwargs)
def printmb(*args, **kwargs):
    print(MINT_BOLD + " ".join(map(str, args)) + RESET, **kwargs)
def printy(*args, **kwargs):
    print(YELLOW + " ".join(map(str, args)) + RESET, **kwargs)
def printyb(*args, **kwargs):
    print(YELLOW_BOLD + " ".join(map(str, args)) + RESET, **kwargs)
def printr(*args, **kwargs):
    print(RESET + " ".join(map(str, args)) + RESET, **kwargs)

class MintConfigError(Exception):
    def __init__(self, message, path=None):
        self.message = message
        self.path = path
        super().__init__(self.__str__())

    def __str__(self):
        if self.path:
            return f"MintConfigError in '{self.path}': {self.message}"
        return f"MintConfigError: {self.message}"
    
class MintUnknownError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.__str__())

    def __str__(self):
        return f"MintUnknownError: {self.message}"

class MintDownloadError(Exception):
    def __init__(self, file_hash, message):
        self.file_hash = file_hash
        self.message = message
        super().__init__(self.__str__())

    def __str__(self):
        return f"MintDownloadError for file with SHA256 sum '{self.file_hash}': {self.message}"

class MintPublishError(Exception):
    def __init__(self, file_path, message):
        self.file_path = file_path
        self.message = message
        super().__init__(self.__str__())

    def __str__(self):
        return f"MintPublishError for file at path '{self.file_path}': {self.message}"

def loadConfig(path="~/.mintfsh/config.json"):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        doCreateConfig = input(f"Configuration file at path {path} does not exist. Have Mint create the default config there? [Y/n]: ").strip().lower()
        if doCreateConfig in ["y", "yes", ""]:
            return createConfig(path)
        else:
            raise MintConfigError(f"Configuration file at path {path} not found (user declined to create it)")
    try:
        with open(path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise MintConfigError(f"Error decoding Mint config: {e}", path)
    except FileNotFoundError:
        raise MintConfigError(f"Configuration file at path {path} not found")
    except Exception as e:
        raise MintUnknownError(f"An unknown error occured when running Mint: {e}")
    return config

def createConfig(path="~/.mintfsh/config.json"):
    path = os.path.expanduser(path)
    config = {
        "hosts": [
            {
                "name": "default",
                "host": "https://mint-test.giacomosm.workers.dev/",
                "priority": 0,
                "identity": "test-identity",
            }
        ],
        "tor": False,
        "identity": "default",
    }
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "x") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        raise MintUnknownError(f"An unknown error occurred when creating Mint config: {e}")
    return config

def publish(file_path, config):
    printm(f"Uploading file: {file_path}")
    # placeholder return
    return None

def download(file_id, config):
    # Validate hash or special case
    is_valid_sha256 = (
        len(file_id) == 64 and all(c in "0123456789abcdef" for c in file_id.lower())
    )

    if not is_valid_sha256 and file_id != "test":
        raise MintDownloadError(file_id, "Invalid file ID. Must be a valid SHA256 or test!")

    last_error = None

    for host in sorted(config["hosts"], key=lambda h: h.get("priority", 0)):
        url = f"{host['host'].rstrip('/')}/{file_id}"
        identity = host.get("identity", config.get("identity"))

        headers = {
                "User-Agent": "mint-client",
                "Accept": "*/*",
        }
        if identity:
            headers["Mint-Identity"] = identity

        printy(f"Trying {url}...")

        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                filename = resp.headers.get("Mint-Filename") or f"{file_id}.mintdownload"

                if is_valid_sha256:
                    actual_hash = hashlib.sha256(data).hexdigest()
                    if actual_hash != file_id:
                        printr(f"Hash mismatch from {host['name']} (got {actual_hash})! Expected {file_id}. Skipping this host")
                        continue

                with open(filename, "wb") as f:
                    f.write(data)

                printmb("Saved to", filename)
                return

        except urllib.error.HTTPError as e:
            if e.code == 403:
                msg = f"Access denied (403) on host '{host['name']}'. Well behaved Mint hosts only throw this based on the identity they recieve. Some platforms may have signups/payment required to get a valid identity- like an API key."
                printyb(msg)
                printm(e)
                last_error = msg
            elif e.code == 404:
                msg = f"File not found (404) on host '{host['name']}'"
                printr(msg)
                last_error = msg
            else:
                msg = f"Host '{host['name']}' responded with HTTP {e.code}"
                printr(msg)
                last_error = msg

        except Exception as e:
            msg = f"Unknown error on host '{host['name']}': {e}. Make sure the host is reachable and follows Mint best practices"
            printr(msg)
            last_error = msg

    raise MintDownloadError(file_id, last_error or "File not found on any configured host")

def print_config(config):
    # for now, just echos the config
    # need to make it actually parse the json later
    # qwertyuiopasdfghjklzxcvbnm so much to do
    printmb("Mint configuration:")
    print(json.dumps(config, indent=4))

def main():
    parser = argparse.ArgumentParser(
        prog="mint",
        description="a simple, fast and secure file sharing tool"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # mint upload <file>
    upload_parser = subparsers.add_parser("upload", help="Upload a file")
    upload_parser.add_argument("file", help="Path to file to upload")

    # mint download <sha256>
    download_parser = subparsers.add_parser("download", help="Download a file by its SHA256")
    download_parser.add_argument("hash", help="SHA256 sum of the file")

    # mint info
    subparsers.add_parser("info", help="Displays info about Mint configuration")

    args = parser.parse_args()
    config = loadConfig()

    try:
        if args.command == "upload":
            publish(args.file, config)
        elif args.command == "download":
            download(args.hash, config)
        elif args.command == "info":
            print_config(config)
    except (MintDownloadError, MintPublishError, MintUnknownError, MintConfigError) as e:
        printr(str(e))
        exit(1)

if __name__ == "__main__":
    main()
