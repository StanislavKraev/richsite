# -*- coding: utf-8 -*-
import codecs
import os
from pybars import Compiler

compiler = Compiler()

import tornado.ioloop
import tornado.web

APP_DIR = os.path.abspath(os.path.dirname(__file__))
CLIENT_DIR = os.path.join(APP_DIR, '../../client')
MODULES_DIR = os.path.join(CLIENT_DIR, "modules")
TEMPLATES_DIR = os.path.join(APP_DIR, "templates")
APPLICATIONS_DIR = os.path.join(CLIENT_DIR, "apps")

#from pydev import pydevd
#pydevd.settrace('localhost', port=33321, stdoutToServer=True, stderrToServer=True, suspend=False)

def render_module(this, options, module_name):
    assert module_name
    result = []
    path = os.path.join(MODULES_DIR, module_name, "templates", "content.html")
    with codecs.open(path, encoding="utf-8") as file:
        template_src = file.read()
        template = compiler.compile(template_src)
        rendered = unicode(template(this.context, helpers=HELPERS))
        result.append(rendered)
    # todo: automatically add merged css, js
    return result

def render_application(this, options, app_name):
    assert app_name
    result = []
    path = os.path.join(APPLICATIONS_DIR, app_name, "content.html")
    with codecs.open(path, encoding="utf-8") as file:
        template_src = file.read()
        template = compiler.compile(template_src)
        rendered = unicode(template(this.context, helpers=HELPERS))
        result.append(rendered)
        # todo: automatically add merged css, js
    return result

HELPERS = helpers={u'module': render_module,
                   u'application' : render_application}

class BaseRequestHandler(tornado.web.RequestHandler):
    def get(self):
        data = self.get_data()

        with codecs.open(os.path.join(TEMPLATES_DIR, self.get_template_name()), encoding="utf-8") as file:
            template_src = file.read()
            template = compiler.compile(template_src)
            result = unicode(template(data, helpers=HELPERS))
        self.write(result)

    def get_data(self): # defaults
        return {'app_name' : "index",
                'page_title' : 'Main Page'}

    def get_template_name(self):
        return "index.html"

class IndexHandler(BaseRequestHandler):
    def get_data(self): # defaults
        data = super(IndexHandler, self).get_data()
        data.update({'app_name' : "index"})
        return data

class ChatPageHandler(BaseRequestHandler):
    def get_data(self): # defaults
        messages = [{'message_body' : "Hi there!"},
                    {'message_body' : "Hi! How are you?"},
                    {'message_body' : "I am fine, than you. And how are you?"},
                    {'message_body' : "Ok, thanks."}]

        data = super(ChatPageHandler, self).get_data()
        data.update({'app_name' : "chat",
                     "chat_module_init" : {"messages" : messages},
                     'page_title' : 'Chat'})
        return data

class NewsPageHandler(BaseRequestHandler):
    def get_data(self): # defaults
        posts = [{'body' : "Advertisement"},
                 {'body' : "Only now. Only for you."},
                 {'body' : "New post"},
                 {'body' : "Ok, thanks."}]

        data = super(NewsPageHandler, self).get_data()
        data.update({'app_name' : "news",
                     "news_module_init" : {"posts" : posts},
                     'page_title' : 'News'})
        return data

application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/chat/", ChatPageHandler),
    (r"/news/", NewsPageHandler),
], debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
