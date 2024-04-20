
import json
from playwright.sync_api import sync_playwright

def get_csp_header():
     with sync_playwright() as p:
        browser =  p.chromium.launch()
        page =  browser.new_page()
        
        
        # Now you can navigate to a page
        response =  page.goto("https://www.mozilla.org")

        try:
                csp_header_csp = response.headers['content-security-policy']
                csp_header_hsts = response.headers['strict-transport-security']
        except KeyError:
                csp_header_csp = 'None'
                csp_header_hsts = 'None'
        
        json_str = json.dumps(response.headers, indent=4)

        # Print response headers
        print("Response Headers:")
        print(json_str)

        # Print CSP and HSTS headers
        print(f"Content Security Policy (CSP): {csp_header_csp}")
        print(f"HTTP Strict Transport Security (HSTS): {csp_header_hsts}")


        
        # Other actions on the page...
        
        # Close the browser
        browser.close()

# Run the async function
get_csp_header()
