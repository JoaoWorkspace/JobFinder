import os
import re
import sys
import glob
import json
import time
import base64
import random
import smtplib
import getpass
import logging

from datetime import datetime
from email.message import EmailMessage
from email.contentmanager import ContentManager
from email.policy import default
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from Utils import get_integer_input

def is_valid_email(email):
    # Regular expression for validating an email address
    email_regex = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    )
    return re.match(email_regex, email) is not None

def generate_email_body(company_name, position, data):
    opening = "".join(data['message']['opening']).format(company=company_name)
    constant = "".join(data['message']['constant']).format(position=position)
    variable = random.choice(data['message']['variable']).format(company=company_name)
    ending = "".join(data['message']['ending']).format(name=data['name'])

    email_body = f"""
    <html>
    <body>
        {opening}
        {constant}
        {variable}
        {ending}
    </body>
    </html>
    """
    return email_body

def authenticate_gmail():
    credentials = None
    if os.path.exists('token.json'):
        try:
            credentials = Credentials.from_authorized_user_file('token.json')
        except Exception as error:
            logging.error(f"A problem happened processing file 'token.json': {error}")
            print(f"<- EMAIL GENERATOR -> ERROR: {error}")
            sys.exit()
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/gmail.send'])
                credentials = flow.run_local_server(port=8080)
            except Exception as error:
                logging.error(f"A problem happened processing file 'credentials.json': {error}")
                print(f"<- EMAIL GENERATOR -> ERROR: {error}")
                sys.exit()
        with open('token.json', 'w', encoding='utf-8') as token:
            token.write(credentials.to_json())
    return credentials

