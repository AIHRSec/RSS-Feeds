## This script should be complete
## There might be minor changes in the future

# Placeholder
#[email]
#smtp_server = smtp.gmail.com
#smtp_port = 587
#sender_email = sender@gmail.com
#recipient_email = receiver@gmail.com
#password = password

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dateutil import parser, tz
from datetime import datetime, timedelta
import configparser
import smtplib
import feedparser
import requests
import csv

def fetch_csv_raw_data_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch CSV data. Status code: {response.status_code}")
        return None

github_raw_url = 'https://raw.githubusercontent.com/AIHRSec/RSS-Feeds/main/RSSFeeds.csv'
raw_data = fetch_csv_raw_data_from_github(github_raw_url)
urls = []

if raw_data:
    url_list = [url.strip() for url in raw_data.split(',') if url.strip()]
    urls = url_list

# Get time and date variables
current_time = datetime.now(tz.tzutc())
current_date = datetime.now().strftime("%Y-%m-%d")

# Calculate the datetime 24 hours ago in UTC timezone
twenty_four_hours_ago = current_time - timedelta(hours=24)

# Define a function to handle unknown timezones - probably could be lower
def custom_tzinfos(abbreviation, offset):
    if abbreviation == "EST":
        return tz.gettz("America/New_York")
    elif abbreviation == "EDT":
        return tz.gettz("America/New_York")
    elif abbreviation == "PST":
        return tz.gettz("America/Los_Angeles")
    elif abbreviation == "PDT":
        return tz.gettz("America/Los_Angeles")
    elif abbreviation == "MST":
        return tz.gettz("America/Denver")
    elif abbreviation == "MDT":
        return tz.gettz("America/Denver")
    elif abbreviation == "CST":
        return tz.gettz("America/Chicago")
    elif abbreviation == "CDT":
        return tz.gettz("America/Chicago")
    elif abbreviation == "BST":
        return tz.gettz("Europe/London")
    elif abbreviation == "CET":
        return tz.gettz("Europe/Paris")
    elif abbreviation == "CEST":
        return tz.gettz("Europe/Paris")
    elif abbreviation == "AEST":
        return tz.gettz("Australia/Sydney")
    elif abbreviation == "AEDT":
        return tz.gettz("Australia/Sydney")
    elif abbreviation == "JST":
        return tz.gettz("Asia/Tokyo")
    elif abbreviation == "IST":
        return tz.gettz("Asia/Kolkata")
    elif abbreviation == "GMT":
        return tz.gettz("GMT")
    elif abbreviation == "UTC":
        return tz.gettz("UTC")

# Variables for files
ti_data = (current_date + "_ti.csv")
report_data = (current_date + "_report.csv")
data_fieldnames = ["Title", "Date", "Link"]
report_fieldnames = ["Feed_Name", "Number_of_Entries", "Number_of_Recent_Posts"]
subject_name = (current_date + "- TI Report")

# Creating the TI CSV
with open(ti_data, "w", newline='') as data_csv_file:
    data_writer = csv.DictWriter(data_csv_file, fieldnames=data_fieldnames)
    data_writer.writeheader()

    # Creating the report CSV 
    with open(report_data, "w", newline='') as report_csv_file:
        report_writer = csv.DictWriter(report_csv_file, fieldnames=report_fieldnames)
        report_writer.writeheader()

        for feed_url in urls:
            # Parse the RSS feed
            feed = feedparser.parse(feed_url)
            # Check if any entry lacks the 'published' field (for troubleshooting)
            missing_published_field = any('published' not in entry for entry in feed.entries)

            if missing_published_field:
                #print("This feed does not have the 'published' field for some entries.") # Could probably get rid of this line or add more to it
                continue

            # Filter the entries to include only those within the last 24 hours
            filtered_entries = [entry for entry in feed.entries if parser.parse(entry.published, tzinfos=custom_tzinfos).astimezone(tz.tzutc()) >= twenty_four_hours_ago]

            # Adding data to report CSV
            report_writer.writerow({'Feed_Name': feed_url,'Number_of_Entries': len(feed.entries), 'Number_of_Recent_Posts': len(filtered_entries)})
            
            for entry in filtered_entries:
                data_writer.writerow({'Title': entry.title, 'Date': entry.published, 'Link': entry.link})

# Load email configuration from the config file
config = configparser.ConfigParser()
config.read("config.ini")

smtp_server = config["email"]["smtp_server"]
smtp_port = int(config["email"]["smtp_port"])
sender_email = config["email"]["sender_email"]
recipient_email = config["email"]["recipient_email"]
password = config["email"]["password"]

# Create a multipart message
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = recipient_email
message['Subject'] = subject_name

# Add message body
body = ("This is the report for " + current_date)
message.attach(MIMEText(body, 'plain'))

# Attach ti_data
with open(ti_data, "rb") as file:
    part = MIMEApplication(file.read(), Name=ti_data)
part['Content-Disposition'] = f'attachment; filename="{ti_data}"'
message.attach(part)

# Attach report_data
with open(report_data, "rb") as file:
    part = MIMEApplication(file.read(), Name=report_data)
part['Content-Disposition'] = f'attachment; filename="{report_data}"'
message.attach(part)

# Connect to the SMTP server
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Start TLS encryption
    # Login to the SMTP server
    server.login(sender_email, password)
    # Send email
    server.send_message(message)
    print("Email sent successfully")
