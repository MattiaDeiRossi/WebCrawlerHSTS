import json

with open('headers_data.json', 'r') as file:
    json_data = json.load(file)

csp_histogram = {}
hsts_histogram = {}
total_urls = len(json_data)
hsts_used_count = 0

for url, details in json_data.items():
    # csp_value = details.get("Content Security Policy (CSP)")
    # csp_histogram[csp_value] = csp_histogram.get(csp_value, 0) + 1

    hsts_value = details.get("HTTP Strict Transport Security (HSTS)")
    if hsts_value and hsts_value.strip().lower() != "none":
        hsts_used_count += 1
        hsts_values = hsts_value.split(";")
        for value in hsts_values:
            value = value.strip()
            hsts_histogram[value] = hsts_histogram.get(value, 0) + 1

# print("CSP usage (%):")
# for csp, count in csp_histogram.items():
#     percentage = (count / total_urls) * 100
#     print(f"{csp}: {percentage:.2f}%")

print("\nHSTS usage (%):")
print(f"Total sites using HSTS: {(hsts_used_count / total_urls) * 100:.2f}%")
for hsts, count in hsts_histogram.items():
    percentage = (count / hsts_used_count) * 100
    print(f"- {hsts}: {percentage:.2f}%")
