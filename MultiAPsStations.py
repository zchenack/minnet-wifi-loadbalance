# -*- coding: utf-8 -*-
"""
Test bandwidth for Multi-Stations of Multi-APs

@author: chenze

"""
from mininet.net import Mininet
from mininet.node import Controller,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import numpy as np

def Topology(n,m):
    '''
    产生网络拓扑图
    '''
    #Create a network
    net = Mininet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )
    N = m+n
    Position = Rand_Position(N)
    IP_ADD = Create_IP(N)
    MAC_ADD = Create_MAC(N)
    #用来产生AP节点
    APs = []
    for i in range(m):
        ap_tmp = net.addBaseStation( 'ap%s'%(i+1),ssid= 'my-ssid', mode= 'g', channel= '1', position=Position[i] )
        APs.append(ap_tmp)
        
    #用来产生Station节点
    STAs = []
    for i in range(n):
        sta_tmp = net.addStation( 'sta%s'%(i+1), mac=MAC_ADD[i], ip=IP_ADD[i], position=Position[m+i] )
        STAs.append(sta_tmp)

    #产生Host节点
    Hosts = []
    for i in range(m):
        host_tmp = net.addHost('h%s'%(i+1),ip=IP_ADD[i+n])
        Hosts.append(host_tmp)
    
    
    print "*** Creating links"
    net = Access_Control(STAs,APs,net)
    for i in range(m-1):
        net.addLink(APs[i],APs[i+1])
        net.addLink(APs[i],Hosts[i])
    net.addLink(APs[m-1],Hosts[m-1])
    
    c1 = net.addController( 'c1', controller=Controller )
    print "*** Starting network"
    net.build()
    c1.start()
    for i in range(m):
        APs[i].start( [c1] )
    #测量吞吐量
    Hosts[0].cmd('iperf -s')
    STAs[0].cmd('iperf -c 10.0.0.21')
    print "iperf done"
    #for i in range(n):
    #    net.iperf([STAs[i],Hosts[0]],seconds=10)
    #BandWidth = net.iperf([STAs[0],Hosts[2]],seconds=10)
    #print BandWidth
    net.plotGraph(max_x=100, max_y=100)

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

def Rand_Position(n):
    '''
    产生随机坐标值
    '''
    L = 3 #三维坐标值
    Pos = []
    for i in range(n):
        tmp_pos = ''
        for j in range(L-1):
            dat = np.random.uniform(0,100)
            tmp_pos+=str(dat)
            tmp_pos+=','
        tmp_pos+='0'
        Pos.append(tmp_pos)
    return Pos

def Access_Control(STAs,APs,net):
    '''
    用于连接Stations 和APs
    '''
    n = len(STAs) #number of stations
    m = len(APs)  #number of APs
    for i in range(n):
        tmp_dist = []
        for j in range(m):
            tmp_dist.append(cal_dist(STAs[i],APs[j]))
        min_dist = min(tmp_dist)
        ind = tmp_dist.index(min_dist)
        net.addLink(STAs[i],APs[ind])
    return net

def Create_IP(n):
    '''
    产生IP地址
    '''
    Address = '10.0.0.'
    ip_add = []
    for i in range(1,n+1):
        ip_add.append(Address+str(i)+'/8')
    return ip_add

def Create_MAC(n):
    '''
    产生MAC地址
    '''
    Address1 = '00:00:00:00:00:'
    Address2 = '00:00:00:00:00:0'
    MAC_add = []
    for i in range(1,n+1):
        tmp_str = str(hex(i))[2:]
        if len(tmp_str)==1:
            MAC_add.append(Address2+tmp_str)
        else:
            MAC_add.append(Address1+tmp_str)
    return MAC_add

def cal_dist(sta,ap):
    '''
    用于计算Station与AP之间的距离
    '''
    pos_sta = map(float,sta.params['position'])
    pos_ap = map(float,ap.params['position'])
    dist = 0.0
    L = len(pos_sta)
    for i in range(L):
        dist += (pos_sta[i]-pos_ap[i])**2
    return np.sqrt(dist)
    
if __name__=='__main__':
    m = 4 #AP数量
    n = 20 #STA数量
    setLogLevel( 'info' )
    Topology(n,m)
