#! encoding=utf-8
import gevent.monkey
gevent.monkey.patch_all()
import gevent
import os
from datetime import datetime, date
from threading import Thread
from flask import render_template
from flask import copy_current_request_context

def parse_date(date_str, date_format='%Y-%m-%d', default=date.today()):
    return datetime.strptime(date_str, date_format) if date_str else default

def format_date(date_obj, date_format='%Y-%m-%d'):
    return date_obj.strftime(date_format)

def format_date_from_stamp(timestamp, date_format='%Y-%m-%d'):
    date_obj = datetime.fromtimestamp(timestamp)
    return format_date(date_obj, date_format=date_format)

def async(func):
    def _wrap(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()

    return _wrap

def async_func(func, *args, **kwargs):
    """
        异步任务处理。本函数会立即返回，并使用 gevent 的新线程执行 func 函数（带 request 上下文）。
    """
    return gevent.spawn(copy_current_request_context(func), *args, **kwargs)

def render_macro(filename, *args, **kwargs):
    kwargs['auto_render'] = True
    return render_template(filename, *args, **kwargs)

def remove_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError, e:
            print ("Error: %s - %s." % (e.filename,e.strerror))

