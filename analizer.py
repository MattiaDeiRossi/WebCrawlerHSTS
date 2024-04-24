# Author: [Mattia Dei Rossi - 885768@stud.unive.it, Alessandro Simonato - 882339@stud.unive.it ]
# Description: This script analyzes the adoption of HTTP Strict Transport Security (HSTS) policy based on the input file provided.
import argparse
import json
import matplotlib.pyplot as plt


def make_plots(json_data):
    csp_histogram = {}
    hsts_histogram = {}
    maxage_histogram = {}
    total_urls = len(json_data)
    csp_count = 0
    hsts_count = 0
    none_count = 0
    maxage_count = 0
    csp_hsts_count = 0
    only_csp_count = 0
    only_hsts_count = 0


    for url, details in json_data.items():
        csp_value = details.get("Content Security Policy (CSP)")
        if csp_value != "None":
            csp_count+=1
        
        hsts_value = details.get("HTTP Strict Transport Security (HSTS)")
        hsts_value = hsts_value.replace("/n", " ")
        if hsts_value != "None":
            hsts_count+=1
            hsts_values = hsts_value.lower().strip().split(";")
            for value in hsts_values:
                hsts_values = value.strip().split("=")
                key = hsts_values[0].lower()
                value = hsts_values[1].lower() if len(hsts_values) > 1 else ''
                hsts_histogram[key] = hsts_histogram.get(key, 0) + 1
                if(key == "max-age"):
                    maxage_count+=1 
                    value = int(value) / (31 * 24 * 60 * 60)
                    if value <= 1:
                        key = 'under 1 month'
                    elif value < 12:
                        key = "1-12 months"
                    else:
                        key = "over 12 months"
                    maxage_histogram[key] = maxage_histogram.get(key, 0) + 1
            

        if csp_value != "None" and hsts_value == "None":
            only_csp_count+=1
        if csp_value == "None" and hsts_value != "None":
            only_hsts_count+=1

        if csp_value == "None" and hsts_value == "None":
            none_count+=1
        else:
            csp_hsts_count+=1

    print(f"Total URLs: {total_urls}")

    csp_perc = (csp_count / total_urls) 
    print(f"- Total CSP: {csp_perc:.2f}%")
    hsts_perc = (hsts_count / total_urls) 
    print(f"- Total HSTS: {hsts_perc:.2f}%")
    none_perc = (none_count / total_urls) 
    print(f"- Total None: {none_perc:.2f}%")

    # Union
    csp_hsts_union = (csp_hsts_count/ total_urls)
    print(f"- Union: {csp_hsts_union}")

    csp_cond_hsts = only_csp_count / csp_hsts_union
    hsts_cond_csp = only_hsts_count / csp_hsts_union


    print("\nHSTS usage (%):")
    print(f"Total sites using HSTS: {(hsts_count / total_urls) * 100:.2f}%")
    for hsts, count in hsts_histogram.items():
        percentage = (count / hsts_count)
        print(f"- {hsts}: {percentage * 100:.2f}% (Total: {count})")
    print("\nMax-Age:")
    print(f"Max-Age <1 <12 >12")
    for key, value in maxage_histogram.items():
        print(f"- {key}: {value}")

    # Plots
    hsts_histogram = {k: v for k, v in map(lambda item: (item[0], item[1] / hsts_count * 100), hsts_histogram.items())}
    x = hsts_histogram.keys()
    y = hsts_histogram.values()
    plt.subplot(2, 2, 3)  
    plt.ylabel('Polices usage in %')
    plt.xlabel('Polices')
    plt.bar(x, y)
    plt.title('Directives of HSTS header')

    hsts_histogram = {k: v for k, v in map(lambda item: (item[0], item[1] / maxage_count * 100), hsts_histogram.items())}
    x = maxage_histogram.keys()
    y = maxage_histogram.values()
    plt.subplot(2, 2, 4)  
    plt.ylabel('Ages usage')
    plt.xlabel('Ages')
    plt.bar(x, y)
    plt.title('Usage of Max-Age')

    labels = ['CSP plus HSTS', 'None']
    counts = [csp_hsts_union, none_perc]
    plt.subplot(2, 2, 1)  
    plt.ylabel('Percentage of domains using CSP or HSTS')
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(' Using domains with CSP and HSTS')
    plt.axis('equal')
    # Breakdown between CSP and HSTS headers in percentage
    csp_hsts_union_perc = (csp_hsts_union/csp_hsts_count) * 100
    labels = ['CSP without HSTS', 'HSTS without CSP', 'CSP and HSTS']
    counts = [csp_cond_hsts, hsts_cond_csp, csp_hsts_union_perc]
    plt.subplot(2, 2, 2)  
    plt.bar(labels, counts)
    plt.title('Breakdown between CSP and HSTS headers')

    # Show all graphs
    plt.tight_layout() 
    plt.show()

def main():
    """
    This Python3 script, analyzer.py, is a command-line tool designed to analyze the adoption of HTTP Strict Transport Security (HSTS) policy based on the input file provided. Here's how to use it:

    Usage:
        python3 analyzer.py -f <input_filename>

    Arguments:
        -f, --input-file <input_filename>: Specifies the filename from which to read the list of websites to analyze for HSTS adoption.

    Example:
        To run the tool and analyze HSTS adoption based on the list of websites in 'websites.csv', execute:
            ```
            python3 analyzer.py -f websites.csv
            ```

    After execution, the script will analyze the adoption of HSTS policy for each website listed in the input file and provide relevant statistics.

    Note: Ensure that you have necessary permissions to read the input CSV file in the specified directory.
    """
    # Argument parsing
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--input-file', metavar='<input_filename>', required=True, help='Specifies the filename from which to read the list of websites to analyze for HSTS adoption.')
    args = parser.parse_args()

    # Retrieve input filename
    input_filename = args.input_file
    try:
        with open(input_filename, 'r') as file:
            json_data = json.load(file)
            make_plots(json_data)
    except FileNotFoundError:
            print(f"File '{input_filename}' not found.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()