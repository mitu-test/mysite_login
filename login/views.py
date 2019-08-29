from django.shortcuts import render,redirect
from .models import User,ConfirmString
from .forms import UserForm
from .forms import RegisterForm
import hashlib
import datetime
from django.conf import settings
# Create your views here.


def index(request):
    """主页视图"""
    pass
    return render(request,'index.html')


def login(request):
    """登录视图"""
    if request.session.get('is_login',None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if not user.has_confirmed:
                    message = '该用户还未通过邮件确认!'
                    return render(request,'login.html',locals())
                if user.password == hash_code(password): #哈希值和数据库内的值进行比较
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request,'login.html',locals())
    login_form = UserForm()
    return render(request,'login.html',locals())


def logout(request):
    """登出视图"""
    if not request.session.get('is_login',None):
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


def register(request):
    """注册视图"""
    if request.session.get('is_login',None):
        #登录状态不允许注册
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request,'register.html',locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user: #用户名唯一
                    message = '用户名已经存在，请重新选择用户名！'
                    return render(request,'register.html',locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user: #邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request,'register.html',locals())
                new_user = User()
                new_user.name = username
                new_user.password = hash_code(password1)#使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                code = make_confirm_string(new_user)
                send_email(email,code)
                return redirect('/login/') #自动跳转到登录页面
        else:
            return render(request,'register.html',locals())
    register_form = RegisterForm()
    return render(request,'register.html',locals())


def hash_code(s,salt='mysite'):
    """hash密码加密"""
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    """生成邮箱验证码"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(email,code):
    """注册发送邮件"""
    from django.core.mail import EmailMultiAlternatives
    subject = "来自郭军的测试邮件！"
    text_content = "谢谢各位！"
    html_content = '''<p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.guojun.com</a>,测试邮件！</p>
                      <p>请点击上方链接完成注册确认！</p>
                      <p>此链接有效期为{}天！</p>
                      '''.format('127.0.0.1:8000',code,settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    """邮箱注册激活"""
    code = request.GET.get('code',None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求！'
        return render(request,'confirm.html',locals())

    create_time = confirm.create_time
    now = datetime.datetime.now()
    if now > create_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册！'
        return render(request,'confirm.html',locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request,'confirm.html',locals())