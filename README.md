# aiocrioc
An LLM and OCR based Indicator of Compromise Extraction Tool

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
