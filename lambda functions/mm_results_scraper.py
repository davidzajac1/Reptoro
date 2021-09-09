from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from random import randint
import json, boto3, time
from scrapers import Scraper

def lambda_handler(event, context):

    s3 = boto3.client('s3')
    s = Scraper()

    result = []
    for page in range(event['start'],event['end']):

        time.sleep(randint(100,200)/100)

        for animal in s.results_page_scraper(event['sessionid'], event['min_price'], event['max_price'], page, retries=2):
            result.append(animal)

    filename = f"{event['scrapedate']} Pages {event['start']}-{event['end']} Prices {str(event['min_price'])}-{str(event['max_price'])}.json"
    filepath = f"/tmp/{filename}"

    with open(filepath, 'w') as f:
        for r in result:
            f.write(json.dumps(r))
            f.write("\n")

    s3.upload_file(filepath, 'morphmarkettemporary', f"raw_scraped_data/{filename}")

    return {'status': 200, 'count_to_error': 100}
