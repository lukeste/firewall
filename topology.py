#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.link import TCLink

class final_topo(Topo):
  def build(self):
    # Campus network hosts
    h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='10.1.1.10/24',defaultRoute="h1-eth0")
    h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='10.1.1.11/24',defaultRoute="h2-eth0")
    h3 = self.addHost('h3',mac='00:00:00:00:00:03',ip='10.1.1.12/24',defaultRoute="h3-eth0")
    h4 = self.addHost('h4',mac='00:00:00:00:00:04',ip='10.1.1.13/24',defaultRoute="h4-eth0")

    # Home network hosts
    d1 = self.addHost('d1',mac='00:00:00:00:00:05',ip='10.2.2.10/24',defaultRoute="d1-eth0")
    d2 = self.addHost('d2',mac='00:00:00:00:00:06',ip='10.2.2.11/24',defaultRoute="d2-eth0")

    # Computing cluster hosts
    CCServer1 = self.addHost('CCServer1',
                             mac='00:00:00:00:00:07',
                             ip='10.3.3.1/29',
                             defaultRoute="CCServer1-eth0")
    CCServer2 = self.addHost('CCServer2',
                             mac='00:00:00:00:00:08',
                             ip='10.3.3.2/29',
                             defaultRoute="CCServer2-eth0")

    # Switches
    s1 = self.addSwitch('s1') 
    s2 = self.addSwitch('s2') 
    s3 = self.addSwitch('s3') 
    s4 = self.addSwitch('s4') 
    s5 = self.addSwitch('s5') 

    # Campus network links
    self.addLink(s1, h1, port1=8, port2=0, bw=3)
    self.addLink(s1, h2, port1=9, port2=0, bw=3)
    self.addLink(s1, h3, port1=10, port2=0, bw=3)
    self.addLink(s1, h4, port1=11, port2=0, bw=3)
    
    # Home network links
    self.addLink(s3, d1, port1=1, port2=0, bw=3)
    self.addLink(s3, d2, port1=2, port2=0, bw=3)

    # CCServer links
    self.addLink(s4, CCServer1, port1=1, port2=0, bw=10)
    self.addLink(s5, CCServer2, port1=1, port2=0, bw=3)

    # Switch-switch links
    self.addLink(s1, s2, port1=1, port2=1, bw=3)
    self.addLink(s1, s3, port1=2, port2=3, bw=3)
    self.addLink(s1, s5, port1=3, port2=2, bw=3)
    self.addLink(s2, s4, port1=2, port2=2, bw=3)
    self.addLink(s4, s5, port1=3, port2=3, bw=3)
    self.addLink(s3, s5, port1=4, port2=4, bw=3)

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController, link=TCLink)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
