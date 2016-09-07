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
