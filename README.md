## Cloudy Loot
Cloudy-loot is a tool to look for common cloud tools, configuration files, keys, and secrets.  It is not meant to be all encompassing, but will hopefully help speed up the process.

It may be useful being run after breaking out of container, getting a shell on a webapp or if you have compromised a linux host.

### Usage:

```
usage: cloudyloot.py [-h] [-A] [-e] [-i] [-k] [-t] [-C] [-c] [-m] [-o OUTFILE] [--debug]

Cloudy Loot - Host enumeration tool, specifically looking for cloud loot

optional arguments:
  -h, --help            show this help message and exit
  -A, --all             Run all Enumeration
  -e, --env             Print ENV
  -i, --iptables        List IPTables rules
  -k, --keyfiles        Identify Key files
  -t, --tools           Identify Cloud Tools
  -C, --credfiles       Identify Credential Files
  -c, --containers      Enum Containers and orchestration
  -m, --metadata        Query Metadata Endpoints
  -o OUTFILE, --outfile OUTFILE
                        File Name to Log to
```

### Example

```
python3 cloudy-loot.py -A -o output.txt
[+] ----- OS ----- 
OS_Info: posix.uname_result(sysname='Linux', nodename='ubuntu', release='5.13.0-28-generic', version='#31~20.04.1-Ubuntu SMP Wed Jan 19 14:08:10 UTC 2022', machine='x86_64')
<snip>
[+] ----- Key Files ----- 
Keyfile: /home/ubuntu/.minikube/machines/minikube/id_rsa.pub
Keyfile: /home/ubuntu/.minikube/machines/minikube/id_rsa
[+] ----- Cloud Tools ----- 
<snip>
```
