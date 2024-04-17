import json
import csv
from playwright.sync_api import sync_playwright
import requests


headers_data = {} # Dictionary to hold headers data for all resources

def inspect_headers(url, output_file,):
    url = "https://" + url
    print(f"Inspecting headers for {url}...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Enable request interception to capture response headers
        page.route('**', lambda route: route.continue_())
        try:
            response = page.goto(url)
        # Capture all response headers
            try:
                csp_header_csp = response.headers['content-security-policy']
                csp_header_hsts = response.headers['strict-transport-security']
            except KeyError:
                csp_header_csp = 'None'
                csp_header_hsts = 'None'
            

            # Extract and store CSP and HSTS headers
            resource_data = {}  # Dictionary to hold headers data for each resource
            if csp_header_csp:
                resource_data["Content Security Policy (CSP)"] = csp_header_csp

            if csp_header_hsts:
                resource_data["HTTP Strict Transport Security (HSTS)"] = csp_header_hsts
                
            # Store headers data for the resource
            headers_data[url] = resource_data


        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()



def process_records(records):
    # Your function logic here
    for record in records:
        inspect_headers(record, "headers_data.json")

def main():
    file_path = "top-1m.csv"
    output_file = "headers_data.json"
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            # Read the first 5 rows
            first_five_rows = [row[1] for _, row in zip(range(20), reader)]
            process_records(first_five_rows)
            # Write headers data to a JSON file
            with open(output_file, 'w') as f:
                json.dump(headers_data, f, indent=4)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
