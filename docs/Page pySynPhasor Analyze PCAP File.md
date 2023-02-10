---
layout: default
title: Analyze PCAP File 
nav_order: 5
---

If you already have network traffic files(.pcap) captured by Wireshark,  then you can analyze the packet using pySynphasor as follows 

```python
pkts = rdpcap('synphasor_pkts.pcap') #change the pcap file 
count = 0
total = 0
for pkt in pkts:
    total += 1
    if synphasor in pkt:
        count += 1
print('Total Packets: ' + str(total))
print('Total IEEE C37.118 packets: '+ str(count))
```

Output
```python
Total Packets: 10 
Total IEEE C37.118 packets: 10
```

## Dissect First Packet
Now, to see the contents of the first packet
```python
#Check if the packet is synphasor type
if synphasor in pkts[0]:
    pkts[0].show()
else:
    print("The packet is not a Synchrophasor type")
```

Output looks like as follows. The first packet is the command type packet
```python
###[ Loopback ]### 
  type      = IPv4
###[ IP ]### 
     version   = 4
     ihl       = 5
     tos       = 0x0
     len       = 58
     id        = 36829
     flags     = DF
     frag      = 0
     ttl       = 128
     proto     = tcp
     chksum    = 0x0
     src       = 127.0.0.1
     dst       = 127.0.0.1
     \options   \
###[ TCP ]### 
        sport     = 1520
        dport     = 4712
        seq       = 3473346746
        ack       = 3518961130
        dataofs   = 5
        reserved  = 0
        flags     = PA
        window    = 10233
        chksum    = 0xf354
        urgptr    = 0
        options   = []
###[ IEEE C37.118.2 COMMON FRAME ]### 
           synByte   = 0xaa
           reserved  = 0
           type      = CMD
           version   = Version 1
           framesize = 18
           idcode    = 7
           soc       = 1642040610
           fracsec   = 50238
###[ synphasor command ]### 
              cmd       = 1
              chk       = 0x590a
```


## Dissect Third Packet

```python
pkts[2].show()
```

