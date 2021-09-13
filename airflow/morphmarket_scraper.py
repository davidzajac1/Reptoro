from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
import boto3, json, botocore, time
import json
import botocore
import time


SCRAPEDATE = datetime.now().strftime("%Y-%m-%d")
AWSKEY = Variable.get('AWSKEY')
AWSSECRETKEY = Variable.get('AWSSECRETKEY')
MMUSER = Variable.get('MMUSER')
MMPASS = Variable.get('MMPASS')
CONNECTIONSTRING = Variable.get('CONNECTIONSTRING')
EMAIL = Variable.get('EMAIL')

#Configuring botocore to communicate with AWS
config = botocore.config.Config(
    read_timeout=7200,
    connect_timeout=7200,
    retries={"max_attempts": 2}
)

session = botocore.session.Session()

#Creating a session to communicate with AWS Lambda
lambdaclient = session.create_client('lambda', region_name='us-east-2'
, aws_access_key_id =AWSKEY
, aws_secret_access_key=AWSSECRETKEY
,config=config)

#Creating a session to communicate with AWS Athena
athenaclient = session.create_client('athena', region_name='us-east-2'
, aws_access_key_id =AWSKEY
, aws_secret_access_key=AWSSECRETKEY
,config=config)

#The price intervals the scraper will be split into
price_intervals = [(0,80), (81,140), (141,180)
, (181,240), (241, 290), (291, 350), (351, 480)
, (481, 650), (651, 1200), (1201, 0)]


#Logs into a MM account and gets the sessionid from the cookies
def invoke_session_ids(ti, user, passw, interval):

    event = {
      "user": user,
      "pass": passw,
      "min_price": price_intervals[interval][0],
      "max_price": price_intervals[interval][1]
    }
    payload = json.dumps(event, indent=2).encode('utf-8')

    response = lambdaclient.invoke(
        FunctionName='arn:aws:lambda:us-east-2:967068097097:function:get_sessionid',
        LogType='None',
        Payload=payload
    )

    payload = json.loads(response['Payload'].read())
    sessionid = payload['sessionid']
    num_pages = payload['num_pages']

    ti.xcom_push(key='sessionid', value=(sessionid,num_pages))


#Uses lambda functions to scrape the search results pages
def invoke_results_scraper(ti, interval):

    sessionid_and_pages = ti.xcom_pull(key='sessionid', task_ids=f"get_login_cookies_{interval}")
    sessionid, total_pages = sessionid_and_pages[0], sessionid_and_pages[1]

    scraping_intervals = []
    for x in range(1,total_pages,100):
        if x + 100 <= total_pages:
            scraping_intervals.append((x, x + 100))
        else:
            scraping_intervals.append((x, total_pages))

    for tuple in scraping_intervals:

        event = {
          "sessionid": sessionid,
          "start": tuple[0],
          "end": tuple[1],
          "scrapedate": SCRAPEDATE,
          "min_price": price_intervals[interval][0],
          "max_price": price_intervals[interval][1]
        }
        payload = json.dumps(event, indent=2).encode('utf-8')

        response = lambdaclient.invoke(
            FunctionName='arn:aws:lambda:us-east-2:967068097097:function:mm_results_scraper',
            InvocationType='Event',
            LogType='None',
            Payload=payload
        )

        time.sleep(700)

#Checks if the session ids and number of pages are the correct format before initiating scrapers
def check_sessionid_num_pages(ti):

    sessionids = ti.xcom_pull(key='sessionid', task_ids=['get_login_cookies_0','get_login_cookies_1'
    ,'get_login_cookies_2','get_login_cookies_3','get_login_cookies_4','get_login_cookies_5'
    ,'get_login_cookies_6','get_login_cookies_7','get_login_cookies_8','get_login_cookies_9'])

    if len(sessionids) < 10:
        raise Exception(f"Only {len(sessionids)} Session IDs")
    for sesh in sessionids:
        if (isinstance(sesh[0],str) == False) or (len(sesh[0]) < 20):
            raise Exception("Session ID not correct format")
        if sesh[1] < 500:
            raise Exception("Not enough results in interval")

