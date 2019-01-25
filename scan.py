#!/usr/bin/env python

from myutils.mytools import get_input
import time
from random import randrange
import threading
import requests
import ipaddress as ip
from pymongo import MongoClient

some_database = MongoClient().some_database
some_collection = some_database.some_collection


def get_network():
    net = get_input("Please provide the network you wish to scan (ex. 192.168.20.0/24): ")
    try:
        network = ip.IPv4Network(net)
    except ["AddressValueError", "NetmaskValueError", "ValueError"] as e:
        print(f"You screwed up somewhere!\n{e}\nTry again!\n")
        get_network()
    return network


'''
AddressValueError: If ipaddress isn't a valid IPv4 address.
NetmaskValueError: If the netmask isn't valid for
  an IPv4 address.
ValueError: If strict is True and a network address is not
  supplied.
'''


def randhost():
    a = randrange(256)
    b = randrange(256)
    c = randrange(256)
    d = randrange(256)
    return '%i.%i.%i.%i' % (a, b, c, d)

def host_countdown(net_begin=None):
    if net_begin:
        subnet_begin = net_begin.split('.0')[0]

def process(host, port):
    if port == 80:
        url = 'http://%s' % host
    elif port == 443:
        url = 'https://%s' % host
    else:
        url = 'http://%s:%i' % (host, port)
    req = requests.get(url, timeout=1)
    doc = {'host': host, 'port': port, 'headers': dict(req.headers)}
    some_collection.insert_one(doc)

def scanloop():
    while True:
        host = randhost()
        try:
            process(host, 80)
        except:
            pass

threadcount = 100

threads = []

for i in xrange(threadcount):
    thread = threading.Thread(target=scanloop)
    thread.daemon = True
    thread.start()
    threads.append(thread)

while threading.active_count() > 0:
    time.sleep(0.1)
