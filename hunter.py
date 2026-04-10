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
            "Covenant C2": [
                "ssl:Covenant http.component:Blazor",
                "http.favicon.hash:-737603591",
                "product:Covenant"
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
