# aiocrioc
An LLM and OCR based Indicator of Compromise Extraction Tool.
Built as a POC to compare against straight regex and OCR see: [***ioc-ocr-extractor***](https://github.com/referefref/ioc-ocr-extractor)
The LLM version does significantly better at understanding the context of indicators like domains and file extensions which are often confused with plain regex (such as .com)


## Setup (tested on Ubuntu 22.04 with python3-venv)
```bash
# Download and install requirements
apt install tesseract-ocr python3 python3-venv git -y
# Clone git repo
git clone https://github.com/referefref/aiocrioc.git
cd ioc-ocr-extractor
# Setup python3 virtual environment
python3 -m venv env
source env/bin/activate
# Install python requirements with pip
pip install -r requirements.txt
# Set your openai key in the .env file
sed -i 's/REPLACEME/put your openai key here or edit the .env file/g' .env
```

## Usage
```bash
./extractor.py --url "url" --output "outputfile.json"
```

## Example
```bash
extract.py --url "https://thedfirreport.com/2024/01/29/buzzing-on-christmas-eve-trigona-ransomware-in-3-hours/" --output "test.json"
```
## Output
```json
[
    {
        "Indicator Type": "indicator type",
        "Indicator": "indicator",
        "Context": "context"
    },
    {
        "Indicator Type": "IP address",
        "Indicator": "77.83.36.6",
        "Context": "initial RDP connection from Ukraine"
    },
    {
        "Indicator Type": "IP address",
        "Indicator": "193.106.31.98",
        "Context": "second RDP connection"
    },
    {
        "Indicator Type": "domain name",
        "Indicator": "Mega.io",
        "Context": "used for data exfiltration"
    },
    {
        "Indicator Type": "file name",
        "Indicator": "build_redacted.exe",
        "Context": "Trigona Ransomware executable"
    },
    {
        "Indicator Type": "SHA-256 hash",
        "Indicator": "d743daa22fdf4313a10da027b034c603eda255be037cb45b28faea23114d3b8a",
        "Context": "hash for build_redacted.exe"
    },
    {
        "Indicator Type": "MD5 hash",
        "Indicator": "1852be15aa8dcf664291b3849bd348e4",
        "Context": "MD5 hash for build_redacted.exe"
    },
    {
        "Indicator Type": "SHA-1 hash",
        "Indicator": "eea811d2a304101cc0b0edebe6590ea0f3da0a27",
        "Context": "SHA-1 hash for build_redacted.exe"
    },
    {
        "Indicator Type": "file name",
        "Indicator": "DefenderOFF.bat",
        "Context": "batch script to disable Windows Defender"
    },
    {
        "Indicator Type": "SHA-256 hash",
        "Indicator": "d6d8302d8db7f17aaa45059b60eb8de33166c95d1d833ca4d5061201e4737009",
        "Context": "hash for DefenderOFF.bat"
    },
    {
        "Indicator Type": "MD5 hash",
        "Indicator": "c5d7ce243c1d735d9ca419cc916b87ec",
        "Context": "MD5 hash for DefenderOFF.bat"
    },
    {
        "Indicator Type": "SHA-1 hash",
        "Indicator": "21b7460aa5f7eb7a064d2a7a6837da57719f9c2e",
        "Context": "SHA-1 hash for DefenderOFF.bat"
    },
    {
        "Indicator Type": "file name",
        "Indicator": "newuser.bat",
        "Context": "script to create a new user named sys with password Taken1918"
    },
    {
        "Indicator Type": "username",
        "Indicator": "sys",
        "Context": "created by newuser.bat"
    },
    {
        "Indicator Type": "password",
        "Indicator": "Taken1918",
        "Context": "password for user sys created by newuser.bat"
    },
    {
        "Indicator Type": "file name",
        "Indicator": "newnewuser.bat",
        "Context": "script to create a user named Support with password Kawa72ws"
    },
    {
        "Indicator Type": "username",
        "Indicator": "Support",
        "Context": "created by newnewuser.bat"
    },
    {
        "Indicator Type": "password",
        "Indicator": "Kawa72ws",
        "Context": "password for user Support created by newnewuser.bat"
    },
    {
        "Indicator Type": "file name",
        "Indicator": "netscan.exe",
        "Context": "SoftPerfect\u2019s Netscan tool used for network discovery"
    },
    {
        "Indicator Type": "SHA-256 hash",
        "Indicator": "18f0898d595ec054d13b02915fb7d3636f65b8e53c0c66b3c7ee3b6fc37d3566",
        "Context": "hash for netscan.exe"
    },
    {
        "Indicator Type": "MD5 hash",
        "Indicator": "27f7186499bc8d10e51d17d3d6697bc5",
        "Context": "MD5 hash for netscan.exe"
    },
    {
        "Indicator Type": "SHA-1 hash",
        "Indicator": "52332ce16ee0c393b8eea6e71863ad41e3caeafd",
        "Context": "SHA-1 hash for netscan.exe"
    },
    {
        "Indicator Type": "file name",
        "Indicator": "rdp.exe",
        "Context": "Remote Desktop Plus tool dropped but not used"
    },
    {
        "Indicator Type": "SHA-256 hash",
        "Indicator": "8cf27e05e639fcc273d3cceadf68e69573b58e74b4bfce8460a418366a782fbd",
        "Context": "hash for rdp.exe"
    },
    {
        "Indicator Type": "MD5 hash",
        "Indicator": "037d9a5307e32252a3556bbe038a0722",
        "Context": "MD5 hash for rdp.exe"
    },
    {
        "Indicator Type": "SHA-1 hash",
        "Indicator": "641b7cf77286bd86eb144147bbf073bbd2c9c261",
        "Context": "SHA-1 hash for rdp.exe"
    },
    {
        "Indicator Type": "file name",
        "Indicator": "start \u2014 \u043a\u043e\u043f\u0438\u044f.bat",
        "Context": "batch script to execute rclone.exe for data exfiltration"
    },
    {
        "Indicator Type": "SHA-256 hash",
        "Indicator": "8b5fdb358b26c09a01c56de4de69841c67051f64ac8afcdd56dfddee06fdaa7b",
        "Context": "hash for start \u2014 \u043a\u043e\u043f\u0438\u044f.bat"
    },
    {
        "Indicator Type": "MD5 hash",
        "Indicator": "76faaf2e85045fcd1a404b7cb921d7c1",
        "Context": "MD5 hash for start \u2014 \u043a\u043e\u043f\u0438\u044f.bat"
    },
    {
        "Indicator Type": "SHA-1 hash",
        "Indicator": "4484887c6857a26e40f4337d64ac0df7c391ba83",
        "Context": "SHA-1 hash for start \u2014 \u043a\u043e\u043f\u0438\u044f.bat"
    }
]
```
