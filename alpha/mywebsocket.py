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
from app.models import Coordonates,Site
from random import randint
from datetime import datetime
import time
import ast
import random



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
            self.persit=False


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
            self.speed = coordonnates['speed']
            self.course = coordonnates['course']
            self.satellite = coordonnates['satellite']
            self.moment = datetime.now().strftime('%H:%M:%S')
            coordonnates = {'Lat': self.lat, 'Long': self.long, 'Alt': self.alt, 'Moment': self.moment, 'Sat': self.satellite,'Course': self.course, 'Speed': self.speed}
            self.write_message(coordonnates)
            if self.persit==True:
                self.saveCoordonates()

            return coordonnates



    def open(self):
        self.persit=False

    def on_message(self, message):

        message=ast.literal_eval(message)
        print(message)
        coordonates={}

        if message.get('action')=='get_position':
            coordonates=self.getPosition()
        elif message.get('action')=='start_persiste':
            print("start persisting....")
            self.site_name=str(message.get('site_name'))
            self.capture_type=str(message.get('type'))
            self.description=str(message.get('description'))
            self.site_number = str(int(time.time())) + str(random.randrange(1, 99))
            _name=self.site_name
            _description=self.description
            _type=self.capture_type
            _site_number=self.site_number
            monSite=Site(name=_name,description=_description,site_number=_site_number,type=_type)
            monSite.save()
            self.persit = True
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


    def saveCoordonates(self):
        _lat=str(self.lat)
        _long=str(self.long)
        _alt=str(self.alt)
        _moment=str(self.moment)
        _vitesse=str(self.speed)
        _course=str(self.course)
        _satellite=str(self.satellite)
        _site_number=str(self.site_number)
        coord=Coordonates(lat=_lat,long=_long,alt=_alt,moment=_moment,vitesse=_vitesse,course=_course,satellite=_satellite,site_number=_site_number)

        coord.save()




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