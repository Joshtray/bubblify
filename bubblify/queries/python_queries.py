# ----------------
import os
from dotenv import load_dotenv
import mindsdb_sdk

load_dotenv()

db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_port = os.getenv('DB_PORT')
db_pwd = os.getenv('DB_PWD')
minds_user = os.getenv('MINDS_USER')
minds_pwd = os.getenv('MINDS_PWD')
openai_key = os.getenv('OPENAI_API_KEY')

server = mindsdb_sdk.connect(
    login=minds_user, password=minds_pwd)

try:
    email_db = server.get_database('email_db')
except:
    email_db = server.create_database(
        engine="cockroachdb",
        name="email_db",
        connection_args={
            "host": db_host,
            "database": db_name,
            "user": db_user,
            "port": db_port,
            "password": db_pwd
        }
    )

project = server.get_project()

try:
    server.ml_engines.create('openai_engine', 'openai')
except:
    pass

try:
    email_classifer = project.models.get('email_classifier')
except:
    email_classifier = project.models.create(
        name='email_classifier',
        engine='openai_engine',
        api_key=openai_key,
        predict='email_classification',
        prompt_template='Classify each of the following email informations into one of the provided clusters: {{clusters}}. Respond with just a list of your classifications and no other text, for example: [URGENT]. Consider the following information during classification: 1. If the email contains a deadline and strong language, it should be classified as Urgent.2. If the email subject contains the word urgent, it should be classified as Urgent. Now, analyze the email information and make your classification for each of the following: {{emails_list}}',
        max_tokens=3300,
        temperature=0.8,
    )

email_table = email_db.get_table('emails_info')

# cluster_table = email_db.get_table('clusters')
"""
EXAMPLE OF EMAILS JSON
"""
emails_info = [
    {
        "sender": "GitGuardian <security@getgitguardian.com>",
        "snippet": "GitGuardian has detected the following Google OAuth2 Keys exposed within your GitHub account. Details - Secret type: Google OAuth2 Keys - Repository: Joshtray/bubblify - Pushed date: October 29th 2023,",
        "subject": "[Joshtray/bubblify] Google OAuth2 Keys exposed on GitHub",
        "date_received": "2023-10-28",
        "unread": False,
        "category_name": "INBOX"
    },
    {
        "sender": "John Doe <john.doe@example.com>",
        "snippet": "Hello, just checking in on our project progress. How's it going?",
        "subject": "Project Progress",
        "date_received": "2023-10-27",
        "unread": True,
        "category_name": "INBOX"
    }]
emails_list = []
for email in emails_info:
    emails_list.append("{Email Title}: %s|{Email Sender}: %s|{Email Send date}: %s|{Email Body}: %s|{Was email unread}: %s" % (
        email["subject"], email["sender"], email["date_received"], email["snippet"], email["unread"]))
emails_list = "[" + ','.join(emails_list) + "]"

"""
EXAMPLE OF CLUSTERS LIST
"""
clusters = ['Routine', 'Important', 'Urgent',
            'Job Applications', 'Miscellaneous']
clusters = "[" + ','.join(clusters) + "]"
query = project.query(
    f"SELECT email_classification FROM email_classifier WHERE emails_list = \"{emails_list}\" AND clusters = \"{clusters}\";")

print(query.fetch())
