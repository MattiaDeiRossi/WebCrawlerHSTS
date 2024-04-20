import json

with open('headers_data.json', 'r') as file:
    json_data = json.load(file)

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

# # Intercept
# csp_hsts_intercept = csp_perc * hsts_perc
# print(f"- Intercept: {csp_hsts_intercept}")

# # Cond
# csp_cond_hsts = csp_hsts_intercept/hsts_perc
# hsts_cond_csp = csp_hsts_intercept/csp_perc

#
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

#crea grafico






# Plots
import matplotlib.pyplot as plt

# Definisci i dati per il terzo grafico
hsts_histogram = {k: v for k, v in map(lambda item: (item[0], item[1] / hsts_count * 100), hsts_histogram.items())}
x = hsts_histogram.keys()
y = hsts_histogram.values()

# Crea un nuovo subplot per il terzo grafico
plt.subplot(2, 2, 3)  # 2 righe, 2 colonne, terzo grafico
plt.ylabel('Polices usage in %')
plt.xlabel('Polices')
plt.bar(x, y)
plt.title('Directives of HSTS header')

hsts_histogram = {k: v for k, v in map(lambda item: (item[0], item[1] / maxage_count * 100), hsts_histogram.items())}
x = maxage_histogram.keys()
y = maxage_histogram.values()


plt.subplot(2, 2, 4)  # 2 righe, 2 colonne, quarto grafico
plt.ylabel('Ages usage in %')
plt.xlabel('Ages')
plt.bar(x, y)
plt.title('Usage of Max-Age')

labels = ['CSP plus HSTS', 'None']
counts = [csp_hsts_union, none_perc]
plt.subplot(2, 2, 1)  # 2 righe, 2 colonne, primo grafico
plt.ylabel('Percentage of domains using CSP or HSTS')
plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title(' Using domains with CSP and HSTS')
plt.axis('equal')

# Aggiorna i dati e le etichette per il secondo grafico
labels = ['CSP without HSTS', 'HSTS without CSP', 'CSP and HSTS']
counts = [csp_cond_hsts, hsts_cond_csp, csp_hsts_union]
plt.subplot(2, 2, 2)  # 2 righe, 2 colonne, secondo grafico
plt.bar(labels, counts)
plt.title('Breakdown between CSP and HSTS headers')

# Mostra tutti i grafici
plt.tight_layout()  # Ottimizza la disposizione dei grafici
plt.show()

