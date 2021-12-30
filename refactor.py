import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Emailer:

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.gmail_smtp = 'smtp.gmail.com'
        self.gmail_imap = 'imap.gmail.com'

    def send_message(self, recipients_list: list, subject_text: str, msg_text: str):
        message_send = MIMEMultipart()
        message_send['From'] = self.login
        message_send['To'] = ', '.join(recipients_list)
        message_send['Subject'] = subject_text
        message_send.attach(MIMEText(msg_text))
        mailer = smtplib.SMTP(self.gmail_smtp, 587)
        # identify ourselves to smtp gmail client
        mailer.ehlo()
        # secure our email with tls encryption
        mailer.starttls()
        # re-identify ourselves as an encrypted connection
        mailer.ehlo()
        mailer.login(self.login, self.password)
        mailer.sendmail(self.login, message_send.as_string())
        mailer.quit()

    def receive_message(self, header: str):
        # receive
        mail_imap = imaplib.IMAP4_SSL(self.gmail_imap)
        mail_imap.login(self.login, self.password)
        mail_imap.list()
        mail_imap.select('inbox')
        criteria = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail_imap.uid('search', header, criteria)
        assert data[0], 'There are no letters with current header'
        latest_mail_uid = data[0].split()[-1]
        result, data = mail_imap.uid('fetch', latest_mail_uid, '(RFC822)')
        email_raw = data[0][1]
        email_msg = email.message_from_string(email_raw)
        mail_imap.logout()
        # end receive


def main():
    email_address = input('Enter your e-mail:')
    email_password = input('Enter your password:')
    gmail = Emailer(email_address, email_password)
    recipients_list = []
    while True:
        cmd = input('\nWhat do you want to do?\n1) Send e-mail\n2) Receive e-mail\nType "send" or "receive."\n')
        if cmd.lower() == 'send':
            while True:
                amount_of_recipients = int(input('How many recipients are there? '))
                if amount_of_recipients < 1:
                    print('Incorrect amount of recipients.\n')
                else:
                    break
            for amount in range(amount_of_recipients):
                email_to_add = input(f'Number {amount + 1} recipient: ')
                recipients_list.append(email_to_add)
            email_subject = input('Enter e-mail subject: ')
            email_text = input('Enter your e-mail message:')
            gmail.send_message(recipients_list, email_subject, email_text)
        elif cmd.lower() == 'receive':
            header = input('Enter e-mail header: ')
            gmail.receive_message(header)
        else:
            print('Unknown command.')
            print('_' * 50)


if __name__ == '__main__':
    main()

