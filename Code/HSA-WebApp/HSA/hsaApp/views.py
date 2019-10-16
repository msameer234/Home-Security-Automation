# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

import sys

import io
##import logging
##import socketserver
##from threading import Condition
##from http import server

import RPi.GPIO as gpio
import picamera
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

fromaddr = "YourEmail" # change this
toaddr = "YourEmail" # change this

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
    server.login(fromaddr,"YourPassword") # change this
    text = mail.as_string()
    server.sendmail(fromaddr,toaddr,text)
    print("Senddddd..")
    server.quit()

def capture_image():
    camera = picamera.PiCamera()
    data = time.strftime("%d_%b_%Y|%H:%M:%S")
    camera.start_preview()
    time.sleep(1)
    print(data)
    camera.capture('/home/pi/Desktop/cam/%s.jpg'%data)
    print('Image Captured')
    camera.stop_preview()
    print('camera preview stopped')
    time.sleep(0.5)
    print("Sending image to Email")
##    sendMail(data)
    print('Closing camera')
    time.sleep(1)
    camera.close()
    print("Image Sent..!!!")
    print("Press CTRL+C to stop monitoring\n\n")
    print("------------------------------------------")


def record_video(length):
    camera = picamera.PiCamera()
    data = time.strftime("%d_%b_%Y|%H:%M:%S")
    camera.start_preview()
    time.sleep(1)
    print(data)
    duration = int(length)
    camera.start_recording('/home/pi/Desktop/videos/%s.h264'%data)
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



def stopMonitoring():
##    camera = picamera.PiCamera()
##    camera.stop_preview()
##    camera.close()
##    startMonitoring.monitoring = False
##    gpio.output(led,0)
##    gpio.output(buz,0)

    return HttpResponse("Monitoring Stopped")

    
def startMonitoring(request):
    
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
            capture_image()
        else:
            gpio.output(led,0)
            gpio.output(buz,0)
        time.sleep(0.1)

def Monitoring(request):


    time.sleep(2)
    print("------------------------------------------")
    print("Monitoring Mode")
    
##    mStatus = "Off"
##    print(mStatus)
    print("Press CTRL+C to stop monitoring")
    monitoring = True
##    if request.method == 'POST':
##            mStatus = (request.POST['mmradio'])
##            print(mStatus)
##            if mStatus=="On":
##                monitoring = True
    while monitoring:
##        if mStatus == "On":
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
                capture_image()
            else:
                gpio.output(led,0)
                gpio.output(buz,0)
##        else:
##            monitoring = False
##            break
            
##        time.sleep(0.1)
    print("end of loop")
    status = 'Monitoring Started'
    context = {status:'status'}
    template = 'index.htm'
    return render(request, template, context)

def capimgrecvid(request):    
    context = {}
    template = 'capimgrecvid.htm'
    return render(request, template, context)

def capimg(request):
    capture_image()
    context = {}
    template = 'capimg.htm'
    return render(request, template, context)

def recvid(request):
    template = 'recvid.htm'
    if request.method == 'POST':
        vidlength = (request.POST['vidlen'])
        record_video(vidlength)
        template = 'videorecorded.htm'
    context = {}    
    return render(request, template, context)
    
def videorecorded(request):      
    context = {}
    template = 'videorecorded.htm'
    return render(request, template, context)


def home(request):    
    context = {}
    template = 'index.htm'
    return render(request, template, context)

def turnOn(request):
    gpio.output(led,1)
    return home(request)

def turnOff(request):
    gpio.output(led,0)
    return home(request)
