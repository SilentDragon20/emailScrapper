# emailScrapper
A Python tool that connects to Gmail via IMAP, fetches the last 5 emails, cleans HTML content, and summarizes each email using the LSA algorithm and generates a short summary using Natural Language Processing (NLP).

## Features
- Fetch the latest emails from Gmail securely using an **App Password**.
- Decode email headers (Subject, From, Date) into human-readable format.
- Clean HTML content from email bodies using **BeautifulSoup**.
- Summarize email content using **Sumy LSA summarizer**.
- Display emails with sender, date, and summarized body in a readable format.

## Requirements
- Python 3.10+  
- `beautifulsoup4`  
- `sumy`  

Install dependencies:
```bash
pip install beautifulsoup4 sumy


#Usage
1. Enable 2-step verfication on your Gmail account
2. Generate an App password for the script which is not your actual password but a 16 character long auto generated password
3. Replace EMAIL_ACCOUNT and APP_PASSWORD in the script with your credentials
4. Run the script:
    python emailScrapper.py
