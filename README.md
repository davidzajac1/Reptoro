# Reptoro
### A Data Visualization and Analytics Platform for the Reptile Industry

Most billion dollar industries have many large corporations who employ full-time business analysts to crunch numbers and analyze data, making prices and margins competitive.

The exotic reptile trade is a rare exception, with only a handful of medium sized players and with the majority of the industry being comprised of “Mom and Pop” operations there are potentially undiscovered high margin opportunities. These animals frequently sell for four and even five figures but live inside an enclosure the size of a shoe box.

Reptoro is the first and only data visualization and analytics platform specific to the Exotic Reptile Industry.

### How it Works

Reptoro continuously webscrapes industry marketplaces, adding new animals and breeders to our database as well as tracking price and status changes to existing listings.

Below is a flowchart of our cloud-based tech stack and ETL pipeline. Apache Airflow is used to schedule and orchestrate periodic webscrapes using AWS Lambda Functions to request and parse data.

Data is dumped into an AWS S3 bucket where it is cleaned and transformed using AWS. After the scrape is over a Lambda Function updates our PostgreSQL database.

Our website [Reptoro.com](https://www.reptoro.com) is hosted on an AWS EC2 instance, runs on a Flask framework and utilizes Dash and Plotly open source Python libraries to interactively display data on our dashboards.

![alt text](/flowchart.JPG)

### ETL Pipeline

Below you'll see a flowchart of our ETL Pipeline from the Apache Airflow GUI. All long tasks in the pipeline are conducted at 10x concurrency using Boto3 to trigger multiple Lambda Functions at the same time.

In the first step a Chrome Browser is rendered in the Lambda Function using Selenium to interact with the website, login to an account and extract the Session ID so that it can be passed in to other Lambda Functions to access login-required data.

After the login Session ID's are extracted, they are passed down the pipeline and more Lambda Functions scrape all search results pages. The URLs are queried against our PostgreSQL database to check for listings that are not already in the database.

The new listings are then scraped and entered into the database, the same process is completed for all sellers profiles.

![alt text](/airflow_chart.JPG)


### Web App

Reptoro is hosted on an AWS EC2 instance using AWS ElasticBeanstalk to auto-scale and provision resources, so that the website will still function during an influx of requests.

The Web Application is written in Python using Flask and Jinja2 in tandem with a Bootstrap template to quickly build a beautiful dynamic user interface.

Our dashboards are built using Dash, an open-source Python library that contains pre-built visualizations made using React JS. This library allowed us to pass in Pandas Dataframes into the Dash framework and quickly yield interactive 2D and 3D visualizations.

![alt text](/dashboard.JPG)
