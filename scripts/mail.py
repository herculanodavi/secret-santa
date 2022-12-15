import smtplib
import logging
from jinja2 import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from dataclasses import dataclass
from person import Person


@dataclass
class User:
    email: str
    password: str


class Sender:
    def __init__(self, user: User):
        self.user = user
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.template = Template(open('index.html').read())

    def __del__(self):
        self.server.quit()

    def connect(self):
        self.server.starttls()
        self.server.login(self.user.email, self.user.password)

    def parameters_from(self, sender: Person, receiver: Person) -> dict[str, str]:
        return {
            'receiver_pronoun': receiver.pronoun,
            'giver_name': sender.name,
            'receiver_name': receiver.name
        }

    def send_mail(self, sender: Person, receiver: Person):
        rendered_template = self.template.render(
            self.parameters_from(sender, receiver))

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Amigo Secreto 2022!"
        msg['From'] = self.user.email
        msg['To'] = sender.email

        text = MIMEText(rendered_template, 'html')
        msg.attach(text)

        image = MIMEImage(open('images/image-1.png', 'rb').read())
        image.add_header('Content-ID', '<image1>')
        msg.attach(image)

        image = MIMEImage(open('images/image-2.png', 'rb').read())
        image.add_header('Content-ID', '<image2>')
        msg.attach(image)

        self.server.sendmail(self.user.email, sender.email, msg.as_string())



class DummySender:
    def __init__(self, user: User):
        self.user = user

    def connect(self):
        pass

    def send_mail(self, sender: Person, receiver: Person):
        logging.debug(f"Sending from {sender} to {receiver}")