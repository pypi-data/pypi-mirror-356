from mcp.server.fastmcp import FastMCP
import shodan
import os

# Load API key from environment variable for safety
SHODAN_API_KEY = os.environ.get("SHODAN_API_KEY", "your_shodan_api_key")
api = shodan.Shodan(SHODAN_API_KEY)

mcp = FastMCP("Shodan MCP Toolkit")

@mcp.tool()
def shodan_search(query: str, limit: int = 5):
    """Advanced search with filters and facets."""
    results = api.search(query)
    return results['matches'][:limit]

@mcp.tool()
def get_ip_info(ip: str):
    """Get detailed information about an IP: open ports, services, and location."""
    return api.host(ip)

@mcp.tool()
def dns_lookup(domain: str):
    """Perform DNS lookup to get IP from domain."""
    return api.dns.resolve(domain)

@mcp.tool()
def reverse_dns(ip: str):
    """Get domain name for a given IP (reverse DNS)."""
    return api.dns.reverse(ip)

@mcp.tool()
def domain_info(domain: str):
    """Get domain info including subdomains."""
    return api.dns.domain_info(domain)

@mcp.tool()
def on_demand_scan(ip: str):
    """Launch an on-demand scan on a target IP (requires upgraded API access)."""
    return api.scan([ip])

@mcp.tool()
def create_network_alert(name: str, ip: str):
    """Create a new network alert to monitor an IP."""
    return api.alert.create(name=name, filters={"ip": ip})

@mcp.tool()
def list_alerts():
    """List all existing network alerts."""
    return api.alerts()

@mcp.tool()
def get_cves(query: str, limit: int = 3):
    """Perform vulnerability analysis with CVE tracking."""
    results = api.search(query)
    cves = []
    for item in results["matches"][:limit]:
        for vuln in item.get("vulns", []):
            cves.append({
                "ip": item["ip_str"],
                "cve": vuln,
                "summary": item["vulns"][vuln]["summary"]
            })
    return cves

@mcp.tool()
def get_api_info():
    """Return information about API usage and limits."""
    return api.info()

@mcp.tool()
def get_historical_data(ip: str):
    """Get historical scan data for an IP (premium access required)."""
    return api.host(ip, history=True)


def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
