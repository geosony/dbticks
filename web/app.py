import tornado.ioloop
from tornado import web, ioloop
from tornado.options import options

from settings import settings
from routes import handlers

class Application(web.Application):
    def __init__(self):
        web.Application.__init__(self, handlers, **settings)

def main():
    app = Application()
    app.listen(options.port)
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
