# Python Standard Library Imports
import ipaddress
import json
import os
import re

# Third Party Imports
from dotenv import load_dotenv
from shodan import Shodan, exception


def _ip_sort_key(ip):
    # Sort IPs numerically (so 9.x sorts before 10.x); fall back to text for
    # anything that isn't a valid address.
    try:
        return (0, int(ipaddress.ip_address(ip.strip())))
    except ValueError:
        return (1, ip.strip())


def write_ips(filepath, ip_iterable):
    # Write a de-duplicated, numerically sorted list of IPs. Using a context
    # manager guarantees the data is flushed/closed before anything reads it.
    unique_sorted = sorted(set(ip_iterable), key=_ip_sort_key)
    with open(filepath, "w") as f:
        for ip in unique_sorted:
            f.write(f"{ip}\n")


# A safe product name: no path separators, no parent-dir tricks, not blank.
_SAFE_NAME = re.compile(r"^[^/\\]+$")


def load_custom_queries(path):
    """Load and validate custom queries from a JSON file.

    Returns a dict of {product_name: [query, ...]} containing only the entries
    that passed validation. Invalid entries are skipped with a warning rather
    than aborting the whole run, and a malformed/missing file yields {}.
    """
    try:
        with open(path, "r") as f:
            raw = json.load(f)
    except FileNotFoundError:
        return {}  # No custom query file present; normal case.
    except json.JSONDecodeError:
        print(f"{path} is empty or not valid JSON; ignoring it.")
        return {}

    if not isinstance(raw, dict):
        print(f"{path} must be a JSON object of {{\"Product\": [queries]}}; ignoring it.")
        return {}

    validated = {}
    for product, queries in raw.items():
        name = str(product).strip()
        if not name or not _SAFE_NAME.match(name):
            print(f"  Skipping custom query: invalid product name {product!r}.")
            continue
        # Allow a lone string as a convenience, but normalize to a list.
        if isinstance(queries, str):
            queries = [queries]
        if not isinstance(queries, list) or not all(isinstance(q, str) and q.strip() for q in queries):
            print(f"  Skipping '{name}': queries must be a string or a list of non-empty strings.")
            continue
        validated[name] = queries

    return validated


