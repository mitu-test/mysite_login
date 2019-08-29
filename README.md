mysite_login
====
项目简介：
-------
mysite_login是基于python3.6+Django 1.11.6+Bootstrap3开发的一个简单的用户登录模块，支持用户注册、登录、密码加密、图形验证码、邮件激活认证等功能。

使用方法：
-------
1.安装Python3.6环境
-------
2.下载代码到本地并解压
-------
3.cmd到根目录下安装相关依赖包
-------
```
pip install -r requirements.txt
```
4.安装mysql数据库，进入mysite/settings.py配置数据库连接
-------

```DATABASES = {
‘default’: {
    # 'ENGINE': 'django.db.backends.sqlite3',
    # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    'ENGINE':'django.db.backends.mysql',     # 数据库类型，mysql
    'NAME':'mysite',            #  database名
    'USER':'root',               # 登录用户
    'PASSWORD':'123456',        #  登录用户名
    'HOST':'127.0.0.1',        # 数据库地址
    'PORT':'3306'              # 数据库端口
}
}
```
5.cmd到根目录下，生成数据库迁移记录
-------
```
python manage.py makemigrations
```
6.完成数据库迁移
-------
```
python manage.py migrate 
```
7.创建超级用户，用于后台管理
-------
```
python manage.py createsuperuser
```
8.运行启动django服务
-------
```
python manage.py runserver 127.0.0.0:8000
```
9.访问127.0.0.0:8000/login进入登录页面
-------
![](https://graph.baidu.com/resource/111deae03ec595eeb9abd01566484087.jpg)
