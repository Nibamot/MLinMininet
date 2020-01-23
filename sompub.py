from pox.core import core
from pox.lib.revent import *
import pox
import time
import threading
import pox.openflow.libopenflow_01 as of

class SomEvent(Event):
  def __init__(self):
    Event.__init__(self)
    print "SomEvent is initialized"

class Publisher(EventMixin):
  """
  This is a Class for Publisher which can raise an event
  """
  _eventMixin_events = set([SomEvent,])
  def __init__(self):
    self.listenTo(core)
    print "Publisher is initialised\n"


  def _handle_GoingUpEvent(self, event):
    self.listenTo(core.openflow)
    print "this is in publisher, what is this for?\n"

  def publishEvent(self):
    print "publishEvent is called, will raise the test Event\n"
    self.raiseEvent(SomEvent,)
    print "foo raised event\n"

  def _handle_PacketIn(self,event):
    print "PacketIn event is raised,packetIn\n"
    print "\npacket destination "+str(event.parsed.dst)+"\n"+\
          "The DPID is "+str(event.dpid)+"\n The in-port is "+str(event.port)+"\n"
    if event.dpid == 1:
        self.publishEvent()
    return

def launch():
  core.registerNew(Publisher)
