# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 10:39:07 2016

@author: dell
"""

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import  Controller, OVSKernelSwitch, RemoteController, UserSwitch
from mininet.wmediumdConnector import WmediumdConn, WmediumdLink, StaticWmediumdIntfRef

def topology():
    """
    create network
    STAs and AP
    """
    print "***network created"
    net = Mininet()
    
    print "***Configure wmediumd"
    APwlan0 = StaticWmediumdIntfRef('AP','AP-wlan0','02:00:00:00:00:00')
    sta1wlan0 = StaticWmediumdIntfRef('sta1', 'sta1-wlan0', '02:00:00:00:01:00')
    sta2wlan0 = StaticWmediumdIntfRef('sta2', 'sta2-wlan0', '02:00:00:00:01:00')
    
    intfrefs = [sta1wlan0,APwlan0,sta2wlan0]
    links = [
             WmediumdLink(sta1wlan0, APwlan0, 15),
             WmediumdLink(APwlan0, sta1wlan0, 15),
             WmediumdLink(sta2wlan0, APwlan0, 15),
             WmediumdLink(APwlan0, sta2wlan0, 15)]
    WmediumdConn.set_wmediumd_data(intfrefs, links)
    WmediumdConn.connect_wmediumd_on_startup()
    
    print "*** Creating nodes"
    AP = net.addAccessPoint('AP',ssid="ssid_AP",mode="g",channel="5")
    sta1 = net.addStation('sta1')
    sta2 = net.addStation('sta2')
    c0 = net.addController('c0', controller=Controller, ip='127.0.0.1' )

#    print "*** Adding Link"
#    net.addLink(sta1, AP, bw=10, loss=20)
#    net.addLink(sta2, AP)
    
    print "*** Starting network"
    
    net.build()
    c0.start()
    AP.start([c0])
    
    print "*** Running CLI"
    CLI(net)
    
    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()