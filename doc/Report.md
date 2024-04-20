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

## Case study
We analyzed the first 100 record of `tranco.csv` and we obtained the following results:
You can see that the

// TODO -> add images and reports what's happening

