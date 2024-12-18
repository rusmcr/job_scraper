# Job Scraper Project

This project scrapes job listings from IamExpat.nl and sends email notifications with the latest job postings.

## Features
- Scrapes multiple pages of job listings.
- Compares new listings with existing ones.
- Saves listings to a CSV file.
- Sends email notifications.

## Setup Instructions

### 1. Clone this Repository
```bash
git clone https://github.com/rusmcr/job_scraper.git
cd job_scraper
```

### 2. Install Dependencies
Install the required Python libraries listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Set Up the `.env` File
Create a `.env` file in the root directory and add the following environment variables:
```
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
RECIPIENT_EMAIL=recipient@example.com
```
Replace `your_email@gmail.com` and `your_app_password` with your email credentials. Use an [App Password](https://support.google.com/accounts/answer/185833?hl=en) for better security.

### 4. Run the Scraper
Execute the scraper script:
```bash
python scraper.py
```

## Requirements
- **Python 3.7+**
- **Libraries**:
  - `beautifulsoup4`
  - `requests`
  - `yagmail`
  - `python-dotenv`

Install these libraries via `pip` using:
```bash
pip install -r requirements.txt
```

## How It Works
1. **Scraping**:
   - The scraper fetches job listings from the specified website (IamExpat.nl).
   - It processes multiple pages to collect job details like Title, Category, Location, and Link.

2. **Comparison**:
   - Compares the newly scraped jobs with the ones in the existing `jobs.csv` file.
   - Only new jobs are added to the CSV file.

3. **Email Notification**:
   - Sends an email to the specified recipient with a summary of the new job listings.
