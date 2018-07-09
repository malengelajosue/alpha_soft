from .webToranado import  WSHandler
import tornado
import socket
class WS:

    @classmethod
    def start(cls):
        cls.ws = WSHandler()
        application = tornado.web.Application([
            (r'/ws', cls.ws),
        ])

        if __name__ == "__main__":
            http_server = tornado.httpserver.HTTPServer(application)
            http_server.listen(8888)
            myIP = socket.gethostbyname(socket.gethostname())
            print
            '*** Websocket Server Started at %s***' % myIP
            tornado.ioloop.IOLoop.instance().start()