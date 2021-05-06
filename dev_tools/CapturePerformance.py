import json
import pprint
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

capabilities = DesiredCapabilities.CHROME
# capabilities["loggingPrefs"] = {"performance": "ALL"}  # chromedriver < ~75
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

driver = webdriver.Chrome(
    ChromeDriverManager().install(),
    desired_capabilities=capabilities,
)


def process_browser_logs_for_network_events(logs):
    """
    Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
    since we're interested in the network events specifically.
    """
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
                "Network.response" in log["method"]
                or "Network.request" in log["method"]
                or "Network.webSocket" in log["method"]
        ):
            yield log


driver.get("https://www.rkengler.com")

logs = driver.get_log("performance")

events = process_browser_logs_for_network_events(logs)
with open("log_entries.txt", "wt") as out:
    for event in events:
        pprint.pprint(event, stream=out)


driver.get_log()

driver.get("https://www.salesforce.com")

logs = driver.get_log("performance")

events = process_browser_logs_for_network_events(logs)
with open("log_salesforce.txt", "wt") as out:
    for event in events:
        pprint.pprint(event, stream=out)