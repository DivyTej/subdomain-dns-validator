import dns.resolver
import sys

# Function to read files (subdomains and IPs) and return lists
def read_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Function to check DNS A (IPv4), AAAA (IPv6), and CNAME records
def check_dns(subdomain, known_ips, resolver, valid_domains, invalid_domains, cname_domains, reserved_domains):
    try:
        resolved_ips = []
        subdomain_ok = False
        cname_target = None

        # Query the CNAME record of the subdomain
        try:
            result_cname = resolver.resolve(subdomain, 'CNAME')
            for cnameval in result_cname:
                cname_target = cnameval.to_text()
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass  # No CNAME found, ignore this part

        # Query the A (IPv4) record of the subdomain
        try:
            result_a = resolver.resolve(subdomain, 'A')
            for ipval in result_a:
                resolved_ips.append(ipval.to_text())
                if ipval.to_text() in known_ips:
                    subdomain_ok = True
        except dns.resolver.NoAnswer:
            pass  # Ignore if no A record exists

        # Query the AAAA (IPv6) record of the subdomain
        try:
            result_aaaa = resolver.resolve(subdomain, 'AAAA')
            for ipval in result_aaaa:
                resolved_ips.append(ipval.to_text())
                if ipval.to_text() in known_ips:
                    subdomain_ok = True
        except dns.resolver.NoAnswer:
            pass  # Ignore if no AAAA record exists

        # Categorize the subdomain
        if subdomain_ok:
            # Valid domain: IPs in yellow
            valid_domains.append(f"{subdomain} - \033[93m{', '.join(resolved_ips)}\033[0m")
        elif resolved_ips:
            # Invalid domain: IPs in red
            invalid_domains.append(f"{subdomain} - \033[91m{', '.join(resolved_ips)}\033[0m")
        elif cname_target:
            # Domain has CNAME but no A/AAAA records
            cname_domains.append(f"{subdomain} -> {cname_target}")
        else:
            # Check if the domain has nameservers
            try:
                # Query NS records to check if nameservers exist
                resolver.resolve(subdomain, 'NS')
                # If NS records exist, it's not a reserved domain
                pass
            except (dns.resolver.NoNameservers, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                # No nameservers found, mark as reserved
                reserved_domains.append(subdomain)

    except Exception as e:
        pass  # Ignore errors to keep the console clean

# Main function with graceful exit on Ctrl+C
def main(subdomain_file, ip_file, dns_server=None):
    try:
        # Read subdomains and IPs from the provided files
        subdomains = read_file(subdomain_file)
        known_ips = read_file(ip_file)

        # Set up the DNS resolver
        resolver = dns.resolver.Resolver()
        resolver.timeout = 10  # Increase timeout to 10 seconds
        resolver.lifetime = 10  # Increase total resolution lifetime to 10 seconds

        # If a DNS server is provided, use it
        if dns_server:
            resolver.nameservers = [dns_server]

        # Lists to store domains for each category
        valid_domains = []
        invalid_domains = []
        cname_domains = []
        reserved_domains = []

        # Iterate through subdomains and check their DNS records
        for subdomain in subdomains:
            check_dns(subdomain, known_ips, resolver, valid_domains, invalid_domains, cname_domains, reserved_domains)

        # Output tables
        print("\n--- Valid Domains ---")
        for domain in valid_domains:
            print(domain)

        print("\n--- Invalid Domains ---")
        for domain in invalid_domains:
            print(domain)

        print("\n--- CNAME Domains ---")
        for domain in cname_domains:
            print(domain)

        print("\n--- Reserved Domains ---")
        for domain in reserved_domains:
            print(domain)

        # Summary at the end
        print("\n--- DNS Check Summary ---")
        print(f"Total subdomains checked: {len(subdomains)}")
        print(f"Valid subdomains (infrastructure IP match): {len(valid_domains)}")
        print(f"Invalid subdomains (IP not in infrastructure): {len(invalid_domains)}")
        print(f"CNAME-only domains: {len(cname_domains)}")
        print(f"Reserved subdomains (no nameserver): {len(reserved_domains)}")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully...")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python script.py <subdomain_file> <ip_file> [<dns_server>]")
        sys.exit(1)

    subdomain_file = sys.argv[1]
    ip_file = sys.argv[2]

    # Get the DNS server if provided (third argument)
    dns_server = sys.argv[3] if len(sys.argv) == 4 else None

    # Start the main function
    main(subdomain_file, ip_file, dns_server)
