#!/usr/bin/env python
import signal
import sys
import threading

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.wsgi
from tornado.iostream import StreamClosedError
from alpha.wsgi import application as myapp_wsgi
from app.models import Post
from random import randint
from datetime import datetime
import time
import ast

from myclasses.gpsaccess import Gpsaccess as Gps

# Javascript Usage:
# var ws = new WebSocket('ws://localhost:8000/ws');
# ws.onopen = function(event){ console.log('socket open'); }
# ws.onclose = function(event){ console.log('socket closed'); }
# ws.onerror = function(error){ console.log('error:', err); }
# ws.onmessage = function(event){ console.log('message:', event.data); }
# # ... wait for connection to open
# ws.send('hello world')


class MyAppWebSocket(tornado.websocket.WebSocketHandler):
    # Simple Websocket echo handler. This could be extended to
    # use Redis PubSub to broadcast updates to clients.

    def sendCordonnates(self):
        self.connected=False
        if self.connected==False:
            self.gpsDevice = Gps()
            self.myCoord=''
            self.connected=True


        while (True):
            coordonnates = self.gpsDevice.readCoordonates()
            self.myCoord=coordonnates
            if  coordonnates!={}:

                lat = float(coordonnates['latitude'])
                long = float(coordonnates['longitude'])
                alt = coordonnates['altitude']
                speed=coordonnates['speed']
                course = coordonnates['course']
                satellite = coordonnates['satellite']
                moment = datetime.now().strftime('%H:%M:%S')
                coordonnates = {'Lat': lat, 'Long': long, 'Alt': alt, 'Moment': moment,'Sat':satellite,'Course':course,'Speed':speed}
                self.write_message(coordonnates)
                time.sleep(0.5)
    def getPosition(self):
        self.connected = False
        if self.connected == False:
            self.gpsDevice = Gps()
            self.myCoord = ''
            self.connected = True

        coordonnates = self.gpsDevice.readCoordonates()
        self.myCoord = coordonnates
        if coordonnates != {}:
            self.lat = float(coordonnates['latitude'])
            self.long = float(coordonnates['longitude'])
            self.alt = coordonnates['altitude']
            speed = coordonnates['speed']
            course = coordonnates['course']
            satellite = coordonnates['satellite']
            self.moment = datetime.now().strftime('%H:%M:%S')
            coordonnates = {'Lat': self.lat, 'Long': self.long, 'Alt': self.alt, 'Moment': self.moment, 'Sat': satellite,'Course': course, 'Speed': speed}
            self.write_message(coordonnates)
            return coordonnates



    def open(self):
        self.persit=False

    def on_message(self, message):

        message=ast.literal_eval(message)
        print(message)
        coordonates={}

        if message.get('action')=='get_position':
            coordonates=self.getPosition()
            print(message.get('action'))
        elif message.get('action')=='start_persiste':
            print("start persisting....")
            self.persisteCoordonates()
        elif message.get('action')=='stop_persiste':
           self.persit=False

    def run(self):
        time.sleep(1)
        return

    def on_close(self):
        try:
            print
            'connection closed'
        except tornado.websocket.WebSocketClosedError:
            print('connection fermee de maniere inatendu!')
            self.close()

    def check_origin(self, origin):
        return True


    def persisteCoordonates(self):
        self.getPosition()
        print("enregistrement"+self.moment)


application = tornado.web.Application([
    (r'/ws', MyAppWebSocket),
    (r'/(.*)', tornado.web.FallbackHandler, dict(
        fallback=tornado.wsgi.WSGIContainer(myapp_wsgi)
    )),
], debug=True)

if __name__ == '__main__':


    application.listen(8001)
    instance=tornado.ioloop.IOLoop.instance()
    instance.start()




    def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        instance.stop()
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()