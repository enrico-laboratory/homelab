#!/bin/bash

iptables -t nat -F
iptables -F

# Creating NAT
iptables -t nat -A POSTROUTING -s 192.168.100.0/24 -o ens16f0 -j SNAT --to-source 192.168.2.103

# Forwarding dns
# iptables -t nat -A PREROUTING -p udp --dport 53 -j DNAT --to-destination 192.168.100.52
