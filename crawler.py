# Author: [Mattia Dei Rossi - 885768@stud.unive.it, Alessandro Simonato - 882339@stud.unive.it ]
# Description: This script crawls a list of websites provided in a CSV file
# and gathers information about the HTTPS headers of each website.

import json
import csv
from playwright.sync_api import sync_playwright
import argparse

headers_data = {} # Dictionary to hold headers data for all resources

def inspect_headers(url):
    url = "https://" + url
    print(f"Inspecting headers for {url}...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
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
    for record in records:
        inspect_headers(record)
    
def main():
    """
    This Python3 script, crawler.py, is a command-line tool designed to crawl a list of websites provided in a CSV file and gather information about the HTTPS headers of each website. Here's how to use it:

    Usage:
        python3 crawler.py -f <input_filename> -o <output_filename> -n <number_of_domains>

    Arguments:
        -f, --input-file <input_filename>: Specifies the filename from which to read the list of domains to analyze.
        -o, --output-file <output_filename>: Specifies the destination file to save the results.
        -n, --num-domains <number_of_domains>: Specifies the number of domains to analyze (optional). If not provided, all domains will be analyzed.

    Example:
        To run the tool and analyze domains listed in 'tranco.csv', save the results to 'headers_data.json', and analyze only 100 domains, execute:
            ```
            python3 crawler.py -f tranco.csv -o headers_data.json -n 100
            ```

    After execution, the script will save the gathered information about the HTTP headers of each website to the specified output file in JSON format.

    Note: Ensure that you have necessary permissions to read the input CSV file and write to the output JSON file in the specified directory.
    """
    # Argument parsing
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--input-file', metavar='<input_filename>', required=True, help='Specifies the filename from which to read the list of domains to analyze.')
    parser.add_argument('-o', '--output-file', metavar='<output_filename>', required=True, help='Specifies the destination file to save the results.')
    parser.add_argument('-n', '--num-domains', metavar='<number_of_domains>',  required=True, type=int, help='Specifies the number of domains to analyze.')
    args = parser.parse_args()

    # Retrieve input filename, output filename, and number of domains
    input_filename = args.input_file
    output_filename = args.output_file
    num_domains = args.num_domains

    try:
        with open(input_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            urls = [row[1] for _, row in zip(range(num_domains), reader)]
            process_records(urls)
            with open(output_filename, 'w') as f:
                json.dump(headers_data, f, indent=4)
    except FileNotFoundError:
        print(f"File '{input_filename}' not found.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()