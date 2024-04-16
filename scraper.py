import json
import csv
import requests
from playwright.sync_api import sync_playwright

def get_csp_from_url(url):
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for non-2xx status codes

    # Extract CSP header (may vary depending on server configuration)
    csp_header_csp = response.headers.get('Content-Security-Policy')
    csp_header_hsts = response.headers.get('strict-transport-security')
    return csp_header_csp,csp_header_hsts
  except requests.exceptions.RequestException as e:
    print(f"Error retrieving CSP from {url}: {e}")
    return None

def inspect_headers(url, output_file):
    url = "https://" + url
    headers_data = {}  # Dictionary to hold headers data
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Enable request interception to capture response headers
        try:
            page.route('**', lambda route: route.continue_())
            page.goto(url)
        
            # Capture all response headers
            csp_header_csp,csp_header_hsts = get_csp_from_url(url)

            # Extract and store CSP and HSTS headers

            resource_data = {}  # Dictionary to hold headers data for each resource
            if csp_header_csp:
                resource_data["Content Security Policy (CSP)"] = csp_header_csp

            if csp_header_hsts:
                resource_data["HTTP Strict Transport Security (HSTS)"] = csp_header_hsts
                
                # Store headers data for the resource
                headers_data[url] = resource_data
        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")

        browser.close()

    # Write headers data to a JSON file
    with open(output_file, 'w') as f:
        json.dump(headers_data, f, indent=4)

def process_records(records):
    # Your function logic here
    for record in records:
        inspect_headers(record, "headers_data.json")

def main():
    file_path = "top-1m.csv"
    
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            # Read the first 5 rows
            first_five_rows = [row[1] for _, row in zip(range(5), reader)]
            process_records(first_five_rows)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
