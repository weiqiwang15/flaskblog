# flaskblog - 基于 Flask 的社交博客
## 地址: http://www.yiheng15.com/
## 演示
![](/README/demo.gif)

## 主要功能
- 用户注册、登录、修改密码和更换头像等
- 发表文章、评论文章

## 技术
- 使用 Flask 框架及其相关组件 (Jinja2, SQLAlchemy)
- 使用 MySQL 存储数据，使用 Flask-SQLAlchemy 作为 ORM
- 使用 Nginx 实现反向代理并处理静态文件
- 使用 Gunicorn 实现多进程, 提高访问效率
- 利用 Vagrant 实现开发与部署的环境一直，并使用 Bash 脚本一键部署