This is a configuration type of packet
```
###[ Loopback ]### 
  type      = IPv4
###[ IP ]### 
     version   = 4
     ihl       = 5
     tos       = 0x0
     len       = 494
     id        = 36837
     flags     = DF
     frag      = 0
     ttl       = 128
     proto     = tcp
     chksum    = 0x0
     src       = 127.0.0.1
     dst       = 127.0.0.1
     \options   \
###[ TCP ]### 
        sport     = 4712
        dport     = 1520
        seq       = 3518961130
        ack       = 3473346782
        dataofs   = 5
        reserved  = 0
        flags     = PA
        window    = 10233
        chksum    = 0xa9d4
        urgptr    = 0
        options   = []
###[ IEEE C37.118.2 COMMON FRAME ]### 
           synByte   = 0xaa
           reserved  = 0
           type      = CFG2
           version   = Version 1
           framesize = 454
           idcode    = 7
           soc       = 1642040611
           fracsec   = 503942
###[ IEEE C37.118.2 CFG2 ]### 
              TIME_BASE = 1000000
              num_pmu   = 1
              \pmu       \
               |###[ PMU Configuration ]### 
               |  stn       = 'Station A       '
               |  idcode    = 7734
               |  unused    = 0
               |  freq      = 16-bit integer
               |  analog    = 32-bit IEEE floating point
               |  phasor_dtype= 16-bit integer
               |  phasor_format= rectangular
               |  phnmr     = 4
               |  annmr     = 3
               |  dgnmr     = 1
               |  phname    = ['VA              ', 'VB              ', 'VC              ', 'I1              ']
               |  anname    = ['ANALOG1         ', 'ANALOG2         ', 'ANALOG3         ']
               |  \dgname    \
               |   |###[ digital status name ]### 
               |   |  dname1    = 'BREAKER 1 STATUS'
               |   |  dname2    = 'BREAKER 2 STATUS'
               |   |  dname3    = 'BREAKER 3 STATUS'
               |   |  dname4    = 'BREAKER 4 STATUS'
               |   |  dname5    = 'BREAKER 5 STATUS'
               |   |  dname6    = 'BREAKER 6 STATUS'
               |   |  dname7    = 'BREAKER 7 STATUS'
               |   |  dname8    = 'BREAKER 8 STATUS'
               |   |  dname9    = 'BREAKER 9 STATUS'
               |   |  dname10   = 'BREAKER A STATUS'
               |   |  dname11   = 'BREAKER B STATUS'
               |   |  dname12   = 'BREAKER C STATUS'
               |   |  dname13   = 'BREAKER D STATUS'
               |   |  dname14   = 'BREAKER E STATUS'
               |   |  dname15   = 'BREAKER F STATUS'
               |   |  dname16   = 'BREAKER G STATUS'
               |  \phunit    \
               |   |###[ ('Phasor Conversion Factor',) ]### 
               |   |  flag      = voltage
               |   |  phfactor  = 915527
               |   |###[ ('Phasor Conversion Factor',) ]### 
               |   |  flag      = voltage
               |   |  phfactor  = 915527
               |   |###[ ('Phasor Conversion Factor',) ]### 
               |   |  flag      = voltage
               |   |  phfactor  = 915527
               |   |###[ ('Phasor Conversion Factor',) ]### 
               |   |  flag      = current
               |   |  phfactor  = 45776
               |  \anunit    \
               |   |###[ ('Analog Conversion Factor',) ]### 
               |   |  flag      = single point on wave
               |   |  anfactor  = 1
               |   |###[ ('Analog Conversion Factor',) ]### 
               |   |  flag      = rms of analog
               |   |  anfactor  = 1
               |   |###[ ('Analog Conversion Factor',) ]### 
               |   |  flag      = peak of analog
               |   |  anfactor  = 1
               |  \dgunit    \
               |   |###[ Digital Status Words ]### 
               |   |  normal_status= 0x0
               |   |  valid_input= 0xffff
               |  reserved  = 0
               |  fnom      = 60Hz
               |  CFGCNT    = 1
              data_rate = 1
              chk       = 0x7d07
```


## Dissect Fifth Packet

```python
pkts[4].show()
```

This packet is the data packet. The output is as follows:
```
###[ Loopback ]### 
  type      = IPv4
###[ IP ]### 
     version   = 4
     ihl       = 5
     tos       = 0x0
     len       = 92
     id        = 36845
     flags     = DF
     frag      = 0
     ttl       = 128
     proto     = tcp
     chksum    = 0x0
     src       = 127.0.0.1
     dst       = 127.0.0.1
     \options   \
###[ TCP ]### 
        sport     = 4712
        dport     = 1520
        seq       = 3518961584
        ack       = 3473346800
        dataofs   = 5
        reserved  = 0
        flags     = PA
        window    = 10233
        chksum    = 0x394c
        urgptr    = 0
        options   = []
###[ IEEE C37.118.2 COMMON FRAME ]### 
           synByte   = 0xaa
           reserved  = 0
           type      = DATA
           version   = Version 1
           framesize = 52
           idcode    = 7
           soc       = 1642040611
           fracsec   = 504940
###[ IEEE C37.118.2 Data ]### 
              \pmu_data  \
               |###[ PMU Data ]### 
               |  data_error= Good measurement
               |  pmu_sync  = sync with UTC
               |  data_storing= by time stamp
               |  pmu_trigger= no trigger
               |  cfg_change= change effected
               |  data_modified= otherwise
               |  pmu_time_quality= Not used
               |  unlocked_time= Sync locked or unlocked < 10s
               |  trigger_reason= Manual
               |  phasors   = [(14635+0j), (58218+52860j), (58218+12675j), (1092+0j)]
               |  freq      = 2500
               |  dfreq     = 0
               |  analogs   = [100.0, 1000.0, 10000.0]
               |  digitals  = [0x3c12]
              chk       = 0xc963
```



## References