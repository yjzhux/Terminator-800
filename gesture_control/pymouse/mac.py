from Quartz import *
from AppKit import NSEvent
from base import PyMouseMeta, PyMouseEventMeta

pressID = [None, kCGEventLeftMouseDown, kCGEventRightMouseDown, kCGEventOtherMouseDown]
releaseID = [None, kCGEventLeftMouseUp, kCGEventRightMouseUp, kCGEventOtherMouseUp]

class PyMouse(PyMouseMeta):
    def press(self, x, y, button = 1):
        event = CGEventCreateMouseEvent(None, pressID[button], (x, y), button - 1)
        CGEventPost(kCGHIDEventTap, event)

    def release(self, x, y, button = 1):
        event = CGEventCreateMouseEvent(None, releaseID[button], (x, y), button - 1)
        CGEventPost(kCGHIDEventTap, event)

    def move(self, x, y):
        move = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), 0)
        CGEventPost(kCGHIDEventTap, move)
        

    def position(self):
        loc = NSEvent.mouseLocation()
        return loc.x, CGDisplayPixelsHigh(0) - loc.y

    def screen_size(self):
        return CGDisplayPixelsWide(0), CGDisplayPixelsHigh(0)

class PyMouseEvent(PyMouseEventMeta):
    def run(self):
        tap = CGEventTapCreate(
            kCGSessionEventTap,
            kCGHeadInsertEventTap,
            kCGEventTapOptionDefault,
            CGEventMaskBit(kCGEventMouseMoved) |
            CGEventMaskBit(kCGEventLeftMouseDown) |
            CGEventMaskBit(kCGEventLeftMouseUp) |
            CGEventMaskBit(kCGEventRightMouseDown) |
            CGEventMaskBit(kCGEventRightMouseUp) |
            CGEventMaskBit(kCGEventOtherMouseDown) |
            CGEventMaskBit(kCGEventOtherMouseUp),
            self.handler,
            None)

        loopsource = CFMachPortCreateRunLoopSource(None, tap, 0)
        loop = CFRunLoopGetCurrent()
        CFRunLoopAddSource(loop, loopsource, kCFRunLoopDefaultMode)
        CGEventTapEnable(tap, True)

        while self.state:
            CFRunLoopRunInMode(kCFRunLoopDefaultMode, 5, False)

    def handler(self, proxy, type, event, refcon):
        (x, y) = CGEventGetLocation(event)
        if type in pressID:
            self.click(x, y, pressID.index(type), True)
        elif type in releaseID:
            self.click(x, y, releaseID.index(type), False)
        else:
            self.move(x, y)
        
        if self.capture:
            CGEventSetType(event, kCGEventNull)

        return event
