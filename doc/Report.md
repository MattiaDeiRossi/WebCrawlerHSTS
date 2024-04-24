# Measuring HSTS Adoption

<a>
    <img src="./img/unive.png" alt="logo" title="CaFoscari" align="right" height="100" />
</a>

### Authors
- Mattia Dei Rossi - 885768@stud.unive.it
- Alessandro Simonato - 882339@stud.unive.it 

## Goals
We are tasked to measure the state of HSTS adoption on the Web. This activity is performed in groups of two people and involves several steps:
1.  Write a crawler to collect HSTS policies from live websites and store them, e.g., in a database
2. Write a security analyzer for the collected HSTS policies designed to draw conclusions about the state of security in the wild
3. Write a report detailing the crawling procedure, the security analysis procedure and the findings of your study

## HSTS
HTTP Strict Transport Security (HSTS) is a policy mechanism that helps to protect websites against man-in-the-middle attacks such as cookie hijacking. The HSTS Policy is communicated by the server to the user agent via an HTTP response header field named `Strict-Transport-Security`. HSTS can be used also to prevent SSL stripping.
The HSTS policies are:

### max-age
It specifies the maximum amount of time (in seconds) that the HSTS policy should be enforced by the browser.

### includeSubDomains
It instructs the browser to apply the HSTS policy not only to the current domain but also to all of its subdomains. Using subdomains in the HSTS policy ensure that all communication with the entire domain hierarchy is encrypted over HTTPS,

### preload
It indicates to web browsers that the domain should be included in the HSTS preload list.
The HSTS preload list is a list of websites maintained by browser vendors that are hardcoded into their respective browsers. Websites on this list will automatically have the HSTS policy enforced, even for the initial HTTP connection attempt. This means that before the browser even attempts to make a connection to a website on the preload list, it will ensure that the connection is over HTTPS.

## CSP vs HSTS 
CSP (Content Security Policy) and HSTS (HTTP Strict Transport Security) are both important security mechanisms used to enhance web application security, but they serve different purposes:

### Content Security Policy (CSP):
- CSP is a security standard that helps prevent various types of attacks, such as Cross-Site Scripting (XSS) and data injection attacks.
- It allows web developers to control which resources (scripts, stylesheets, fonts, etc.) a browser is allowed to load and execute on a particular web page. 
- CSP works by allowing developers to define a whitelist of trusted sources for content such as scripts, stylesheets, and other resources. If a browser detects that content from an unauthorized source is attempting to load or execute, it will block it according to the policy rules.
- CSP headers are delivered via HTTP headers or within a meta tag in the HTML code.
### HTTP Strict Transport Security (HSTS):
- HSTS is a security policy mechanism that helps protect websites against man-in-the-middle attacks and cookie hijacking by forcing web browsers to communicate with a website using only secure HTTPS connections.
- Once a web server sends an HSTS header to a browser, the browser will only communicate with that server over HTTPS for a specified period of time (the max-age directive).
- This helps to ensure that sensitive data such as login credentials or session cookies are always transmitted over encrypted connections, reducing the risk of interception or tampering by attackers.
- HSTS headers are delivered via HTTP response headers.

In summary, CSP is primarily focused on preventing malicious code execution and data injection attacks by controlling which resources can be loaded and executed on a web page, while HSTS is focused on enforcing secure communication between the browser and the server by mandating the use of HTTPS.

## Crawler
This is a simple script that uses Playwright to parse the HTTPS headers of a number of websites and save the collected information in a JSON file. 
This script accepts a URL as input and inspects the HTTPS headers of that URL
to then start an instance of the Chromium browser and open a new page.
Then we try to visit the domain, if it responds with the header we take the CSP and HSTS information to save it inside a JSON file.
Then the Json file will be parsed by another script that will extract the information we will describe in the case study
## Case study
We analyzed the first 100 record of `tranco.csv` and we obtained the following results:
The pie chart shows the percentage of domains using Content Security Policy (CSP) and HTTP Strict Transport Security (HSTS).
-None: 64.3% of domains use neither CSP nor HSTS.
-CSP and HSTS: 35.7% of domains use both CSP and HSTS.

