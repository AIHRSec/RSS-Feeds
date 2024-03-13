## This script is still in development and it only partial working.
## There are plans to complete the rest of the script.

import feedparser
from datetime import datetime, timedelta
from dateutil import parser, tz

urls = [
    "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?max=10&ContentType=1&Site=945","https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=2&Site=945&max=10","https://msrc.microsoft.com/blog/categories/msrc/feed","https://msrc.microsoft.com/blog/feed","https://www.cisa.gov/cisa/blog.xml","https://www.cisa.gov/news.xml","https://www.cisa.gov/ncas/alerts.xml","https://exploitalert.com/feed","https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml","https://www.ncsc.gov.uk/api/1/services/v1/blog-post-rss-feed.xml","https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml","https://www.cshub.com/rss/news","https://www.cshub.com/rss/news-trends","https://www.cshub.com/rss/categories/cloud","https://www.cshub.com/rss/categories/attacks","https://www.bleepingcomputer.com/feed/","https://www.wiz.io/feed/rss.xml","https://www.microsoft.com/en-us/security/blog/feed/","https://fetchrss.com/rss/65b0eb775582bd1c19083c4365b0fdb664898a0daa63bef4.xml","https://www.govinfosecurity.com/rss-feeds","https://www.mandiant.com/resources/blog/rss.xml","https://www.crowdstrike.com/blog/feed","https://newsroom.trendmicro.com/news-releases?pagetemplate=rss&category=787","https://newsroom.trendmicro.com/cyberthreat?pagetemplate=rss","https://blog.talosintelligence.com/rss/","https://isc.sans.edu/rssfeed.xml"
    # Add more URLs if needed
]

# Get the current time in UTC timezone
current_time = datetime.now(tz.tzutc())

# Calculate the datetime 24 hours ago in UTC timezone
twenty_four_hours_ago = current_time - timedelta(hours=72)

# Define a function to handle unknown timezones
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
    # Add more timezone mappings if needed

for url in urls:
    print("Parsing RSS feed:", url)
    # Parse the RSS feed
    feed = feedparser.parse(url)
    print("Number of entries:", len(feed.entries))

    # Check if any entry lacks the 'published' field
    missing_published_field = any('published' not in entry for entry in feed.entries)

    if missing_published_field:
        print("This feed does not have the 'published' field for some entries.")
        continue

    # Filter the entries to include only those within the last 24 hours
    filtered_entries = [entry for entry in feed.entries if parser.parse(entry.published, tzinfos=custom_tzinfos).astimezone(tz.tzutc()) >= twenty_four_hours_ago]

    print("Number of filtered entries:", len(filtered_entries))

    # Print each filtered entry in a formatted way
    for entry in filtered_entries:
        print("Title:", entry.title)
        print("Link:", entry.link)
        print("Published:", entry.published)
        print()
