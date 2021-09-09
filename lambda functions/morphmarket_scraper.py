from urllib.request import Request, urlopen
from Animal import Animal
from random import randint
import pandas as pd
import psycopg2, json, time, boto3, botocore


def lambda_handler(event, context):

    config = botocore.config.Config(
    read_timeout=900,
    connect_timeout=900,
    retries={"max_attempts": 2}
    )

    session = botocore.session.Session()

    athenaclient = session.create_client('athena', region_name='us-east-2'
    , aws_access_key_id = event['AWSKEY']
    , aws_secret_access_key= event['AWSSECRETKEY']
    ,config=config)


    response = athenaclient.start_query_execution(
        QueryString=f"""SELECT url FROM AwsDataCatalog.morphmarkets3.unscraped_urls WHERE row_num BETWEEN {event['start']} and {event['end']};""",
        ResultConfiguration={'OutputLocation': 's3://morphmarkettemporary/AthenaQuery/'}
        )

    QueryExecutionId = response['QueryExecutionId']

    for _ in range(0,10):

        time.sleep(10)

        query_status = athenaclient.get_query_execution(QueryExecutionId=QueryExecutionId)
        query_status = query_status['QueryExecution']['Status']['State']

        if query_status == 'SUCCEEDED':
            break
        elif (query_status == 'FAILED') or (query_status == 'CANCELLED'):
            raise Exception("Athena Query failed")

    results = athenaclient.get_query_results(QueryExecutionId=QueryExecutionId)


    urls = []
    for row in results['ResultSet']['Rows']:
        urls.append(row['Data'][0]['VarCharValue'])

    urls.pop(0)

    errors = 0
    df = pd.DataFrame()
    for url in urls:
        try:
            df = df.append(Animal(f"https://www.morphmarket.com{url}").scrape(event['sessionid'], event['scrape_date']), ignore_index=True)
            time.sleep(randint(150,250)/100)
        except Exception as e:
            errors = errors + 1
            print(e)
            print(url)
            time.sleep(2)
            try:
                df = df.append(Animal(f"https://www.morphmarket.com{url}").scrape(event['sessionid'], event['scrape_date']), ignore_index=True)

            except Exception as e:
                errors = errors + 1
                print(e)


    df.to_sql('master', con=event['con'], schema='morphmarket', if_exists='append', index=False)


    return {'errors': f"{errors} Errors"}
