import os
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':
    subject, from_email, to = '来自郭军的测试邮件', 'jun.guo01@united-imaging.com', 'yue.liu@united-imaging.com'
    text_content = 'python测试！'
    html_content = '<p>欢迎访问<a href="https://www.baidu.com" target=blank>www.baidu.com</a>,测试邮件！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()