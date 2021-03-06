###############################################################################
# -*- coding: utf-8 -*-
###############################################################################

# tornado imports
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.auth
import tornado.escape
import tornado.websocket
from tornado.options import define, options
import pyinotify
import os
import simplejson as json
import subprocess
import utils
import settings

###############################################################################

define('port', default=8000, help='set explicitly port', type=int)
define('debug', default=True, help='debugging', type=bool)

###############################################################################

class Application(tornado.web.Application):
    def __init__(self, options):
        handlers = [
            (r'/', MainHandler),
            (r'/stat', StatHandler),
            (r'/del', DeleteHandler),
            (r'/ins', InsertHandler),
            (r'/conf', ConfigHandler),
            ]
        env = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=options.debug,
            xsrf_cookies=True,
            login_url='/login',
            static_handler_class=MyStaticFileHandler,
            )
        tornado.web.Application.__init__(self, handlers, **env)

###############################################################################

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',
                    book_name=settings.BOOK_NAME,
                    remote=settings.REMOTE_SERVERS)
            
###############################################################################

class StatHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            num = int(self.get_argument('num'))
            files = utils.get_files(settings.PICDIR, num)
            self.write(json.dumps(files))
        except Exception as e:
            self.write(json.dumps(None))

###############################################################################

class DeleteHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            left = self.get_argument('left')
            right = self.get_argument('right')
            os.remove(left)
            os.remove(right)
        except Exception as e:
            utils.delete_all_files(settings.PICDIR)
        self.write(json.dumps(True))

###############################################################################

class InsertHandler(tornado.web.RequestHandler):
    def get(self):
        left = self.get_argument('left')
        right = self.get_argument('right')
        ret = utils.insert(settings.PICDIR, left, right)
        self.write(json.dumps(ret))

###############################################################################

class ConfigHandler(tornado.web.RequestHandler):
    def get(self):
        action = self.get_argument('action')
        if action == 'switch':
            ret = utils.switch_pages()
        elif action == 'bookname':
            name = self.get_argument('name')
            ret = utils.set_bookname(name)
        elif action == 'upload':
            remote = self.get_argument('remote')
            ret = utils.upload(remote)
        self.write(json.dumps(ret))

###############################################################################

class MyStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

###############################################################################

def handle_read_callback(notifier):
    """
    Just stop receiving IO read events after the first
    iteration (unrealistic example).
    """
    print('handle_read callback')
    notifier.io_loop.stop()

###############################################################################
if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(options))
    http_server.listen(options.port)
    ioloop = tornado.ioloop.IOLoop.instance()
    #wm = pyinotify.WatchManager()
    #notifier = pyinotify.TornadoAsyncNotifier(wm, ioloop, callback=handle_read_callback)
    #wm.add_watch('/tmp', pyinotify.ALL_EVENTS)

    ioloop.start()
    #ioloop.close()
    #notifier.stop()

###############################################################################
