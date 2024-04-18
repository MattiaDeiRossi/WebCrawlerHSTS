
import json
from playwright.sync_api import sync_playwright

def get_csp_header():
     with sync_playwright() as p:
        browser =  p.chromium.launch()
        page =  browser.new_page()
        
        
        # Now you can navigate to a page
        response =  page.goto("https://google.com")
        
        json_str = json.dumps(response.headers, indent=4)

        # Print response headers
        print("Response Headers:")
        print(json_str)
        
        # Other actions on the page...
        
        # Close the browser
        browser.close()

# Run the async function
get_csp_header()
