import requests
from bs4 import BeautifulSoup
import csv
import os
import yagmail
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create necessary directories
if not os.path.exists("logs"):
    os.makedirs("logs")

if not os.path.exists("data"):
    os.makedirs("data")

# Configure logging
logging.basicConfig(
    filename="logs/job_scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def scrape_jobs(base_url, max_pages=3):
    """
    Scrapes job data from multiple pages of the given URL.

    Args:
        base_url (str): The base URL of the job listings page.
        max_pages (int): Maximum number of pages to scrape.

    Returns:
        list: A list of dictionaries, each containing job details.
    """
    jobs = []

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}  # Prevent blocking by servers

        for page in range(1, max_pages + 1):
            url = f"{base_url}?page={page}"
            logging.info(f"Scraping page: {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all job listing elements
            for job in soup.find_all('div', class_='box-job-info'):
                title_elem = job.find('h2', class_='article__title')
                category_elem = job.find('span', class_='article__category')
                location_elem = job.find('span', class_='article__info')
                link_elem = job.find('a', class_='article__link')

                title = title_elem.text.strip() if title_elem else 'N/A'
                category = category_elem.text.strip() if category_elem else 'N/A'
                location = location_elem.text.strip() if location_elem else 'N/A'
                link = link_elem['href'] if link_elem else 'N/A'
                if link and not link.startswith('http'):
                    link = 'https://www.iamexpat.nl' + link

                jobs.append({
                    'Title': title,
                    'Category': category,
                    'Location': location,
                    'Link': link
                })
    except Exception as e:
        logging.error(f"Error while scraping jobs: {e}")

    return jobs

def save_to_csv(jobs, filename="data/jobs.csv"):
    """
    Saves a list of job dictionaries to a CSV file.

    Args:
        jobs (list): List of job dictionaries to save.
        filename (str): Name of the CSV file.
    """
    try:
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Title', 'Category', 'Location', 'Link'])
            if not file_exists:
                writer.writeheader()
            writer.writerows(jobs)
        logging.info(f"Saved {len(jobs)} jobs to {filename}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")

def compare_and_save_new_jobs(new_jobs, filename="data/jobs.csv", recipient_email="recipient@example.com"):
    """
    Compare new jobs with existing jobs and save only the new ones.

    Args:
        new_jobs (list): List of new job dictionaries to compare.
        filename (str): Name of the CSV file.
        recipient_email (str): Email address to send notifications to.
    """
    existing_jobs = set()

    # Read existing jobs if the file exists
    if os.path.isfile(filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_jobs.add(row['Link'])

    # Filter out jobs that already exist
    unique_jobs = [job for job in new_jobs if job['Link'] not in existing_jobs]

    if unique_jobs:
        save_to_csv(unique_jobs, filename)
        logging.info(f"Added {len(unique_jobs)} new jobs.")
        send_email_notification(unique_jobs, recipient_email)
    else:
        logging.info("No new jobs found.")

def send_email_notification(new_jobs, recipient_email):
    """
    Sends an email with the new job listings.

    Args:
        new_jobs (list): List of new job dictionaries.
        recipient_email (str): Email address to send notifications to.
    """
    try:
        sender_email = os.getenv("EMAIL_USER", "your_email@gmail.com")
        app_password = os.getenv("EMAIL_PASS", "your_app_password")
        subject = "New Job Listings Available!"
        body = "Here are the new job listings:\n\n"
        for job in new_jobs:
            body += f"Title: {job['Title']}\nCategory: {job['Category']}\nLocation: {job['Location']}\nLink: {job['Link']}\n\n"

        yag = yagmail.SMTP(user=sender_email, password=app_password)
        yag.send(to=recipient_email, subject=subject, contents=body)
        logging.info(f"Email sent to {recipient_email}")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

if __name__ == "__main__":
    BASE_URL = "https://www.iamexpat.nl/career/jobs-netherlands/amsterdam"
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "recipient@example.com")
    job_listings = scrape_jobs(BASE_URL, max_pages=3)
    compare_and_save_new_jobs(job_listings, recipient_email=RECIPIENT_EMAIL)
