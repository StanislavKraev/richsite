# -*- coding: utf-8 -*-
import os
from tornado import template

import tornado.ioloop
import tornado.web

APP_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(APP_DIR, "templates")
loader = template.Loader(TEMPLATES_DIR)

class BaseRequestHandler(tornado.web.RequestHandler):
    def get(self):
        data = self.get_data()
        result = loader.load(self.get_template_name()).generate(**data)
        self.write(result)

    def get_data(self): # defaults
        return {'root' : False}

    def get_template_name(self):
        return "index.html"

class IndexHandler(BaseRequestHandler):
    def get_data(self):
        return {'root' : True}

class ChatPageHandler(BaseRequestHandler):
    def get_template_name(self):
        return "chat.html"

class NewsPageHandler(BaseRequestHandler):
    def get_template_name(self):
        return "news.html"

application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/chat/", ChatPageHandler),
    (r"/news/", NewsPageHandler),
], debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
