# Python Standard Library Imports
import json
import os

# Third Party Imports
from dotenv import load_dotenv
from shodan import Shodan, exception
from censys.search import CensysHosts

def shodan():
    api_key = os.environ["SHODAN_API_KEY"].strip()
    api = Shodan(api_key)
    queries = {
        "AcidRain Stealer": [
            'http.html:"AcidRain Stealer"'
        ],
        "Brute Ratel C4": [
            "http.html_hash:-1957161625",
            "product:'Brute Ratel C4'"
        ],
        "Caldera C2": [
            'http.title:"Login | CALDERA"',
            # https://twitter.com/ViriBack/status/1713714868564394336
            "http.favicon.hash:-636718605",
            "http.html_hash:-1702274888"
        ],
        "Cobalt Strike C2": [
            "HTTP/1.1 404 Not Found Serve: Google Frontend Content-Length: 0 Keep-Alive: timeout=10, max=10 Connection:Keep-Alive Content-Type: text/plain",
            "ssl.cert.serial:146473198",
            "hash:-2007783223 port:50050",
            "product:'Cobalt Strike Beacon'"
            "ssl:foren.zik"
        ],
        "Collector Stealer": [
            'http.html:"Collector Stealer"',
            'http.html:getmineteam',
            'product:"Collector Stealer"'
        ],
        "Covenant C2": [
            "ssl:Covenant http.component:Blazor",
            "http.favicon.hash:-737603591",
            "product:Covenant"
        ],
        "DayBreak BAS": [
            "http.favicon.hash:991353327"
        ],
        "Deimos C2": [
            "http.html_hash:-14029177",
            "product:'Deimos C2'"
        ],
        "GoPhish": [
            "http.title:'Gophish - Login'",
        ],
        "Havoc C2": [
            "X-Havoc: True",
            "product:Havoc"
        ],
        # https://twitter.com/g0njxa/status/1717563999984717991?t=rcVyVA2zwgJtHN5jz4wy7A&s=19
        "Meduza Stealer": [
            "http.html_hash:1368396833",
            "http.title:'Meduza Stealer'"
        ],
        "Misha Stealer": [
            "http.title:misha http.component:UIKit"
        ],
        "Mystic Stealer": [
            "http.title:'Mystic Stealer'",
            "http.favicon.hash:-442056565"
        ],
        "Mythic C2": [
            "ssl:Mythic port:7443",
            "http.favicon.hash:-859291042",
            "product:Mythic"
        ],
        "NimPlant C2" : [
            "http.html_hash:-1258014549"
        ],
        "PANDA C2":  [
            "http.html:PANDA http.html:layui",
            "product:'Panda C2'"
        ],
        "Patriot Stealer": [
            "http.favicon.hash:274603478",
            "http.html:patriotstealer"
        ],
        "Posh C2": [
            "ssl:Pajfds ssl:P18055077",
            "product:PoshC2",
            # https://x.com/pedrinazziM/status/1808629285726400879
            "http.html_hash:855112502",
            "http.html_hash:-1700067737"
        ],
        "RAXNET Bitcoin Stealer": [
            "http.favicon.hash:-1236243965"
        ],
        "Sliver C2": [
            "ssl:multiplayer ssl.cert.issuer.cn:operators",
            '"HTTP/1.1 404 Not Found" "Cache-Control: no-store, no-cache, must-revalidate" "Content-Length: 0" -"Server:" -"Pragma:"',
            # https://twitter.com/Glacius_/status/1731699013873799209
            "product:'Sliver C2'"
        ],
        "Titan Stealer": [
            "http.html:'Titan Stealer'"
        ],
        "XMRig Monero Cryptominer": [
            "http.html:XMRig",
            "http.favicon.hash:-782317534",
            "http.favicon.hash:1088998712"
        ]
    }

    # Try and load custom queries from shodan_queries.json
    try:
        with open('shodan_queries.json', 'r') as file:
            custom_shodan_queries = json.load(file)

        # Merge the dictionaries of queries together
        queries = queries | custom_shodan_queries
    except:
        print("Either the shodan_queries.json file is empty or there is an error in the format.")

    # TODO: Check for duplicate queries to avoid unncessary api calls.
    # TODO: Check for differnt queries for the same tool and merge into one.

   # https://www.techiedelight.com/delete-all-files-directory-python/
    dir_to_clean = "data"
    for file in os.scandir(dir_to_clean):
        os.remove(file.path)

    ip_set_from_all_products = set()
    for product in queries:
        ip_set_from_product = set()
        product_ips_file = open(f"data/{product} IPs.txt", "a")
        for query in queries[product]:
            print(f"Product: {product}, Query: {query}")
            results = api.search_cursor(query)
            # Catch Shodan Query Errors and pass onto the next C2
            # TODO: make it restart main() while keeping track of what was already documented
            try:
                for result in results:
                    ip = str(result["ip_str"])
                    ip_set_from_product.add(ip)
                    ip_set_from_all_products.add(ip)
            except exception.APIError:
                continue
        for ip in ip_set_from_product:
            product_ips_file.write(f"{ip}\n")

    all_ips_file = open("data/all.txt", "a")
    for ip in ip_set_from_all_products:
        all_ips_file.write(f"{ip}\n")

def censys():
    queries = {
        "Poseidon C2": [
            "host.services.endpoints.http.html_title='POSEIDON'",
            "web.endpoints.http.html_title='POSEIDON'"
        ]
    }

    # Try and load custom queries from censys_queries.json
    try:
        with open('censys_queries.json', 'r') as file:
            custom_censys_queries = json.load(file)

        # Merge the dictionaires of queries together
        queries = queries | custom_censys_queries
    except:
        print("Either the censys_queries.json file is empty or there is an error in the format.")

    # TODO: Check for duplicate queries to avoid unnecessary api calls.
    # TODO: Check for different queries for the same tool and merge into one.

    h = CensysHosts()
    all_ips = set()
    for product in queries:
        ips = set()
        product_ips_file = open(f"data/{product} IPs.txt", "a")
        for search_string in queries[product]:
            print(f"Product: {product}, Query: {search_string}")
            query = h.search(search_string)
            results = None
            try:
                results = query()
            except Exception as err:
                print(err)
                continue
            for host in results:
                ip = str(host['ip'])
                all_ips.add(ip)
                ips.add(ip)
        for ip in ips:
            product_ips_file.write(f"{ip}\n")
    all_ips_file = open("data/all.txt", "a")
    for ip in all_ips:
        all_ips_file.write(f"{ip}\n")

def deconflict():
    # Remove any duplicates from the files
    files = os.listdir("data/")
    for file in files:
        filepath = f"data/{file}"
        f = open(filepath, "r")
        lines = f.readlines()
        f.close()
        if len(lines) != len(set(lines)):
            print(f"Deconflicting: {filepath}")
            os.remove(filepath)
            f = open(filepath, "a")
            for line in set(lines):
                f.write(line)
            f.close()

def main():
    load_dotenv()
    shodan()
    #censys()
    deconflict()

if __name__ == '__main__':
    main()
