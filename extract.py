import argparse
import json
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from PIL import Image
import pytesseract
from dotenv import load_dotenv
import openai
from colorama import Fore, Style, init

init(autoreset=True)

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def download_page(url, user_agent):
	print(Fore.BLUE + "Downloading webpage content...")
	headers = {'User-Agent': user_agent}
	response = requests.get(url, headers=headers)
	response.raise_for_status()  
	soup = BeautifulSoup(response.text, 'html.parser')
	lines = [line.strip() for line in soup.get_text(separator='\n').split('\n') if line.strip()]
	noemptylines = "\n".join(lines)
	
	return noemptylines

def download_images(soup, base_url):
	print(Fore.BLUE + "Downloading images...")
	images = soup.find_all('img')
	downloaded_image_paths = []  # This list will store the paths of downloaded images.
	for img in images:
		img_url = urljoin(base_url, img.get('src'))
		if not img_url:
			continue  # Skip if img['src'] is None
		img_response = requests.get(img_url)
		img_name = os.path.basename(img_url)
		img_path = os.path.join(os.getcwd(), img_name)  
		with open(img_path, 'wb') as f:
			f.write(img_response.content)
		downloaded_image_paths.append(img_path)  # Add the path to the list
	return downloaded_image_paths  # Return the list of downloaded image paths

def ocr_image(image_path):
	print(Fore.BLUE + f"Performing OCR on {image_path}...")
	return pytesseract.image_to_string(Image.open(image_path))

def parse_openai_response_to_iocs(text):
	"""Parses the OpenAI text response into a list of IOC dictionaries."""
	iocs = []
	lines = [line for line in text.split('\n') if line.strip()]
	for line in text.split("\n"):
		parts = line.split(" : ")
		if len(parts) == 3:
			iocs.append({
				"Indicator Type": parts[0].strip(),
				"Indicator": parts[1].strip(),
				"Context": parts[2].strip(),
			})
		#else:
		#	print(Fore.RED + "Response format incorrect, resubmitting request...")
		#	return None
	return iocs

def extract_iocs_with_openai(content, context_identifier, retry_count=0, max_retries=1):
	if retry_count > max_retries:
		print(Fore.RED + "Maximum retry limit reached. Moving on without additional retries.")
		return []
	
	system_prompt = "Return only as requested, without comments or code blocks, only as plain text. If nothing is found return: 'No IOCs found in the provided text'"
	prompt = (f"Extract all IOCs (IP addresses, domain names, email addresses, email subject, file name, useragent strings, urls, usernames, passwords, SHA and MD5 hashes, and so on) from the following text and format each as 'indicator type : indicator : context'. Context should be information that surrounds the IOC, such as the filename assocaited to the hash, the type of infrastructure that eixsts on an IPv4 address, and so on. {content}")
	message=[{"role": "assistant", "content": system_prompt }, {"role": "user", "content": prompt}]

	try:
		response = openai.chat.completions.create(
			model="gpt-4-turbo-preview",
			messages=message,
			temperature=0.3,
			max_tokens=4096,
			top_p=1.0,
			frequency_penalty=0.0,
			presence_penalty=0.0
		)
		iocs_text = response.choices[0].message.content
		print(iocs_text)
		iocs = parse_openai_response_to_iocs(iocs_text)
		if iocs is None:
			print(Fore.YELLOW + f"Retry {retry_count+1}/{max_retries} due to format mismatch...")
			return extract_iocs_with_openai(content, context_identifier, retry_count+1, max_retries)
		return iocs
	except Exception as e:
		print(Fore.RED + f"An error occurred while querying OpenAI: {e}")
		return []

def cleanup_files(file_paths):
	for path in file_paths:
		try:
			os.remove(path)
			print(Fore.GREEN + f"Successfully removed {path}.")
		except Exception as e:
			print(Fore.RED + f"Error removing file {path}: {e}")

def main(url, output_file, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3", retry_limit=1):
	print(Fore.GREEN + "Starting IOC extraction process...")
	page_content = download_page(url, user_agent)
	soup = BeautifulSoup(page_content, 'html.parser')
	text_content = soup.get_text()
	downloaded_images = download_images(soup, url)
	
	text_iocs = extract_iocs_with_openai(text_content, "text_content", 0, retry_limit)
	
	all_iocs = text_iocs[:]
	for img_path in downloaded_images:
		img_text = ocr_image(img_path)
		img_iocs = extract_iocs_with_openai(img_text, img_path, 0, retry_limit)
		all_iocs.extend(img_iocs)  

	cleanup_files(downloaded_images)

	with open(output_file, 'w') as f:
		json.dump(all_iocs, f, indent=4)
	print(Fore.GREEN + "IOC extraction process completed.")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Extract IOCs from a webpage.')
	parser.add_argument('--url', required=True, help='The URL of the webpage to analyze')
	parser.add_argument('--output', required=True, help='The JSON file to output')
	parser.add_argument('--retry-limit', type=int, default=3, help='The maximum number of retries for OpenAI requests')
	args = parser.parse_args()

	main(args.url, args.output)
