import json

with open('headers_data.json', 'r') as file:
    json_data = json.load(file)

# csp_histogram = {}
# hsts_histogram = {}
total_urls = len(json_data)
csp_count = 0
hsts_count = 0
none_count = 0
csp_hsts_count = 0
only_csp_count = 0
only_hsts_count = 0

for url, details in json_data.items():
    csp_value = details.get("Content Security Policy (CSP)")
    if csp_value != "None":
        csp_count+=1

    hsts_value = details.get("HTTP Strict Transport Security (HSTS)")
    if hsts_value != "None":
        hsts_count+=1

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

# # Intercept
# csp_hsts_intercept = csp_perc * hsts_perc
# print(f"- Intercept: {csp_hsts_intercept}")

# # Cond
# csp_cond_hsts = csp_hsts_intercept/hsts_perc
# hsts_cond_csp = csp_hsts_intercept/csp_perc

#
csp_cond_hsts = only_csp_count / csp_hsts_union
hsts_cond_csp = only_hsts_count / csp_hsts_union
# Plots
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 6))

labels = ['CSP U HSTS', 'None']
counts = [csp_hsts_union, none_perc]
plt.subplot(1, 2, 1)  # 1 rows, 2 column, 1st grafico
plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('CSP U HSTS')
plt.axis('equal')

labels = ['CSP | HSTS', 'HSTS | CSP', 'CSP u HSTS']
counts = [csp_cond_hsts, hsts_cond_csp, csp_hsts_union]
plt.subplot(1, 2, 2)  # 1 rows, 2 column, 2nd grafico
plt.bar(labels, counts)
plt.title('CSP, HSTS')

plt.show()



    # csp_histogram[csp_value] = csp_histogram.get(csp_value, 0) + 1

    # hsts_value = details.get("HTTP Strict Transport Security (HSTS)")
    # hsts_histogram[hsts_value] = hsts_histogram.get(hsts_value, 0) + 1
    # if hsts_value and hsts_value.strip().lower() != "none":
    #     hsts_used_count += 1
    #     hsts_values = hsts_value.split(";")
    #     for value in hsts_values:
    #         value = value.strip()
    #         hsts_histogram[value] = hsts_histogram.get(value, 0) + 1

# print("CSP usage (%):")
# for csp, count in csp_histogram.items():
#     percentage = (count / total_urls) * 100
#     print(f"{csp}: {percentage:.2f}%")

# print("\nHSTS usage (%):")
# # print(f"Total sites using HSTS: {(hsts_used_count / total_urls) * 100:.2f}%")
# for hsts, count in hsts_histogram.items():
#     percentage = (count / total_urls) * 100
#     print(f"- {hsts}: {percentage:.2f}%")
