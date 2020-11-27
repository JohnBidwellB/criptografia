from client import connect3, search_by_email, get_emails, get_message_ids
from email import parser
from credentials import EMAILS_FROM


def create_file(message_ids):
    file = open("result.txt", "a")
    for message in message_ids:
        file.write(str(message) + "\n")
    file.close()


if __name__ == "__main__":
    print("Hello world")
    mail_server = connect3()
    mail_ids = search_by_email(mail_server, EMAILS_FROM)
    messages = get_emails(mail_server, mail_ids)
    # print("messages", messages)
    message_ids = get_message_ids(messages)
    print(message_ids)
    create_file(message_ids)
    # numero = len(mail_server.list()[1])
    # # print(numero)
    # for i in range(numero):
    #     print("Mensaje numero"+str(i+1))
    #     print("--------------------")
    #     # Se lee el mensaje
    #     response, headerLines, bytes = mail_server.retr(i + 1)
    # headers = parser.HeaderParser(headerLines)
    # print(response)
    # print(headerLines)
    # # Se mete todo el mensaje en un unico string
    # mensaje = '\n'.join(headers)
    # print(mensaje)
    # # Se parsea el mensaje
    # p = parser.Parser()
    # email = p.parsestr(mensaje)
    # # Se sacan por pantalla los campos from, to y subject
    # print("From: "+email["From"])
    # print("To: "+email["To"])
    # print("Subject: "+email["Subject"])