<a>
    <img src="./img/CSP_HSTS_USAGE.png" alt="logo" title="CaFoscari" align="center" height="300" />
</a>

 The majority of domains (64.3%) do not yet use either CSP or HSTS. This means that these websites are vulnerable to a range of cyber threats, including:

**Script injection**: Attackers can inject malicious code into websites that do not use CSP, allowing them to steal data, hijack users or even take control of the website.

**Cross-Site Scripting (XSS)**: XSS is a type of attack that allows attackers to inject malicious JavaScript code into websites. This code can be used to steal cookies, user sessions or even take control of the user's browser.

**Mixed Content Sniffing**: When a website does not use HSTS, the connections between the website and the user's browser are not encrypted. This means attackers can intercept connections and steal sensitive data, such as passwords or credit card information.

Instead, with this graph we can see of those using CSP or HSTS how they are apportioned (i.e., whether they use only one or both)

<a>
    <img src="./img/CSP_HSTS_Headers.png" alt="logo" title="CaFoscari" align="center" height="300" />
</a>

In this graph we can see that no domain only CSP or HSTS. But they all use both CSP and HSTS. This is the safest group of websites, as they are protected from a number of cyber threats.


The bars in the graph show the policies we found and with what percentage they are repeated.

<a>
    <img src="./img/HSTS_Header.png" alt="logo" title="CaFoscari" align="center" height="300" />
</a>


We can note The most common HSTS directives are max-age and preload.
The includesubdomains directive is used less frequently.

**max-age**: This parameter specifies the duration, in seconds, for which the browser should store the information that the Web site is to be accessed exclusively via HTTPS. For example, For example, the browser will keep this information for the defined time, after which the Web site should reaffirm the HSTS policy.

**preload**: This directive allows websites to be included in the HSTS preload list in major browsers. When a site is preloaded, the browser automatically stores it as an HSTS site before even visiting it for the first time. This helps ensure that the connection to the site is always via HTTPS and helps prevent downgrade attacks.

**includeSubDomains**: This directive indicates whether the HSTS policy should also be extended to subdomains of the main site. If set to includeSubDomains, the HSTS policy will apply to all subdomains of the main site, ensuring that they too are only accessible via HTTPS.

the last graph serves us to understand the various domains that values put within 'max-age' useful for understanding the possible vulnerabilities given by it.

<a>
    <img src="./img/Max-Age.png" alt="logo" title="CaFoscari" align="center" height="300" />
</a>

This chart is useful because if a max-age value is set too long, such as several years, and later the website needs to change its behavior, such as switching from HTTPS to HTTP or using a different certificate, it may be difficult to remove or change the HSTS policy because of the extended duration.

## Conclusioni


We can see that more than 60% of domains do not use HSTS and this makes them vulnerable to attacks such as: Man-in-the-Middle attacks, Redirection attacks to HTTPS, Spoofing attacks, Exposure to protocol downgrades. 
We mainly encountered 3 policies: preload, includesubdomain, max-age.
Preloading is used by 60% of the domains analyzed and is a mechanism for adding one's website to a predefined list maintained by browsers. Avoiding downgrade attacks. IncludeSubDomains is used by only 40 percent of domains and instructs browsers to apply the HSTS policy not only to the main domain, but also to all its subdomains giving Uniformity of security policy across all domains used.
Finally, instead the max-age policy is used by all analyzed domains and indicates which browser should store the HSTS policy for a given domain. Instead, the max-age policy is used by all analyzed domains and indicates which browser should store the HSTS policy for a given domain. The max-age is also analyzed for its value since a high max-age could cause browsers to continue to apply the compromised HSTS policy for a long period, even after the problem was fixed. This could lead to a vulnerability as the browser continues to request connections via HTTPS even though the certificate has been compromised.
