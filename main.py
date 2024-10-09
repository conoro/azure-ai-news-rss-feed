#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "feedgenerator",
#     "bs4",
#     "requests",
#     "playwright",
# ]
# ///

import feedgenerator
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Function to fetch page content using Playwright
def fetch_page_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(".heading-wrapper")  # Wait for dynamic content to load
        content = page.content()
        browser.close()
        return content

# URL of the page
url = "https://learn.microsoft.com/en-us/azure/ai-services/openai/whats-new"

# Fetch and parse the page using Playwright
html_content = fetch_page_content(url)
soup = BeautifulSoup(html_content, "html.parser")

# Extract updates based on the correct class for headings
updates = soup.find_all("div", class_="heading-wrapper")

# Log updates to console for debugging
if not updates:
    print("No updates found.")
else:
    for idx, update in enumerate(updates, 1):
        title = ("Azure Open AI Updates - "+update.find("h3").get_text()) if update.find("h3") else "Azure Open AI Updates - No Title"
        description = update.get_text(strip=True)
        print(f"Update {idx}: {title}")
        print(f"Description: {description}\n")

# Create an RSS feed
feed = feedgenerator.Rss201rev2Feed(
    title="Azure OpenAI Service Updates",
    link=url,
    description="Latest updates from Azure OpenAI Service",
    language="en",
)

# Loop through and add updates to the feed
for update in updates:
    title = ("Azure Open AI Updates - "+update.find("h3").get_text()) if update.find("h3") else "Azure Open AI Updates - No Title"
    description = update.get_text(strip=True)
    
    feed.add_item(
        title=title,
        link=url,  # Could customize link if needed
        description=description,
    )

# Write the RSS feed to a file
with open("rss.xml", "w") as f:
    feed.write(f, "utf-8")

print("RSS feed generated successfully!")