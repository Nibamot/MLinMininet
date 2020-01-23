#!/usr/bin/env python

from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

def loadBalanceTest():
    """Test"""
    net = Mininet(topo=None, host=CPULimitedHost, link=TCLink)#TClink required , controller=RemoteController
    # for opts in addLink
    net.addController(name='poxc0', controller=RemoteController)#only 1 remotecontroller needed not in construct as well
    switch1 = net.addSwitch('s1')
    switch2 = net.addSwitch('s2')


    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')


    net.addLink(switch1, h1)# bw=10, delay='0ms', loss=2
    net.addLink(switch1, h2)
    net.addLink(switch2, h3)
    net.addLink(switch2, h4)
    net.addLink(switch1, switch2)
    net.start()
    #print(h2.cmd("iperf -c 10.0.0.1 -b 10m -t 100"))
    #print(h1.cmd("iperf -s -u -i 1 >> dev_sda3/h1sh2c.txt | python datatrim.py"))

    #dumpNodeConnections(net.hosts)
    CLI(net)
    #net.pingAll()
    #net.iperf( ( net.h1, net.h4 ), l4Type='UDP' )
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    loadBalanceTest()
#iperf -c 10.1.1.1 -u -b 10m at client with server address
#iperf -s -u -i 1 at server i is dor report interval
