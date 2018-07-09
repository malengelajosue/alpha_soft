
import serial
import  time
from serial.serialutil import SerialException
class Gpsaccess:
    def __init__(self):
        self.path='/dev/ttyUSB0'
        self.baurate=4800
        self.timeout=1
        self.readSpeed=1200
        self.latitude=''
        self.longitude=''
        self.altitude=''
        self.speed =''
        self.course=''
        self.satellite=''
        self.usbPort = ''
        self.connected=False
        self.data=[]

    def converter(self,coordonate):
        coord = coordonate.split('.')

        mmmList = coord[1]
        mmm = mmmList[:-1]
        signe = mmmList[-1:]
        ddmm = list(coord[0])
        if int(''.join(ddmm[0:1])) != 0:
            dd = ''.join(ddmm[0:2])
            mm = ''.join(ddmm[2:])
        else:
            dd = ''.join(ddmm[1:3])
            mm = ''.join(ddmm[3:])

        newCoordonate = int(dd) + (int(mm) / 60) + (int(mmm) / (60 * (10 ** len(mmm))))
        if signe == 'S' or signe=='W':
            newCoordonate *= -1
        newCoordonate=format(newCoordonate,'4f')
        return  newCoordonate
    def readCoordonates(self):
        coordonates={}

        try:
            if self.connected==False:
                self.usbPort = serial.Serial(self.path, self.baurate,timeout= self.timeout)
                self.connected=True

            data=self.usbPort.read(1200)
            pos1 = data.find(bytes('$GPRMC', 'utf-8'))
            post2 = data.find(bytes("\n", 'utf-8'), pos1)
            pos3 = data.find(bytes('$GPGGA', 'utf-8'))
            pos4 = data.find(bytes("\n", 'utf-8'), pos3)

            RMC=data[int(pos1):int(post2)]
            GGA=data[int(pos3):int(pos4)]

            RMC=RMC.split(bytes(",",'utf-8'))
            GGA = GGA.split(bytes(",", 'utf-8'))


            if len(RMC)>10 and len(GGA)>10:
                if (RMC[2])=='V':
                    print('No location found', '----/n')
                else:
                    self.latitude=RMC[3]+(RMC[4])
                    self.longitude = (RMC[5]) + (RMC[6])
                    self.altitude = (GGA[9]) + (GGA[10])
                    self.speed = (RMC[7])
                    self.course = (RMC[8])
                    self.satellite = GGA[7]
                    newLatitude=self.converter(str(self.latitude,'utf-8'))
                    newLongitude=self.converter(str(self.longitude,'utf-8'))
                    coordonates={'latitude':newLatitude,'longitude':newLongitude,'altitude':str(self.altitude,'utf-8'),'speed':str(self.speed,'utf-8'),'course':str(self.course,'utf-8'),'satellite':str(self.satellite,'utf-8')}

            return coordonates
        except SerialException:
            print('Droit d\' au peripherique insufisant ou numero de port incorrecte!')
            print('reconnection ... to /dev/ttyUSB1 ')
            self.path='/dev/ttyUSB1'
            self.usbPort = serial.Serial(self.path, self.baurate, timeout=self.timeout)
        except FileNotFoundError:
            print('Impossible de trouver le fihcier '+self.path+' veuillez branchez le module GPS')





# gps=Gpsaccess()
#
#
# while True:
#      print(gps.readCoordonates()  )



