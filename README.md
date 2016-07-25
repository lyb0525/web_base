# 开发说明
## 开发环境搭建
1. python运行环境为2.7.9
2. git clone repo 并 checkout br_name 分支
3. `virtualenv flask` 创建virtualenv
4. `source flask/bin/activate` 启用virtualenv开发环境
5. `pip install -r ./requirements.txt` 安装依赖库
6. Congratulations!


## 测试环境服务器通过`manage.py`运行：
  ```
  python manage.py runserver
  ```

## 生产环境说明
1. `uwsgi -s /tmp/uwsgi++.sock -w app:app`
2. `killall -HUP nginx`  __OR__ `nginx -s reload`


