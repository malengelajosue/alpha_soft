#!/usr/bin/env python
import threading

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.wsgi
from alpha.wsgi import application as myapp_wsgi
from app.models import Post
from random import randint
from datetime import datetime
import time

from myclasses.gpsaccess import Gpsaccess as Gps

# Javascript Usage:
# var ws = new WebSocket('ws://localhost:8000/ws');
# ws.onopen = function(event){ console.log('socket open'); }
# ws.onclose = function(event){ console.log('socket closed'); }
# ws.onerror = function(error){ console.log('error:', err); }
# ws.onmessage = function(event){ console.log('message:', event.data); }
# # ... wait for connection to open
# ws.send('hello world')

post=posts=Post.objects.all()

class MyAppWebSocket(tornado.websocket.WebSocketHandler):
    # Simple Websocket echo handler. This could be extended to
    # use Redis PubSub to broadcast updates to clients.

    def sendCordonnates(cls):
        cls.connected=False
        if cls.connected==False:
            cls.gpsDevice = Gps()
            cls.connected=True


        while (True):
            coordonnates = cls.gpsDevice.readCoordonates()


            if  coordonnates!={}:

                lat = float(coordonnates['latitude'])
                long = float(coordonnates['longitude'])
                alt = coordonnates['altitude']
                speed=coordonnates['speed']
                course = coordonnates['course']
                satellite = coordonnates['satellite']
                moment = datetime.now().strftime('%H:%M:%S')
                coordonnates = {'Lat': lat, 'Long': long, 'Alt': alt, 'Moment': moment,'Sat':satellite,'Course':course,'Speed':speed}
                cls.write_message(coordonnates)
                time.sleep(0.5)

    def open(self):
        try:
             print
             ('new connection')
             t=threading.Thread(target=self.sendCordonnates())
             t.start()
        except tornado.websocket.WebSocketClosedError:
            print('la connexion a ete fermee!')
            self.close()


           # self.write_message(coordonnates)

    def on_message(self, message):
        print
        ( message)
        # Reverse Message and send it back
        print
        'sending back message: %s' % message[::-1]
        self.write_message(message[::-1])

    def on_close(self):
        try:
            print
            'connection closed'
        except tornado.websocket.WebSocketClosedError:
            print('connection fermee de maniere inatendu!')
            self.close()

    def check_origin(self, origin):
        return True




application = tornado.web.Application([
    (r'/ws', MyAppWebSocket),
    (r'/(.*)', tornado.web.FallbackHandler, dict(
        fallback=tornado.wsgi.WSGIContainer(myapp_wsgi)
    )),
], debug=True)

if __name__ == '__main__':
    application.listen(8001)
    tornado.ioloop.IOLoop.instance().start()