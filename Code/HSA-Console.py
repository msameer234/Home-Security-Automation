import sys

import io
##import socket
##import netifaces as ni
import logging
import socketserver
from threading import Condition
from http import server

import RPi.GPIO as gpio
import picamera
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

fromaddr = "samirmalik570@gmail.com"
toaddr = "samirmalik570@gmail.com"

mail = MIMEMultipart()

mail["From"] = fromaddr
mail["To"] = toaddr
mail["Subject"] = "Attactment"
body = "Please find the attachment"

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

led = 18
gpio.setup(led,gpio.OUT)

btn = 16
gpio.setup(btn,gpio.IN,pull_up_down=gpio.PUD_UP)

pir = 7
gpio.setup(pir,gpio.IN)

buz = 3
gpio.setup(buz,gpio.OUT)

HIGH = 1
LOW = 0


data = ""

gpio.output(led,0)
gpio.output(buz,0)

def sendMail(data):    
    mail.attach(MIMEText(body,'plain'))
    print(data)
    dat = '%s.jpg'%data
    print(dat)
    attachment = open(cam/dat,'rb')
    image = MIMEImage(attachment.read())
    attachment.close()
    mail.attach(image)
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(fromaddr,"Samstag@000")
    text = mail.as_string()
    server.sendmail(fromaddr,toaddr,text)
    print("Image Sent..!!!")
    server.quit()

def capture_image():
    camera = picamera.PiCamera()
    data = time.strftime("cam/%d_%b_%Y_%H:%M:%S")
    camera.start_preview()
    time.sleep(1)
    print(data)
    camera.capture('%s.jpg'%data)
    print('Image Captured')
    camera.stop_preview()
    print('camera preview stopped')
    time.sleep(0.5)
    print("Sending image to Email")
    try:
        sendMail(data)
    except:
        print('Could not send the Email..!')
    finally:
        print('Closing camera')
        time.sleep(1)
        camera.close()
    print("Press CTRL+C to stop monitoring\n\n")
    print("------------------------------------------")


def record_video():
    camera = picamera.PiCamera()
    data = time.strftime("videos/%d_%b_%Y_%H:%M:%S")
    camera.start_preview()
    time.sleep(1)
    print(data)
    duration = int(input("Video Duration(In Seconds): "))
    camera.start_recording('%s.h264'%data)
    print('[-] Recording Video')
    time.sleep(duration)
    camera.stop_recording()
    print('[-] Video recorded successfully')
    camera.stop_preview()
    print('camera preview stopped')
    time.sleep(0.5)
##    print("Sending image to Email")
##    sendMail(data)
    print('Closing camera')
    time.sleep(1)
    camera.close()
##    print("Image Sent..!!!")
##    print("Press CTRL+C to stop monitoring\n\n")
    print("------------------------------------------")



    
def startMonitoring():    
    time.sleep(2)
    print("------------------------------------------")
    print("Monitoring Mode")
    monitoring = True
    print("Press CTRL+C to stop monitoring")
    while monitoring:
        if gpio.input(pir) == 1:
            print('Motion Detected')
            gpio.output(led,1)
            gpio.output(buz,1)
            capture_image()
            while(gpio.input(pir)):
                time.sleep(1)
        elif gpio.input(btn) == 0:
            print('Button Pressed')
            gpio.output(led,1)
            gpio.output(buz,1)
            time.sleep(0.5)
            gpio.output(led,0)
            gpio.output(buz,0)
            time.sleep(0.2)
            gpio.output(led,1)
            gpio.output(buz,1)
            time.sleep(0.5)
            gpio.output(led,0)
            gpio.output(buz,0)
            capture_image()
        else:
            gpio.output(led,0)
            gpio.output(buz,0)
        time.sleep(0.1)

PAGE="""\
            <html>
            <head>
            <title>Raspberry Pi - Surveillance Camera</title>
            </head>
            <body>
            <center><h1>Raspberry Pi - Surveillance Camera</h1></center>
            <center><img src="stream.mjpg" width="640" height="480"></center>
            </body>
            </html>
            """ 


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

output = StreamingOutput()


def main():
    print("\nWelcome to HOME SECURITY AUTOMATION\n")
    options = """ OPTIONS:
        1. START MONITORING
        2. CAPTURE IMAGE
        3. RECORD VIDEO
        4. STREAM LIVE

        PRESS CTRL+C TO EXIT"""
    try:
        print(options)
        choice = int(input("Select your option(1-4): "))
        if choice == 1:
            try:
                startMonitoring()
            finally:
                print("Monitoring Stopped.\n")
                gpio.output(led,0)
                gpio.output(buz,0)
                main()
        elif choice == 2:
            try:
                capture_image()
            finally:
                gpio.output(led,0)
                gpio.output(buz,0)
                main()
        elif choice == 3:
            try:
                record_video()
            finally:
                gpio.output(led,0)
                gpio.output(buz,0)
                main()
        elif choice == 4:
            with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
                
                #Uncomment the next line to change your Pi's Camera rotation (in degrees)
                #camera.rotation = 90
                camera.start_recording(output, format='mjpeg')
                try:
                    address = ('', 8000)
                    server = StreamingServer(address, StreamingHandler)
                    server.serve_forever()
                finally:
                    camera.stop_recording()
                    camera.close()
                    main()
        else:
            main()

    except:
        print('Exit Successfully')
    finally:
        gpio.output(led,0)
        gpio.output(buz,0)
        gpio.cleanup()


main()
