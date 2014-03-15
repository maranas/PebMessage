#
#  Cocoa_PythonAppDelegate.py
#  Cocoa-Python
#
#  Created by Moises Aranas on 3/9/12.
#  Copyright __MyCompanyName__ 2012. All rights reserved.
#

from Foundation import *
from AppKit import *
from objc import IBAction, IBOutlet
from PyObjCTools import AppHelper

import os
import json
import socket
import time
import threading
import urllib2
import webbrowser
import pebble as libpebble
import Queue
from itertools import izip

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

QUEUE_TIMEOUT = 10
DEFAULT_PORT = 3334

SUPPORTED_COMMANDS = ["sms", "email", "ping"]

message_queue = Queue.Queue()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print self.path
        try:
            head = self.path
            tail = None
            args = []
            (head, tail) = os.path.split(head)
            while(tail):
                if tail in SUPPORTED_COMMANDS:
                    break
                else:
                    tail = urllib2.unquote(tail)
                    args.insert(0, tail)
                tail = None
                (head, tail) = os.path.split(head)
            if tail in SUPPORTED_COMMANDS:
                i = iter(args)
                message_data = dict(izip(i, i))
                message_queue.put({"type": tail, "data": message_data})
                self.wfile.write("ok")
            else:
                self.wfile.write("not supported")
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    
    
    def do_POST(self):
        self.do_GET();

class Cocoa_PythonAppDelegate(NSObject):
    main_menu = IBOutlet()
    about_view = IBOutlet()
    about_item = IBOutlet()
    text_field = IBOutlet()
    connect_button = IBOutlet()
    connect_status = IBOutlet()
    
    is_running = True
    
    status_item = None
    tray_icon = None
    
    pebble = None
    
    pebble_id = "1234"
    
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
        self.is_running = True
        threading.Thread(target=self.task_loop).start()
        self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(-1)
        self.tray_icon = NSImage.alloc().initWithContentsOfFile_(NSBundle.mainBundle().pathForResource_ofType_("tray", "png"))
        self.status_item.setImage_(self.tray_icon)
        self.status_item.setHighlightMode_(True)
        self.status_item.setTarget_(self)
        self.status_item.setAction_("showMenu:")
        self.about_item.setTitle_("Settings...")
        # get the saved pebble id, if any
        self.pebble_id = NSUserDefaults.standardUserDefaults().objectForKey_("pebble_id")
        if (self.pebble_id):
            self.text_field.setStringValue_(self.pebble_id)
            threading.Thread(target=self.try_pairing).start()
        # start the server
        threading.Thread(target=self.startServer).start()

    def startServer(self):
        pool = NSAutoreleasePool.alloc().init()
        connected = False
        while not connected:
            try:
                server = HTTPServer(('', DEFAULT_PORT), RequestHandler)
                host_port = (socket.gethostbyname(socket.gethostname()), DEFAULT_PORT)
                print 'started httpserver (%s:%s)' % host_port
                self.about_item.setTitle_('Running on: %s:%s' % host_port)
                server.serve_forever()
                connected = True
            except KeyboardInterrupt:
                print 'Failed to start server, trying again in 30 seconds...'
                server.socket.close()
                time.sleep(30)
                connected = False
        del pool

    def try_pairing(self):
        pool = NSAutoreleasePool.alloc().init()
        attempts = 0
        while True:
            if attempts > 5:
                self.connect_status.setStringValue_("NOT CONNECTED! Enter your device ID below.")
                self.connect_button.setEnabled_(True)
            try:
                self.connect_status.setStringValue_("Connecting to the device...")
                self.connect_button.setEnabled_(False)
                self.pebble = libpebble.Pebble(self.pebble_id, False, True)
                self.connect_status.setStringValue_("CONNECTED!")
                # save the ID from the successful connect
                NSUserDefaults.standardUserDefaults().setObject_forKey_(self.pebble_id, "pebble_id")
                self.connect_button.setEnabled_(True)
                break
            except:
                time.sleep(5)
                attempts += 1
        del pool

    # COMMANDS

    def cmd_notification_email(self, pebble, sender, subject, body):
        if not pebble:
            return
        pebble.notification_email(sender, subject, body)

    def cmd_notification_sms(self, pebble, sender, body):
        if not pebble:
            return
        pebble.notification_sms(sender, body)

    def cmd_ping(self, pebble):
        if not pebble:
            return
        pebble.ping(cookie=0xDEADBEEF)

    # END COMMMANDS

    def task_loop(self):
        pool = NSAutoreleasePool.alloc().init()
        while self.is_running:
            inner_pool = NSAutoreleasePool.alloc().init()
            try:
                item = message_queue.get(QUEUE_TIMEOUT)
            except:
                continue
            if (item["type"] == "ping"):
                print "Processing ping!"
                self.cmd_ping(self.pebble)
            if (item["type"] == "sms"):
                print "Processing sms notification!"
                self.cmd_notification_sms(self.pebble, item["data"]["sender"], item["data"]["body"])
            if (item["type"] == "email"):
                print "Processing email notification!"
                self.cmd_notification_email(self.pebble, item["data"]["sender"], item["data"]["subject"], item["data"]["body"])
            del inner_pool
        del pool

    def showMenu_(self, arg):
        self.status_item.popUpStatusItemMenu_(self.main_menu)

    def applicationShouldTerminate_(self, sender):
        NSLog("Application is terminating.")
        self.is_running = False
        return NSTerminateNow

    @IBAction
    def quit_(self, arg):
        self.is_running = False
        AppHelper.callAfter(NSApp.terminate_, self)

    @IBAction
    def support_(self, arg):
        webbrowser.open("http://www.ganglionsoftware.com/contact.html")

    @IBAction
    def about_(self, arg):
        self.about_view.center()
        self.about_view.makeKeyAndOrderFront_(self)
        NSApp.activateIgnoringOtherApps_(True)

    @IBAction
    def pair_(self, arg):
        self.pebble_id = self.text_field.stringValue()
        threading.Thread(target=self.try_pairing).start()

    @IBAction
    def testPing_(self, arg):
        self.cmd_ping(self.pebble)

    @IBAction
    def testSMS_(self, arg):
        self.cmd_notification_sms(self.pebble, "Someone", "Someone texted you!")

    @IBAction
    def testEmail_(self, arg):
        self.cmd_notification_email(self.pebble, "Someone", "Re: Something", "Someone emailed you about something!")

