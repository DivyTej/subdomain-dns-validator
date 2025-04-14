# subdomain-dns-validator

This Python script validates DNS records for a list of subdomains against a set of known infrastructure IPs. It checks for A (IPv4), AAAA (IPv6), and CNAME records, categorizing subdomains as valid, invalid, CNAME-only, or reserved.

## Features

* Checks A, AAAA, and CNAME records for subdomains.
* Compares resolved IPs against a list of known infrastructure IPs.
* Categorizes subdomains into:
    * **Valid:** IPs match known infrastructure.
    * **Invalid:** IPs do not match known infrastructure.
    * **CNAME-only:** Subdomains with CNAME records but no A/AAAA records.
    * **Reserved:** Subdomains with no nameservers (NS records).
* Colored output for easy identification of valid (yellow) and invalid (red) IPs.
* Optional custom DNS server specification.
* Graceful handling of DNS resolution errors and user interrupts (Ctrl+C).

## Prerequisites

* Python 3.x
* `dnspython` library: `pip install dnspython`

## Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DivyTej/subdomain-dns-validator
    cd subdomain-dns-validator
    ```

2.  **Prepare your input files:**
    * `subdomains.txt`: A file containing a list of subdomains (one per line).
    * `ips.txt`: A file containing a list of known infrastructure IPs (one per line).

3.  **Run the script:**
    ```bash
    python dns_checker.py subdomains.txt ips.txt [optional: dns_server]
    ```
    * Replace `subdomains.txt` and `ips.txt` with your actual file names.
    * Optionally, specify a custom DNS server (e.g., `8.8.8.8`).

    Example:
    ```bash
    python dns_checker.py subdomains.txt ips.txt 1.1.1.1
    ```

## Output

The script will output four tables:

* **Valid Domains:** Subdomains with IPs matching the provided infrastructure IPs.
* **Invalid Domains:** Subdomains with IPs not matching the provided infrastructure IPs.
* **CNAME Domains:** Subdomains with CNAME records but no A/AAAA records.
* **Reserved Domains:** Subdomains with no nameservers.

It also provides a summary of the checked subdomains.

## Example Input Files

**subdomains.txt:**
www.example.com
api.example.com
mail.example.com
test.example.com

**ips.txt:**

192.168.1.10
192.168.1.20


## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bug fixes or feature requests.