#Queries AWS Athena to check which of the URLs are not in the database already
def get_unscraped_urls(ti):

    response = athenaclient.start_query_execution(
        QueryString=f"""INSERT INTO AwsDataCatalog.morphmarkets3.mm_animal_updates
                        (SELECT DISTINCT '{SCRAPEDATE}' AS date, * FROM AwsDataCatalog.morphmarkets3.raw_results
                        WHERE url IS NOT NULL AND status IS NOT NULL AND price IS NOT NULL);""",
        ResultConfiguration={'OutputLocation': 's3://morphmarkettemporary/AthenaQuery/'}
        )

    QueryExecutionId = response['QueryExecutionId']

    for _ in range(0,10):

        time.sleep(20)

        query_status = athenaclient.get_query_execution(QueryExecutionId=QueryExecutionId)
        query_status = query_status['QueryExecution']['Status']['State']

        if query_status == 'SUCCEEDED':
            break
        elif (query_status == 'FAILED') or (query_status == 'CANCELLED'):
            raise Exception("Athena Query 'appending cleaned results'failed")




    response = athenaclient.start_query_execution(
        QueryString=f"""SELECT count(AwsDataCatalog.morphmarkets3.mm_animal_updates.url) AS num_not_in_master
                        FROM AwsDataCatalog.morphmarkets3.mm_animal_updates
                        WHERE url
                        NOT IN (SELECT url FROM davidpersonal.morphmarket.master)
                        AND date = '{SCRAPEDATE}';""",
        ResultConfiguration={'OutputLocation': 's3://morphmarkettemporary/AthenaQuery/'}
        )

    QueryExecutionId = response['QueryExecutionId']

    for _ in range(0,10):

        time.sleep(20)

        query_status = athenaclient.get_query_execution(QueryExecutionId=QueryExecutionId)
        query_status = query_status['QueryExecution']['Status']['State']

        if query_status == 'SUCCEEDED':
            break
        elif (query_status == 'FAILED') or (query_status == 'CANCELLED'):
            raise Exception("Athena Query 'num_not_in_master' failed")

    results = athenaclient.get_query_results(QueryExecutionId=QueryExecutionId)

    num_not_in_master = int(results['ResultSet']['Rows'][1]['Data'][0]['VarCharValue'])


    response = athenaclient.start_query_execution(
        QueryString=f"""INSERT INTO morphmarkets3.unscraped_urls
                        (SELECT row_number() over () as row_num, url FROM
                        (SELECT AwsDataCatalog.morphmarkets3.mm_animal_updates.url
                        FROM AwsDataCatalog.morphmarkets3.mm_animal_updates
                        WHERE url
                        NOT IN (SELECT url FROM davidpersonal.morphmarket.master)
                        AND date = '{SCRAPEDATE}'));""",
        ResultConfiguration={'OutputLocation': 's3://morphmarkettemporary/AthenaQuery/'}
        )

    QueryExecutionId = response['QueryExecutionId']

    for _ in range(0,10):

        time.sleep(20)

        query_status = athenaclient.get_query_execution(QueryExecutionId=QueryExecutionId)
        query_status = query_status['QueryExecution']['Status']['State']

        if query_status == 'SUCCEEDED':
            break
        elif (query_status == 'FAILED') or (query_status == 'CANCELLED'):
            raise Exception("Athena Query 'urls_not_in_master' failed")

    ti.xcom_push(key='num_not_in_master', value=num_not_in_master)

#Uses lambda to scrape the indvidual pages if they have not already been scraped
def invoke_entry_scraper(ti, interval):


    sessionid = ti.xcom_pull(key='sessionid', task_ids=f"get_login_cookies_{interval}")[0]
    total_pages = ti.xcom_pull(key='num_not_in_master', task_ids='query_unscraped_urls')

    for x in range(0,10):
        start = x * int(total_pages/10) + 1
        end = (x + 1) * int(total_pages / 10)

        if x == 9: end = total_pages

        if x == interval: break

    scraping_intervals = []
    for x in range(start,end,100):
        if x + 100 <= end:
            scraping_intervals.append((x, x + 99))
        else:
            scraping_intervals.append((x, end))

    for tuple in scraping_intervals:

        event = {
          "sessionid": sessionid,
          "start": tuple[0],
          "end": tuple[1],
          "AWSKEY": AWSKEY,
          "AWSSECRETKEY": AWSSECRETKEY,
          "con": CONNECTIONSTRING,
          "scrape_date": SCRAPEDATE
        }
        payload = json.dumps(event, indent=2).encode('utf-8')

        response = lambdaclient.invoke(
            FunctionName='arn:aws:lambda:us-east-2:967068097097:function:morphmarket_scraper',
            InvocationType='Event',
            LogType='None',
            Payload=payload
        )

        time.sleep(750)

#Queries AWS Athena to check which of the Breeder URLs are not in the database already
def get_unscraped_breeder_urls(ti):

    response = athenaclient.start_query_execution(
        QueryString=f"""SELECT COUNT(DISTINCT breeder_url) AS num_not_in_sellers
                        FROM davidpersonal.morphmarket.master WHERE
                        breeder_url NOT IN
                        (SELECT breeder_url FROM davidpersonal.morphmarket.sellers);""",
        ResultConfiguration={'OutputLocation': 's3://morphmarkettemporary/AthenaQuery/'}
        )

    QueryExecutionId = response['QueryExecutionId']

    for _ in range(0,10):

        time.sleep(20)

        query_status = athenaclient.get_query_execution(QueryExecutionId=QueryExecutionId)
        query_status = query_status['QueryExecution']['Status']['State']

        if query_status == 'SUCCEEDED':
            break
        elif (query_status == 'FAILED') or (query_status == 'CANCELLED'):
            raise Exception("Athena Query 'num_not_in_sellers' failed")

    results = athenaclient.get_query_results(QueryExecutionId=QueryExecutionId)

    num_not_in_sellers = int(results['ResultSet']['Rows'][1]['Data'][0]['VarCharValue'])


    response = athenaclient.start_query_execution(
        QueryString=f"""INSERT INTO morphmarkets3.unscraped_breeder_urls
                        (SELECT row_number() over () as row_num, breeder_url FROM
                        (SELECT DISTINCT breeder_url AS breeder_url FROM davidpersonal.morphmarket.master WHERE
                        breeder_url NOT IN (SELECT breeder_url FROM davidpersonal.morphmarket.sellers)));""",
        ResultConfiguration={'OutputLocation': 's3://morphmarkettemporary/AthenaQuery/'}
        )

    QueryExecutionId = response['QueryExecutionId']

    for _ in range(0,10):

        time.sleep(20)

        query_status = athenaclient.get_query_execution(QueryExecutionId=QueryExecutionId)
        query_status = query_status['QueryExecution']['Status']['State']

        if query_status == 'SUCCEEDED':
            break
        elif (query_status == 'FAILED') or (query_status == 'CANCELLED'):
            raise Exception("Athena Query 'breeder_urls_not_in_master' failed")


    ti.xcom_push(key='num_not_in_sellers', value=num_not_in_sellers)


