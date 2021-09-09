from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from random import randint
import json, boto3, time
from Results_Page import Results_Page


def lambda_handler(event, context):

    s3 = boto3.client('s3')

    count = 0
    result = []
    for page in range(event['start'],event['end']):

        time.sleep(randint(100,200)/100)

        try:
            for animal in Results_Page(page,event['min_price'],event['max_price']).scrape(event['sessionid']):
                result.append(animal)

        except Exception as e:
            print(f"{count} Pages until Error")
            print(e)
            return{'status':400, 'count_to_error':count}

        count = count + 1


    filename = f"{event['scrapedate']} Pages {event['start']}-{event['end']} Prices {str(event['min_price'])}-{str(event['max_price'])}.json"
    filepath = f"/tmp/{filename}"

    with open(filepath, 'w') as f:
        for r in result:
            f.write(json.dumps(r))
            f.write("\n")

    s3.upload_file(filepath, 'morphmarkettemporary', f"raw_scraped_data/{filename}")

    return {'status': 200, 'count_to_error': 100}
