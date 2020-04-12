#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='172.30.0.101/16', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='172.30.0.102/16', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='192.168.0.101/24', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='192.168.0.102/24', defaultRoute=None)
   

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(s1, h2)
    net.addLink(s1, r2)
    net.addLink(r2, s3)
    net.addLink(s3, h3)
    net.addLink(s3, h4)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])
    net.get('s3').start([])
   
    info( '*** Post configure switches and hosts\n')
    r2.cmd('ifconfig r2-eth0 172.30.0.1 netmask 255.255.0.0 up')
    r2.cmd('ifconfig r2-eth1 192.168.0.1 netmask 255.255.255.0 up')
    
    #h1.cmd('route add default gw 172.30.0.1')
    #h2.cmd('route add default gw 172.30.0.1')
    #h3.cmd('route add default gw 192.168.0.1')
    #h4.cmd('route add default gw 192.168.0.1')
    
    #r2.cmd('route add -net 172.30.0.0/16 gw 172.30.0.1')
    #r2.cmd('route add -net 192.168.0.0/24 gw 192.168.0.1')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

