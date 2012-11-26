# -*- coding: utf-8 -*-
import codecs
import os
from pybars import Compiler
import simplejson

compiler = Compiler()

import tornado.ioloop
import tornado.web

APP_DIR = os.path.abspath(os.path.dirname(__file__))
CLIENT_DIR = os.path.join(APP_DIR, '../../client')
MODULES_DIR = os.path.join(CLIENT_DIR, "modules")
TEMPLATES_DIR = os.path.join(APP_DIR, "templates")
APPLICATIONS_DIR = os.path.join(CLIENT_DIR, "apps")
COMBO_LOADER_ROOT = os.path.join(CLIENT_DIR, "media", "js", "prebuilt_modules")

#from pydev import pydevd
#pydevd.settrace('localhost', port=33321, stdoutToServer=True, stderrToServer=True, suspend=False)

def render_module(this, options, module_name):
    assert module_name
    result = []
    path = os.path.join(MODULES_DIR, module_name, "templates", "content.html")
    with codecs.open(path, encoding="utf-8") as file:
        template_src = file.read()
        template = compiler.compile(template_src)
        this.context['_current_module_name'] = module_name
        rendered = unicode(template(this.context, helpers=HELPERS, partials=PARTIALS))
        result.append(rendered)
    # todo: automatically add merged css, js
    return result

#def render_module_template(this, options, template_name):
#    assert template_name
#    module_name = this.context['_current_module_name']
#    ctx = this.context
#    while not module_name:
#        ctx = ctx.parent
#        module_name = ctx['_current_module_name']
#    print("module_name: %s" % module_name)
#    result = []
#    path = os.path.join(MODULES_DIR, module_name, "templates", "%s.html" % template_name)
#    with codecs.open(path, encoding="utf-8") as file:
#        template_src = file.read()
#        template = compiler.compile(template_src)
#        rendered = unicode(template(this.context, helpers=HELPERS, partials=PARTIALS))
#        result.append(rendered)
#        # todo: automatically add merged css, js
#    return result

def render_application(this, options, app_name):
    assert app_name
    result = []
    path = os.path.join(APPLICATIONS_DIR, app_name, "content.html")
    with codecs.open(path, encoding="utf-8") as file:
        template_src = file.read()
        template = compiler.compile(template_src)
        this.context['_current_app_name'] = app_name
        rendered = unicode(template(this.context, helpers=HELPERS, partials=PARTIALS))
        result.append(rendered)
        result.append('<script src="/media/js/prebuilt_apps/%s.js"></script>' % app_name)
        # todo: automatically add merged css, js links
    return result

HELPERS = helpers={u'module': render_module,
                   u'application' : render_application}

def get_partial(partial_name):
    module_name = "chat"
    path = os.path.join(MODULES_DIR, module_name, "templates", "%s.html" % "message")
    with codecs.open(path, encoding="utf-8") as file:
        template_src = file.read()
        template = compiler.compile(template_src)
    print("loaded partials: %s" % template_src)
    return template

PARTIALS = {
    u'chat_message' : get_partial("chat_message")
}

class BaseRequestHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            self.get_argument('json')
            json = True
        except Exception:
            json = False

        data = self.get_data()
        if json:
            self.content_type = "application/x-javascript"
            self.write(simplejson.dumps(data))
            self.finish()

        with codecs.open(os.path.join(TEMPLATES_DIR, self.get_template_name()), encoding="utf-8") as file:
            template_src = file.read()
            template = compiler.compile(template_src)
            result = unicode(template(data, helpers=HELPERS, partials=PARTIALS))
        self.write(result)

    def get_data(self): # defaults
        return {'app_name' : "index",
                'page_title' : 'Main Page'}

    def get_template_name(self):
        return "index.html"

class IndexHandler(BaseRequestHandler):
    def get_data(self): # defaults
        data = super(IndexHandler, self).get_data()
        data.update({'app_name' : "index",
                     'username' : 'skraev'})
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

class ComboLoaderHandler(tornado.web.RequestHandler):
    ROOT = COMBO_LOADER_ROOT

    def get(self, *args, **kwargs):
        cur_locale = 'ru'

        file_list = self.request.query.split('&')
        if not len(file_list):
            self.finish()
            return

        type = None
        content_list = []
        for file_name in file_list:
            base, ext = os.path.splitext(file_name)
            if ext == '.js':
                newType = 'js'
            elif ext == '.css':
                newType = 'css'
            else:
                self.write_error(400, "Unknown file type requested: %s" % ext)
                return

            if not type:
                type = newType
            elif type != newType:
                self.write_error(400, "Only same file format types are allowed")
                return

            path = os.path.join(self.ROOT, file_name)
            with codecs.open(path, 'r', 'utf-8') as file:
                content_list.append(file.read())

        mimetypes = {'css' : 'text/css',
                     'js' : 'application/x-javascript'}

        mimetype = mimetypes.get(type)
        if not mimetype:
            self.write_error(400, "Unknown file type requested.")
            return

        content = '\n'.join(content_list)
        self.content_type = mimetype
        self.write(content)
        self.finish()

application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/index/", IndexHandler),
    (r"/chat/", ChatPageHandler),
    (r"/news/", NewsPageHandler),
    (r"/combo/", ComboLoaderHandler),
], debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
