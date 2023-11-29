# ----------------
import os
from dotenv import load_dotenv
import mindsdb_sdk
import numpy as np
import json

load_dotenv()


def classify_emails(emails_info, clusters):
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_port = os.getenv("DB_PORT")
    db_pwd = os.getenv("DB_PWD")
    minds_user = os.getenv("MINDS_USER")
    minds_pwd = os.getenv("MINDS_PWD")
    openai_key = os.getenv("OPENAI_API_KEY")

    server = mindsdb_sdk.connect(login=minds_user, password=minds_pwd)

    try:
        email_db = server.get_database("email_db")
    except:
        email_db = server.create_database(
            engine="cockroachdb",
            name="email_db",
            connection_args={
                "host": db_host,
                "database": db_name,
                "user": db_user,
                "port": db_port,
                "password": db_pwd,
            },
        )

    project = server.get_project()

    try:
        server.ml_engines.create("openai_engine", "openai")
    except:
        pass

    try:
        email_classifer = project.models.get("email_classifier")
    except:
        email_classifier = project.models.create(
            name="email_classifier",
            engine="openai_engine",
            api_key=openai_key,
            predict="email_classification",
            prompt_template="""You are an intelligent classifier of emails.
            
            For the following emails, please categorize them as one of the following: {{clusters}}
            
            Emails: {{emails_list}}
            
            Return only the category name in the following format (each separated by a new comma):
            
            <category_name>, <category_name>, <category_name>
            """,
            max_tokens=3000,
        )

    email_table = email_db.get_table("emails_info")

    emails_list = []
    for email in emails_info:
        emails_list.append(
            "{Email Title}: %s|{Email Sender}: %s|{Email Send date}: %s|{Email Body}: %s|{Was email unread}: %s"
            % (
                email["subject"],
                email["sender"],
                email["date_received"],
                email["snippet"],
                email["unread"],
            )
        )
    emails_list = "[" + ", ".join(emails_list) + "]"

    """
    EXAMPLE OF CLUSTERS LIST
    """

    clusters = "[" + ",".join(clusters) + "]"
    query = project.query(
        f'SELECT email_classification FROM email_classifier WHERE emails_list = "{emails_list}" AND clusters = "{clusters}";'
    )

    email_clusters = np.array(query.fetch())[0][0].split(", ")
    return email_clusters
