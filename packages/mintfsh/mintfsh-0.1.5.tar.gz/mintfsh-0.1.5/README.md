# mint
Mint is a CLI-based file sharing and hosting service
## Features
* **Secure and private**: Mint clients never actually works with your files- think of Mint like a translator that structures and mediates communications between you and the host. Additionally, Mint has full Tor support for more anonymity.
* **Fast**: Mint is designed to be as lightweight on the upload/download process as possible- adding almost no latency to direct communications between the client and host.
* **Easy**: All you need to get started with Mint are two commands: `mint upload` and `mint download`. Adding more hosts or configuring identities is as easy as pasting in a few lines of JSON provided by the host.
## Quickstart
This guide is a quickstart to get you sharing and downloading ASAP on Mint!
### Installation and Test
First, install Mint:
```sh
pip install mintfsh
```
Then, check if it's installed:
```
which mint
```
If it returns a path, great! If not, add your Python package directory to `PATH`. To test Mint, run:
```
mint download test
```
It will ask you if you'd like Mint to create a configuration file for you. Type `y` or just press enter to continue and Mint will automatically create the configuration for you. Then, Mint will download the file `mint_test.txt` for you- run `cat ./mint_test.txt` or open it in a text editor to see some info about the request and host!
### Downloading/uploading
The default config comes with a preconfigured official Mint host! It will work fine for testing/casual sharing, but keep in mind:
* 750MB file size limit
* Deletes files after 7 days
* One file per filename
* Latency

Just run:
```
mint upload <filename>
```
And it will output a SHA256 hash for the file, like:
```
a6ed0c785d4590bc95c216bcf514384eee6765b1c2b732d0b0a1ad7e14d3204a
```
Then, if we want to download that same file from somewhere else (with the same host of course):
```
mint download a6ed0c785d4590bc95c216bcf514384eee6765b1c2b732d0b0a1ad7e14d3204a
```
## Quickstart for hosts
So, you want to set up a Mint host! Running a Mint host is a great way to promote equal access to code and important info, and also a fun learning experience. Mint provides two options for hosting: Node-based (Express) and Python-based (Flask). 
### Prerequisites
* If you're planning on using the Flask host, make sure you have Mint installed:
```
pip install mintfsh
```
* Space on your machine- Mint will make sure that you don't run out, but have at least 5GB available. 
* Good uptime- to be a great host, where many people trust you to be on their hosts list, you will want good uptime. Don't use something like a personal laptop if you plan on keeping it as a serious host, unless you can keep it on for around 95% of the time.
## Flask host (easiest)
The Flask-based host is easy to set up. Again, make sure you have mint installed, then run:
```
mint-host 3000
```
The command takes in other options too:
```
mint host 1234 --maxfs 750 --autodel 7 --cleaninterval 5
```
These are optional, but they let you set the port, max file size, autodelete time, and cleanup interval respectively.\
## Node host (advanced)
Flask is great, but for hosting serious services, Express is faster and more scalable. To run this, simply go to the mint repo and download `mint-host/full_server.js`. Then, run it with Node, and change the constants at the top if needed.
## Using it
It will run on `localhost:3000` by default, which is in the default Mint hosts list. To share it with the world, you can:
* Find a hosting provider (easier for Node, Flask usually requires a VM)
* Set up port forwarding and use your IP/a domain you own
* Set up a tunnel (for example, cloudflared) to your computer. This is easiest and comes with a domain.