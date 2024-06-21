import requests
from bs4 import BeautifulSoup
import csv
import json

# Send a GET request
url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation='
response = requests.get(url)

# If the GET request is successful, the status code will be 200
if response.status_code == 200:
    # Get the content of the response
    page_content = response.content

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(page_content, 'lxml')

    # Find all job listings
    job_listings = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    # Create lists to store job data
    job_titles = []
    company_names = []
    job_locations = []
    job_descriptions = []

    # Extract job data
    for job in job_listings:
        job_title = job.find('h2').text.strip()
        company_name = job.find('h3').text.strip()
        job_location = job.find('ul', class_='top-jd-dtl clearfix').find('li').text.strip()
        job_description = job.find('ul', class_='list-job-dtl').text.strip()

        job_titles.append(job_title)
        company_names.append(company_name)
        job_locations.append(job_location)
        job_descriptions.append(job_description)

    # Create a dictionary to store job data
    job_data = {
        'Job Title': job_titles,
        'Company Name': company_names,
        'Job Location': job_locations,
        'Job Description': job_descriptions
    }

    # Save job data to a CSV file
    with open('job_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(job_data.keys())
        writer.writerows(zip(*job_data.values()))

    # Save job data to a JSON file
    with open('job_data.json', 'w') as file:
        json.dump(job_data, file, indent=4)

else:
    print('Failed to retrieve page')