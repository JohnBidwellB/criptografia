# import smtplib
# import poplib
import email
import imaplib
from credentials import EMAIL, PASSWORD, SERVER, EMAILS_FROM


def connect():
    try:
        # Conecta al servidor
        mail = imaplib.IMAP4_SSL(SERVER)
        mail.login(EMAIL, PASSWORD)
        # Y selecciona el inbox
        mail.select('inbox')
        return(mail)
    except:
        print("Ha ocurrido un error")


def search_by_email(client, email_to_search=None):
    status, data = client.search(None, 'FROM', email_to_search)
    # data corresponde a una lista de bytes [b'1 2 3', b'4 5 6']
    # Separación de los bytes
    mail_ids = []
    for block in data:
        # b'1 2 3'.split() => [b'1', b'2', b'3']
        mail_ids += block.split()
    return(mail_ids)


def get_emails(client, result_bytes):
    msgs = []
    # reversed de modo de obtener desde el más reciente al más antiguo
    for num in reversed(result_bytes):
        typ, data = client.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs


def get_message_ids(msgs):
    message_ids = []
    for msg in msgs:
        for sent in msg:
            if type(sent) is tuple:
                # Se codifica a utf-8
                content = str(sent[1], 'utf-8')
                data = str(content)
                try:
                    # Busca el Message-ID
                    index_start = data.find("Message-ID: <")
                    index_end = data.find(">", index_start)
                    message_id = data[index_start +
                                      len("Message-ID: <"): index_end]
                    # Busca la fecha
                    index_start = data.find("Received:")
                    index_start = data.find("\n", index_start)
                    index_end = data.find("-", index_start)
                    received_at = data[index_start:index_end].strip()

                    message_ids.append([received_at, message_id])
                except UnicodeEncodeError as e:
                    pass
    return(message_ids)
