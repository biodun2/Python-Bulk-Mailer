from django.shortcuts import render
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .forms import UploadFileForm
from .models import MailDatas
from email import encoders
from email.mime.base import MIMEBase


def email_text_with_attachment(smtp_server, smtp_port, user_password, fromaddr, toaddr, subject, body, filename, file_name, type_used):
    msg = MIMEMultipart()
    #msg['From'] = fromaddr
    #msg['To'] = [toaddr]
    msg['Subject'] = subject
    msg.attach(MIMEText(body, type_used))
    filename =filename
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % file_name)

    msg.attach(part)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(fromaddr, user_password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def email_text(smtp_server, smtp_port, user_password, fromaddr, toaddr, subject, body, type_used):

    msg = MIMEMultipart()
    #msg['From'] = fromaddr
    #msg['To'] = [toaddr]
    msg['Subject'] = subject


    msg.attach(MIMEText(body, type_used))

    server = smtplib.SMTP(smtp_server, smtp_port)
    #server.connect(smtp_server, smtp_port)
    server.starttls()
    server.login(fromaddr, user_password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def home(request, template_name="index.html"):
    #recent_file = MailDatas.objects.all()[0]
    # last_file = recent_file.file
    receivers_mail = []
    query = MailDatas.objects.all()
    form = UploadFileForm(request.POST, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            files = form.cleaned_data['file']
        postdata = request.POST.copy()
        smtp_username = postdata.get('smtp_username', '')
        smtp_password = postdata.get('password', '')
        smtp_server = postdata.get('smtp_server', '')
        smtp_port = postdata.get('smtp_port', '')
        smtp_ssl = postdata.get('smtp_ssl', '')
        type_used = postdata.get('type', '')
        check_box = postdata.get('yes', '')
        #file = request.FILES['file', '']
        subject = postdata.get('subject', '')
        message = postdata.get('message', '')
        from_email = postdata.get('sender_email', '')
        receivers = postdata.get('receiver_emails', '')
        new_receivers = receivers.split(',')

        #receivers_mail.append(new_receivers)
        for x in new_receivers:
            receivers_mail.append(str(x))
        if len(smtp_port) == "":
            smtp_port = 587
        new_datas = MailDatas(sender_email=from_email, sender_subject=subject, file=files)
        new_datas.save()

        if len(request.FILES) == 0 :
            email_text(smtp_server,smtp_port,smtp_password, from_email, receivers_mail, subject, message, type_used)


        else:
            last = MailDatas.objects.filter(sender_email=from_email).order_by('-id')[0]
            email_text_with_attachment(smtp_server,smtp_port,smtp_password, from_email, receivers_mail, subject, message, last.file.path, files, type_used)
            #full_path = "http://bulkmime.pythonanywhere.com" + last.file.url


        if True:
            success = True
    return render(request, template_name, locals())

"""Send an email message from the user's account.
"""
'''

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors


def create_draft(service, user_id, message_body):
  """Create and insert a draft email. Print the returned draft's message and id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_body: The body of the email message, including headers.

  Returns:
    Draft object, including draft id and message meta data.
  """
  try:
    message = {'message': message_body}
    draft = service.users().drafts().create(userId=user_id, body=message).execute()

    print 'Draft id: %s\nDraft message: %s' % (draft['id'], draft['message'])

    return draft
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    return None


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print 'Message Id: %s' % message['id']
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}


def create_message_with_attachment(
    sender, to, subject, message_text, file):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string())}
 '''
