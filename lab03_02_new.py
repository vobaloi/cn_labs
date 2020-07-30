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
    r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4 = net.addHost('r4', cls=Node, ip='0.0.0.0')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='172.30.0.101/16', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='172.30.0.102/16', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='192.168.0.101/24', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='192.168.0.102/24', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(s1, h2)
    net.addLink(h3, s2)
    net.addLink(s2, h4)
    net.addLink(r4, s2)
    net.addLink(r3, s1)
    net.addLink(r3, r4)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])
    net.get('s2').start([])

    info( '*** Post configure switches and hosts\n')
    r3.cmd('ifconfig r3-eth0 172.30.0.1 netmask 255.255.0.0 up')
    r3.cmd('ifconfig r3-eth1 10.10.0.1 netmask 255.0.0.0 up')
   
    r4.cmd('ifconfig r4-eth0 192.168.0.1 netmask 255.255.255.0 up')
    r4.cmd('ifconfig r4-eth1 10.10.0.2 netmask 255.0.0.0 up')
    
    h1.cmd('route add default gw 172.30.0.1')
    h2.cmd('route add default gw 172.30.0.1')
    h3.cmd('route add default gw 192.168.0.1')
    h4.cmd('route add default gw 192.168.0.1')
    
    r3.cmd('route add -net 172.30.0.0/16 gw 172.30.0.1')
    r3.cmd('route add -net 192.168.0.0/24 gw 10.10.0.2')
    #r3.cmd('route add -net 10.0.0.0/8 gw 10.10.0.1')
	
    r4.cmd('route add -net 192.168.0.0/24 gw 192.168.0.1')
    r4.cmd('route add -net 172.30.0.0/16 gw 10.10.0.1')
    #r4.cmd('route add -net 10.0.0.0/8 gw 10.10.0.2')
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

vobaloi