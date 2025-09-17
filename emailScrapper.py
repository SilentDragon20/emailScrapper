import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from email.utils import parsedate_to_datetime
import ssl

context = ssl.create_default_context()
mail = imaplib.IMAP4_SSL("imap.gmail.com", 993, ssl_context=context)

# Gmail IMAP server
IMAP_SERVER = "imap.gmail.com" # Gmail IMAP server address
EMAIL_ACCOUNT = "abcdefg@gmail.com" # Email address to fetch emails from
APP_PASSWORD = "abcd efgh ijkl mnop"  # <- App Password for Gmail(NOT THE REAL PASSWORD BUT "APP PASSWORD - 16 CHARACTER ")
LANGUAGE = "english" #Language use for text summarization

# --- HELPER FUNTIONS ---
def decode_mime_words(s):
    #Decode MIME-encoded email headers (like Subject or From)
    #Returns a human-readable string. If no subject, returns '(No Subject)'.
    if not s:
        return "(No Subject)"
    decoded = decode_header(s)
    return ''.join([
        str(t[0], t[1] or 'utf-8') if isinstance(t[0], bytes) else t[0]
        for t in decoded
    ])

def clean_body(body):
    #Remove HTML tags and extra whitespace from email body
    #Returns clean plain text
    if not body:
        return ""
    soup = BeautifulSoup(body, "html.parser")
    text = soup.get_text()
    return ' '.join(text.split())

def summarize_text(text, sentences_count=2):
    #Summarize a given text using LSA summarizer.
    #if text is too short(<20 words), returns original text
    if not text or len(text.split()) < 20:  # skip very short bodies
        return text
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    summarizer = LsaSummarizer(Stemmer(LANGUAGE))
    summarizer.stop_words = get_stop_words(LANGUAGE)
    summary = summarizer(parser.document, sentences_count)
    return " ".join(str(s) for s in summary)

def print_email(subject, sender, date_str, body):
    """
    Print formatted email details including summarized body

    """
    print(f"📧 Subject: {subject}")
    print(f"👤 From: {sender}")
    print(f"📅 Date: {date_str}")
    print(f"📝🔹 Summary: {summarize_text(body, sentences_count=2)}")
    print("-" * 60)

# --- FETCH EMAILS ---
def fetch_emails():
    """
    Connect to Gmail via IMAP, fetch the last 5 emails from inbox,
    decode headers, clean body, and return a list of emails.
    Each email is a tuple: (subject, sender, formatted_date, clean_body)

    """
    print("Fetching emails...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER) #Connect securely to IMAP server
    mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "RECENT")  # all kinds of emails 
    email_ids = messages[0].split()

    emails = []
    for eid in email_ids[-5:][::-1]:  # last 5 unread emails
        status, msg_data = mail.fetch(eid, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                # print("RAW DATE HEADER:" , msg.get("Date"))

                #DECODE EMAIL HEADERS
                subject = decode_mime_words(msg["Subject"])
                sender = decode_mime_words(msg.get("From", "(Unknown Sender)"))

                #PARSE AND FORMAT EMAIL DATE
                raw_date = msg.get("Date")
                try:
                    data_obj = parsedate_to_datetime(raw_date)
                    date_str = data_obj.strftime("%b %d, %Y - %I:%M %p")
                except Exception:
                    date_str = raw_date or "(Unknown Date)"
                

                # EXTRACT EMAIL BODY(SUPPORTS PLAIN TEXT OR HTML)
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                body = clean_body(body) #CLEAN BODY TEXT
                emails.append((subject, sender, date_str, body))# ADD EMAIL TO LIST

    mail.logout() #CLOSE CONNECTION
    return emails

# --- MAIN EXECUTION---
if __name__ == "__main__":
    emails = fetch_emails()  #Fetch emails from Gamil
    if not emails:
        print("No new emails.")
    else:
        #Print each email with summary 
        for subject, sender, date_str, body in emails:
            print_email(subject, sender, date_str, body)