def send_gmail(company_name, position, email_receiver, pdf_path, attachment_name, email_body, credentials):
    service = build('gmail', 'v1', credentials=credentials)
    email_subject = f"Application for {position} at {company_name}"

    message = MIMEMultipart()
    message['to'] = email_receiver
    message['subject'] = email_subject

    message.attach(MIMEText(email_body, 'html'))

    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_name)}')
            message.attach(part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {'raw': raw_message}

    try:
        service.users().messages().send(userId='me', body=message).execute()
        # Log the email details
        logging.info(f"Generated Email - Recipient: {email_receiver} | Subject: {email_subject}\nBody: {email_body}")
        print(f"<- EMAIL GENERATOR -> Email sent to {email_receiver}")
    except Exception as error:
        print(f"<- EMAIL GENERATOR -> ERROR: {error}")

def get_most_recent_company_cv(company_cv_path):
    """
    Fetches the most recent file starting with the given prefix.
    
    Parameters:
    company_cv_path (str): The prefix of the files to search for.
    
    Returns:
    str: The path to the most recent file.
    """
    # Add wildcard to search_pattern
    search_pattern = f"{company_cv_path}*"
    
    # Get a list of files matching the pattern
    files = glob.glob(search_pattern)
    
    if not files:
        return None
    
    # Sort files based on modification time, in descending order
    files.sort(key=os.path.getmtime, reverse=True)
    
    # Return the most recent file
    return files[0]

def configure_logging(log_dir='email'):
    # Function to generate a timestamped filename
    def get_timestamped_filename(base_name, extension='log'):
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        return f"{timestamp}_{base_name}.{extension}"

    # Create the 'mail' directory if it doesn't exist
    log_dir = "mail"
    os.makedirs(log_dir, exist_ok=True)

    # Generate the log filename with a UTC timestamp
    log_file = os.path.join(log_dir, get_timestamped_filename("email"))

    # Configure logging
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def send_cv_email_to_companies(data, pdf_folder):
    def configure_email_interval(email_interval_minimum, email_interval_maximum): #  Configures the intervals that will be used
        if email_interval_minimum < 30:
            print(f"<- EMAIL GENERATOR -> ERROR: Interval Minimum of {email_interval_minimum} minutes is lower than 30 minutes!\n<- EMAIL GENERATOR -> Applying default values instead...")
            email_interval_minimum = 30
        
        if email_interval_maximum < 30:
            print(f"<- EMAIL GENERATOR -> ERROR: Interval Maximum of {email_interval_maximum} minutes is lower than 30 minutes!\n<- EMAIL GENERATOR -> Applying default values instead...")
            email_interval_maximum = 60 
        
        if email_interval_maximum < email_interval_minimum:
            print(f"<- EMAIL GENERATOR -> ERROR: Interval Maximum of {email_interval_maximum} minutes is lower than Interval Minimum of {email_interval_minimum} minutes!\n<- EMAIL GENERATOR -> Applying default values instead...")
            email_interval_minimum = 30 # 30 minutes is the minimum so we don't reach GMail API's cap
            email_interval_maximum = 60 # 60 minutes is the maximum range the application will randomize
        print(f"<- EMAIL GENERATOR -> Interval set to {email_interval_minimum} - {email_interval_maximum} minutes")
        return email_interval_minimum, email_interval_maximum
    
    def engage_email_authentication(): # Engages in I/O with the user to configure the email with the GMail API.
        email = data['contact']['email']
        print(f"<- EMAIL GENERATOR -> Do you wish to use {email} as your sender email?")
        print("\t[1] Yes")
        print("\t[2] No")
        choice = get_integer_input("Your choice: ","<- EMAIL GENERATOR ->")

        email_valid = False
        authenticated = False
        if choice == 1:
            email_sender = email
            email_valid = is_valid_email(email_sender)
            if not email_valid or not email_sender.endswith('@gmail.com'):
                print(f"{email_sender} is invalid.")
            else:
                print(f"<- EMAIL GENERATOR -> GMail detected. Attempting to authenticate and send emails through GMail API...")
                credentials = authenticate_gmail()
                authenticated = True
                print("<- EMAIL GENERATOR -> Successfully authenticated GMail! Sending...")
        
        while not email_valid or not authenticated:
            email_sender = input("<- EMAIL GENERATOR -> Enter your email address (only GMAIL supported): ")
            email_valid = is_valid_email(email_sender)
            if not email_valid or not email_sender.endswith('@gmail.com'):
                print(f"<- EMAIL GENERATOR -> The email '{email_sender}' is not valid, please re-type.")
            else:
                print(f"<- EMAIL GENERATOR -> GMail detected. Attempting to authenticate and send emails through GMail API...")
                credentials = authenticate_gmail()
                authenticated = True
                print("<- EMAIL GENERATOR -> Successfully authenticated GMail! Sending...")
        return credentials
    
    def process_emails(credentials): # Going through every company and sending the CV
        companies = data['companies']
        first_iteration = True
        for company in companies:
            # Doesn't wait an interval on the first iteration
            if not first_iteration: 
                interval_between_email = random.randint(email_interval_minimum, email_interval_maximum)
                print(f"<- EMAIL GENERATOR -> Waiting {interval_between_email} minutes before sending the next email...")
                time.sleep(interval_between_email*60) # Sleeps {interval_between_email} minutes
            first_iteration = False

            company_name, company_logo_extension = os.path.splitext(company['logo'])
            recipient_email = company['email']
            position = company.get('position', 'Senior Fullstack Developer')
            company_cv_path = os.path.join(pdf_folder, f"curriculum_{company_name}.pdf")
            
            print(f"<- EMAIL GENERATOR -> Company: {company_name}, Position: {position}, BaseCV: {company_cv_path}")
            if os.path.exists(company_cv_path):
                company_cv_pattern, company_cv_extension = os.path.splitext(company_cv_path)
                # This function gets all the files starting with 'company_cv' with all the different generated GUIDs and fetches the most recently created to be used.
                # This is essential because there's no way to predict the most recent GUID generated (if any).
                most_recent_company_cv = get_most_recent_company_cv(company_cv_pattern)
                print(f"<- EMAIL GENERATOR -> Most recent company CV found: {most_recent_company_cv}")
                
                # Should be impossible to not find the most recent company CV. With this validation we can skip sending an email without CV.
                if not most_recent_company_cv:
                    print(f"<- EMAIL GENERATOR -> ERROR: Failed to get a CV for {company_name} in {pdf_folder}. Aborting this email.")
                else:
                    email_body = generate_email_body(company_name, position, data)
                    print(f"<- EMAIL GENERATOR -> Email body: {email_body}")
                    send_gmail(company_name, position, recipient_email, most_recent_company_cv, company_cv_path, email_body, credentials)
            else:
                print(f"<- EMAIL GENERATOR -> PDF for {company_name} not found in {pdf_folder}. Skipping...")
    # Start
    configure_logging()
    minimum_interval = data.get('minimumInterval', 30)
    maximum_interval = data.get('maximumInterval', 60)
    email_interval_minimum, email_interval_maximum = configure_email_interval(minimum_interval, maximum_interval)
    credentials = engage_email_authentication()
    process_emails(credentials)
    # End