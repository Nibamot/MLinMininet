import time
import os

import pox
import pox.openflow.libopenflow_01 as of
from pox.core import core
from pox.lib.revent import *
from pox.lib.util import str_to_bool
from pox.lib.util import dpidToStr
from pox.openflow.discovery import Discovery
from pox.openflow.discovery import Link
from pox.lib.addresses import IPAddr


import numpy as np
#np.set_printoptions(threshold=np.inf)
import sompy
from sompy.sompy import SOMFactory
from decorator import timeit

log = core.getLogger()
#check from Discovery
def _handle_LinkEvent (event):
    pass

class SomSwitch(object):
  def __init__ (self, connection, transparent):
    # Switch we'll be adding L2 learning switch capabilities to
    self.connection = connection
    self.transparent = transparent
    self.pktin = None

    connection.addListeners(self)

  def _handle_PacketIn (self, event):
      pkt = event.parsed
      log.debug(str(pkt)+" packets came on "+str(event.port)+"\n")


class Subscriber(EventMixin):

  def __init__(self, transparent):
    self.listenTo(core)
    self.count = 0
    self.links = [Link(dpid1=1,port1=2, dpid2=2,port2=2), Link(dpid1=2,port1=2, dpid2=1,port2=2)]
    core.openflow.addListeners(self)
    self.transparent = transparent
    self.now = time.time()
    self.prevpred = 0.0
    self.details = open("Accuracy"+str(time.time())+".txt", "w")
    self.details.write("Loss(%)\t"+"Throughput\t"+"Prediction\t"+"Error\t"+"Actual\t"+"Verdict\n")

  def _handle_ConnectionUp (self, event):
    log.debug("ConnectionGO %s" % (event.connection,))
    self.connection = event.connection
    SomSwitch(event.connection, self.transparent)

  def _handle_PacketIn (self, event):
      self.pkt = event
      self.packetparsed = event.parsed

  def _handle_GoingUpEvent (self, event):
    self.listenTo(core.Publisher)
    log.debug("Subscriber going up!\n")



  def _handle_SomEvent(self,event):
    print "Som Event is raised,I heard SomEvent\n"
    #log.debug(str(core.openflow_discovery.adjacency)+" LINKS\n")
    self.count+=1

    print("NUMBER OF PACKETS IN "+str(self.count))
    if time.time()-self.now >= 5.0:#if self.count % 30 == 0:
        if os.stat('/home/mininet/testmininet/trainingdata1.txt').st_size != 0:
            self._prediction()
            self.now = time.time()
        else:
            pass

    return


  @timeit()
  def _prediction(self):
      """SOM function"""
      try:
          data = np.loadtxt('/home/mininet/testmininet/trainingdata1.txt', delimiter=',')
          names = ['Interval','Throughput(Mbits/0.5sec)','Bandwidth(Mbits/sec)','Jitter(ms)','Loss','Decision']

          sm = SOMFactory().build(data, normalization = 'var',
                                  initialization='random',
                                  component_names=names)

          sm.train(n_job=1, verbose='info', train_rough_len=15, train_finetune_len=15)

          topographic_error = sm.calculate_topographic_error()
          quantization_error = np.mean(sm._bmu[1])
          line = open('/home/mininet/testmininet/pdata1.txt').readlines()
          log.debug(line)
          comp = line[0].split(",")
          del comp[len(comp)-1]
          data2 = np.array([[float(comp[0]), float(comp[1]), float(comp[2]), float(comp[3]), float(comp[4])]])
          sm.cluster(5)
          pred = np.absolute(sm.predict_by(data2, 5))

          self.details.write(comp[4]+"\t"+comp[1]+"\t"+str(pred[0])+"\t"+str(topographic_error)+"\n")
          print(pred)
          if pred <= 0.5:
              print("No congestion")
              self._congdelay(pred)
          elif pred > 0.5:
              print("Congestion there for next 5 seconds atleast")

          self.prevpred = pred
      except IndexError:
          print("ERROR")

  def _congdelay(self, pred):
      "To calculate cong time"
      slope = float(pred-self.prevpred)/5.0
      print("The rate of increase in congestion is "+str(slope))
      if slope >= 0.15 and slope < 0.20:
          log.debug("Congestion predicted in 5 seconds")



def launch(transparent=False):
  core.openflow_discovery.addListenerByName("LinkEvent", _handle_LinkEvent)
  core.registerNew(Subscriber, str_to_bool(transparent))
