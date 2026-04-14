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
        #    '"HTTP/1.1 404 Not Found" "Cache-Control: no-store, no-cache, must-revalidate" "Content-Length: 0" -"Server:" -"Pragma:"',
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
        #"Viper RAT": [
        #    "http.html_hash:-1250764086"
        #],
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
