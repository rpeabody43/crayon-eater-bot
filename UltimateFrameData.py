import requests
import pprint

URL = "https://ultimateframedata.com/falco.php"
page = requests.get(URL)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(page.content)