def shodan():
    api_key = os.environ.get("SHODAN_API_KEY", "").strip()
    if not api_key:
        print("SHODAN_API_KEY is not set. Set it in your environment or a .env file and try again.")
        return
    api = Shodan(api_key)
    queries = {
        # https://gi7w0rm.medium.com/the-curious-case-of-the-7777-botnet-86e3464c3ffd
        #"7777 Botnet": [
        #    "hash:1357418825"
        #],
        #"AcidRain Stealer": [
        #    'http.html:"AcidRain Stealer"'
        #],
        #"Ares RAT C2": [
        #    "product:'Ares RAT C2'"
        #],
        "AsyncRAT": [
            "product:AsyncRAT"
        ],
        #"Atlandida Stealer": [
        #    "http.title:'Atlantida' http.html:'GY7HXsD.jpg'"
        #],
        #"Bandit Stealer": [
        #    "http.title:Login http.html:'Welcome to Bandit' 'Content-Length: 4125' port:8080"
        #],
        #"BitRAT": [
        #    "product:BitRAT"
        #],
        #"BlackNet Botnet": [
        #    "http.title:'BlackNet - Login'"
        #],
        "Brute Ratel C4": [
            "http.html_hash:-1957161625",
            "product:'Brute Ratel C4'"
        ],
        "BurpSuite": [
            "product:BurpSuite"
        ],
        "Caldera C2": [
            'http.title:"Login | CALDERA"',
            # https://twitter.com/ViriBack/status/1713714868564394336
        #    "http.favicon.hash:-636718605",
        #    "http.html_hash:-1702274888"
        ],
        "Cobalt Strike C2": [
        #    "HTTP/1.1 404 Not Found Serve: Google Frontend Content-Length: 0 Keep-Alive: timeout=10, max=10 Connection:Keep-Alive Content-Type: text/plain",
            "ssl.cert.serial:146473198",
            "hash:-2007783223 port:50050",
            "product:'Cobalt Strike Beacon'"
        #    "ssl:foren.zik"
        ],
        #"Collector Stealer": [
        #    'http.html:"Collector Stealer"',
        #    'http.html:getmineteam',
        #    'product:"Collector Stealer"'
        #],
        "Covenant C2": [
        #    "ssl:Covenant http.component:Blazor",
        #    "http.favicon.hash:-737603591",
            "product:Covenant"
        ],
        "DarkComet Trojan": [
            "product:'DarkComet Trojan'"
        ],
        #"DarkTrack RAT Trojan": [
        #    "product:'DarkTrack RAT Trojan'"
        #],
        "DayBreak BAS": [
            "http.favicon.hash:991353327"
        ],
        "DcRAT": [
            "product:DcRat"
        ],
        #"Deimos C2": [
        #    "http.html_hash:-14029177",
        #    "product:'Deimos C2'"
        #],
        #"Doxerina Botnet": [
        #    "http.title:'Doxerina BotNet'"
        #],
        #"Empire C2": [
        #    "product:'Empire C2'"
        #],
        "Gh0st RAT Trojan": [
            "product:'Gh0st RAT Trojan'"
        ],
        "GoPhish": [
            "http.title:'Gophish - Login'",
        ],
        "Hak5 Cloud C2": [
            "product:'Hak5 Cloud C2'",
        #    "http.favicon.hash:1294130019"
        ],
        #"Hachcat": [
        #    "product:'Hachcat Cracking Tool'"
        #],
        "Havoc C2": [
            "X-Havoc: True",
        #    "product:Havoc"
        ],
        "Hookbot Trojan": [
            "http.title:'Hookbot Panel'"
        ],
        # https://twitter.com/g0njxa/status/1717563999984717991?t=rcVyVA2zwgJtHN5jz4wy7A&s=19
        #"Meduza Stealer": [
        #    "http.html_hash:1368396833",
        #    "http.title:'Meduza Stealer'"
        #],
        #"Misha Stealer": [
        #    "http.title:misha http.component:UIKit"
        #],
        "MobSF": [
            "http.title:'Mobile Security Framework - MobSF'"
        ],
        "Mozi Botnet": [
            "http.html_hash:-1245370368"
        ],
        #"Mystic Stealer": [
        #    "http.title:'Mystic Stealer'",
        #    "http.favicon.hash:-442056565"
        #],
        "Mythic C2": [
            "ssl:Mythic port:7443",
            "http.favicon.hash:-859291042",
        #    "product:Mythic"
        ],
        "NanoCore RAT Trojan": [
            "product:'NanoCore RAT Trojan'"
        ],
        "NetBus Trojan": [
            "product:'NetBus Trojan'"
        ],
        "NimPlant C2" : [
            "http.html_hash:-1258014549"
        ],
        "njRAT Trojan": [
            "product:'njRAT Trojan'"
        ],
        "Orcus RAT Trojan": [
            "product:'Orcus RAT Trojan'"
        ],
        #"Oyster C2": [
        #    "http.html_hash:-51903740"
        #],
        "PANDA C2":  [
            "http.html:PANDA http.html:layui",
            "product:'Panda C2'"
        ],
        "Pantegana C2": [
            "ssl:Pantegana ssl:localhost",
        #    "ssl.cert.issuer.cn:'Pantegana Root CA'"
        ],
        #"Patriot Stealer": [
        #    "http.favicon.hash:274603478",
        #    "http.html:patriotstealer"
        #],
        #"Poison Ivy Trojan": [
        #    "product:'Poison Ivy Trojan'"
        #],
        #"Poseidon C2": [
        #    "http.favicon.hash:219045137",
        #    "http.html_hash:-1139460879",
        #    "hash:799564296"
        #],
        "Posh C2": [
            "ssl:Pajfds ssl:P18055077",
        #    "product:PoshC2",
        #    # https://x.com/pedrinazziM/status/1808629285726400879
        #    "http.html_hash:855112502",
        #    "http.html_hash:-1700067737"
        ],
        #"Prysmax Stealer": [
        #    "http.title:'Prysmax Stealer'"
        #],
        "Quasar RAT": [
            "product:'Quasar RAT'"
        ],
        #"RAXNET Bitcoin Stealer": [
        #    "http.favicon.hash:-1236243965"
        #],
        "RedGuard C2": [
            "http.status:307 http:'307 Temporary Redirect Content-Type: text/html; charset=utf-8 Location: https://360.net'"
        ],
        "Remcos RAT": [
            "product:'Remcos Pro RAT Trojan'"
        ],
        #"RisePro Stealer": [
        #    "'Server: RisePro'"
        #],
        #"Scarab Botnet": [
        #    "http.title:'Scarab Botnet PANEL'"
        #],
         "Sectop RAT": [
            "http.headers_hash:-1731927497 port:9000,15647"
        ],
        "ShadowPad" : [
            "product:ShadowPad"
        ],
        "Sliver C2": [
        #    "ssl:multiplayer ssl.cert.issuer.cn:operators",
            '"HTTP/1.1 404 Not Found" "Cache-Control: no-store, no-cache, must-revalidate" "Content-Length: 0" -"Server:" -"Pragma:"',
        #    # https://twitter.com/Glacius_/status/1731699013873799209
            "product:'Sliver C2'"
        ],
        #"Spectre Stealer": [
        #    "http.title:'Spectre Stealer - Login'"
        #],
        #"SpiceRAT": [
        #    "http.headers_hash:1955818171 http.html_hash:114440660"
        #],
        #"SpyAgent": [
        #    "http.title:'SpY-Agent v1.2'"
        #],
        "Supershell C2": [
            "http.html_hash:84573275",
            "http.favicon.hash:-1010228102",
            "http.title:'Supershell - 登录'"
        ],
        #"Titan Stealer": [
        #    "http.html:'Titan Stealer'"
        #],
        "Unam Web Panel": [
            "html:unam_lib.js http.favicon.hash:-1278680098,-1531496738",
            "http.title:'Unam Web Panel &mdash; Login'"
        ],
        "Villain C2": [
            "hash:856668804"
        ],
        "Viper RAT": [
            "http.html_hash:-1250764086"
        ],
        #"Vshell C2": [
        #    "http.title:'Vshell - 登录'"
        #],
        "XMRig Monero Cryptominer": [
            "http.html:XMRig",
            "http.favicon.hash:-782317534",
            "http.favicon.hash:1088998712"
        ],
        "ZeroAccess Trojan": [
            "product:'ZeroAccess Trojan'"
        ]
    }

    # Load and validate any custom queries, then merge them in.
    queries = queries | load_custom_queries("shodan_queries.json")

    # TODO: Check for duplicate queries to avoid unncessary api calls.
    # TODO: Check for differnt queries for the same tool and merge into one.

    # Collect everything in memory FIRST, then write to disk. We do not delete
    # the existing data/ contents until we know the run actually produced
    # results, so a failed or empty Shodan run can never wipe the existing feed.
    results_by_product = {}
    ip_set_from_all_products = set()
    for product in queries:
        ip_set_from_product = set()
        for query in queries[product]:
            print(f"Product: {product}, Query: {query}")
            # Catch Shodan/network errors per query and move on to the next one,
            # rather than letting one bad query abort the whole run.
            # TODO: make it restart main() while keeping track of what was already documented
            try:
                for result in api.search_cursor(query):
                    ip = str(result["ip_str"])
                    ip_set_from_product.add(ip)
                    ip_set_from_all_products.add(ip)
            except exception.APIError as err:
                print(f"  Shodan API error for query '{query}': {err}")
                continue
            except Exception as err:
                print(f"  Unexpected error for query '{query}': {err}")
                continue
        if ip_set_from_product:
            results_by_product[product] = ip_set_from_product

    # Bail out without touching disk if the run produced nothing (auth failure,
    # exhausted query credits, API outage, etc.) so the existing feed survives.
    if not ip_set_from_all_products:
        print("No results collected; leaving existing data/ untouched.")
        return

    # Run succeeded: now clear out the old data and write the fresh results.
    # https://www.techiedelight.com/delete-all-files-directory-python/
    for file in os.scandir("data"):
        os.remove(file.path)

    # Write each product's list (sorted, so version-controlled diffs are stable).
    for product, ip_set_from_product in results_by_product.items():
        write_ips(f"data/{product} IPs.txt", ip_set_from_product)

    write_ips("data/all.txt", ip_set_from_all_products)

def deconflict():
    # Remove any duplicates from the files
    files = os.listdir("data/")
    for file in files:
        filepath = f"data/{file}"
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        if len(lines) != len(set(lines)):
            print(f"Deconflicting: {filepath}")
            write_ips(filepath, lines)

def main():
    load_dotenv()
    os.makedirs("data", exist_ok=True)
    shodan()
    deconflict()

if __name__ == '__main__':
    main()
