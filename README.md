PebMessage
==========

App for OSX that lets you pair your Pebble to your laptop/desktop running OSX, and allows you to send notifications from your computer to your Pebble watch.

This app uses libpebble and pyserial (see the app's info page for licensing information)

How to use:
-----------

PebMessage is nothing but a simple wrapper to the libpebble library. It runs a local http server which has a REST-like API, that you can use to queue messages for sending to your pebble.

To pair
-------

1. Pair your Pebble with your desktop via System Preferences->Bluetooth.
2. When paired, you will see the Pebble device's name. Take note of the last 4 digits, which will be your Pebble ID, e.g. if your watch's name is Pebble 1234 - 1234 is your pebble id
3. Run the PebMessage app. You will see a menu-bar icon. It will ask you to allow incoming network connections for the http server, allow it.
4. Click on the menu bar icon. You will see the host and port where the server is running. Click on that option to view the settings.
5. Enter the Pebble ID you noted down earlier, and click on the 'Connect' button. (Your pebble has to be unpaired; you can turn off your phone's Bluetooth so it will pair with your desktop)
6. Once paired, you can test sending messages to it by clicking on any of the test buttons.

Note: You will get asked to update to the latest Pebble app by your watch as soon as it pairs; it should still work though - it is still using libpebble which is written for SDK 1, but we will mostly be using just the notification system.

To send your own notifications
------------------------------

PebMessage supports sending 2 types of notifications for now: SMS-like messages or Email-like messages. Here are some sample requests - just replace the IP and Port with the one PebMessage is running on in your machine.

1. Sending an SMS-like message:

Just send a request with "sender" as string and "body" as string (both strings URL encoded):

    http://192.168.1.100:3334/sms/sender/Moises/body/Test%20Message

2. Sending an Email-like message:

Juse send a request with "sender" as string, "subject" as string and "body" as string (all strings are URL encoded):

    http://192.168.2.100:3334/email/sender/Moises/subject/Test%20Subject/body/Test%20Message

Credits (See the app for the licenses of the third-party libraries used)
------------------------------------------------------------------------
libpebble:
Copyright (C) 2013 Liam McLoughlin

pyserial:
Copyright (c) 2001-2013 Chris Liechti <cliechti@gmx.net>;
All Rights Reserved.

Icons:
Some icons by Yusuke Kamiyamane. http://p.yusukekamiyamane.com/

LICENSE
-------

Copyright (c) 2014 Moises Anthony Aranas

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