#Uses lambda to scrape the indvidual seller pages if they have not already been scraped
def invoke_seller_scraper(ti, interval):

    total_pages = ti.xcom_pull(key='num_not_in_sellers', task_ids='query_unscraped_breeder_urls')

    for x in range(0,10):
        start = x * int(total_pages/10) + 1
        end = (x + 1) * int(total_pages / 10)

        if x == 9: end = total_pages

        if x == interval: break

    scraping_intervals = []
    for x in range(start,end,100):
        if x + 100 <= end:
            scraping_intervals.append((x, x + 99))
        else:
            scraping_intervals.append((x, end))

    for tuple in scraping_intervals:

        event = {
          "start": tuple[0],
          "end": tuple[1],
          "AWSKEY": AWSKEY,
          "AWSSECRETKEY": AWSSECRETKEY,
          "con": CONNECTIONSTRING,
          "SCRAPEDATE": SCRAPEDATE
        }
        payload = json.dumps(event, indent=2).encode('utf-8')

        response = lambdaclient.invoke(
            FunctionName='arn:aws:lambda:us-east-2:967068097097:function:seller_scraper',
            InvocationType='Event',
            LogType='None',
            Payload=payload
        )

        time.sleep(750)

#Empties the AWS S3 bucket of the temporary athena tables created
def empty_buckets():

    s3client = session.create_client('s3', region_name='us-east-2'
    , aws_access_key_id =AWSKEY
    , aws_secret_access_key=AWSSECRETKEY
    ,config=config)

    for folder in ('raw_scraped_data/', 'unscraped_urls/', 'unscraped_breeder_urls/'):

        response = s3client.list_objects_v2(Bucket='morphmarkettemporary', Prefix=folder)

        for object in response['Contents'][1:]:

            s3client.delete_object(Bucket='morphmarkettemporary', Key=object['Key'])



with DAG(
    dag_id = 'morphmarket_scraper',
    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2021, 9, 14),
        'email': [EMAIL],
        'email_on_failure': True,
        'retries': 0,
        'schedule_interval': '@weekly'
    }
    ) as dag:


    get_session_ids = []
    for interval in range(0,10):
        task = PythonOperator(
            task_id='get_login_cookies_' + str(interval),
            python_callable=invoke_session_ids,
            op_kwargs = {'user':MMUSER.split('@')[0] + str(interval) + '@' + MMUSER.split('@')[1], 'passw':MMPASS, 'interval': interval}
        )

        get_session_ids.append(task)


    check_cookies = PythonOperator(
        task_id='check_cookies',
        python_callable=check_sessionid_num_pages
    )


    scrape_result_pages = []
    for interval in range(0,10):
        task = PythonOperator(
            task_id='scrape_results_pages_' + str(interval),
            python_callable=invoke_results_scraper,
            op_kwargs = {'interval': interval}
        )

        scrape_result_pages.append(task)


    query_unscraped_urls = PythonOperator(
        task_id='query_unscraped_urls',
        python_callable=get_unscraped_urls
    )

    scrape_new_pages = []
    for interval in range(0,10):
        task = PythonOperator(
            task_id='scrape_new_pages_' + str(interval),
            python_callable=invoke_entry_scraper,
            op_kwargs = {'interval': interval}
        )
        scrape_new_pages.append(task)


    query_unscraped_breeder_urls = PythonOperator(
        task_id='query_unscraped_breeder_urls',
        python_callable=get_unscraped_breeder_urls
    )


    scrape_new_seller_pages = []
    for interval in range(0,10):
        task = PythonOperator(
            task_id='scrape_new_seller_pages_' + str(interval),
            python_callable=invoke_seller_scraper,
            op_kwargs = {'interval': interval}
        )
        scrape_new_seller_pages.append(task)


    empty_s3_buckets = PythonOperator(
        task_id='empty_s3_buckets',
        python_callable=empty_buckets
    )

    get_session_ids >> check_cookies >> scrape_result_pages >> query_unscraped_urls >> scrape_new_pages >> query_unscraped_breeder_urls >> scrape_new_seller_pages >> empty_s3_buckets
