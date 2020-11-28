from client import connect, search_by_email, get_emails, get_message_ids
from credentials import EMAILS_FROM
import csv


def create_file(message_ids):
    messageids_date_file = open("messageids_date.txt", "a")
    messageids_file = open("messageids.txt", "a")

    for message in message_ids:
        messageids_date_file.write(str(message) + "\n")
        messageids_file.write(message[1] + "\n")
    messageids_date_file.close()
    messageids_file.close()


def check_emails():
    with open("datos.csv") as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        email = None
        regex = None
        date = None
        for line in data:
            email, regex, date = line


if __name__ == "__main__":
    mail_server = connect()
    mail_ids = search_by_email(mail_server, EMAILS_FROM)
    messages = get_emails(mail_server, mail_ids)
    message_ids = get_message_ids(messages)
    create_file(message_ids)
    # check_emails()
