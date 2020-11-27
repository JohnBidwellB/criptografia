# import smtplib
# import poplib
import email
import imaplib
from credentials import EMAIL, PASSWORD, SERVER, EMAILS_FROM


def connect():
    try:
        # connect to the server and go to its inbox
        mail = imaplib.IMAP4_SSL(SERVER)
        mail.login(EMAIL, PASSWORD)
        # we choose the inbox but you can select others
        mail.select('inbox')
        return(mail)
    except:
        print("Ha ocurrido un error")


def search_by_email(client, email_to_search=None):

    # we'll search using the ALL criteria to retrieve
    # every message inside the inbox
    # it will return with its status and a list of ids
    status, data = client.search(None, 'FROM', email_to_search)
    # the list returned is a list of bytes separated
    # by white spaces on this format: [b'1 2 3', b'4 5 6']
    # so, to separate it first we create an empty list
    mail_ids = []
    # then we go through the list splitting its blocks
    # of bytes and appending to the mail_ids list
    for block in data:
        # the split function called without parameter
        # transforms the text or bytes into a list using
        # as separator the white spaces:
        # b'1 2 3'.split() => [b'1', b'2', b'3']
        mail_ids += block.split()
    return(mail_ids)


def get_emails(client, result_bytes):
    msgs = []  # all the email data are pushed inside an array
    # for num in result_bytes[len(result_bytes):len(result_bytes) - 50:-1]:
    for num in reversed(result_bytes):
        typ, data = client.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs


def get_message_ids(msgs):
    message_ids = []
    # printing them by the order they are displayed in your gmail
    for msg in msgs:
        for sent in msg:
            # print("sent", sent)
            if type(sent) is tuple:
                # print("")
                # print("sent", sent[1])
                # encoding set as utf-8
                content = str(sent[1], 'utf-8')
                data = str(content)
                # print("data", data[0:5000])

                # Handling errors related to unicodenecode
                try:
                    print()
                    # Search Message-ID
                    index_start = data.find("Message-ID: <")
                    index_end = data.find(">", index_start)
                    print(index_start, index_end)
                    message_id = data[index_start +
                                      len("Message-ID: <"): index_end]
                    # Search date
                    index_start = data.find("Received:")
                    index_start = data.find("\n", index_start)
                    index_end = data.find("-", index_start)
                    print(index_start, index_end)
                    if (index_end == -1):
                        print(data[index_start:200])
                    received_at = data[index_start:index_end].strip()
                    # print(received_at)
                    # print(received_at)
                    # Push to message_ids array
                    message_ids.append([received_at, message_id])
                    # data2 = data[indexstart + 5: len(data)]
                    # indexend = data2.find("</div>")

                    # printtng the required content which we need
                    # to extract from our email i.e our body
                    # print(data2[0: indexend])

                except UnicodeEncodeError as e:
                    pass
    return(message_ids)


# def connect():
#     try:
#         # Establecemos conexion con el servidor smtp de gmail
#         mailServer = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#         mailServer.ehlo()
#         mailServer.login(email, password)
#         return (mailServer)
#     except smtplib.SMTPAuthenticationError:
#         print("Ha ocurrido un error al autenticar el usuario")
#         print("Debes autorizar el acceso a aplicaciones poco seguras")
#     except:
#         print("Ha ocurrido un error")


# def connect2():
#     try:
#         # Se establece conexion con el servidor pop de gmail
#         mail_server = poplib.POP3_SSL('pop.gmail.com', 995)
#         mail_server.user(email)
#         mail_server.pass_(password)
#         print("Sesión iniciada")
#         return(mail_server)
#     except:
#         print("Ha ocurrido un error al iniciar sesión")
