#
#  main.py
#  Cocoa-Python
#
#  Created by Moises Aranas on 3/9/12.
#  Copyright __MyCompanyName__ 2012. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import Cocoa_PythonAppDelegate

# pass control to AppKit
AppHelper.runEventLoop()
