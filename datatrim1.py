#!/bin/env python
""" iperf3 changes made to avoid and regexlist"""
import re
import sys


threshold = 6.0
avoid=['Sending', 'refused', 'datagrams', 'connecting', '--', '- -',
       'Interval', 'buffer', 'port', 'UDP', 'parameter', 'terminated',
       'Server', 'connection', 'iperf3', 'Kbits/sec']
ind=0
file = str(sys.argv)
with open("h1sh3c.txt", "r") as f:#iperftest h1sh2c
    content = f.readlines()

    count = 0
    while ind < len(content):
        for x in avoid:
            if x in content[ind]:
                del content[ind]
                ind = 0
                count = 0
                x = avoid[0]
                break
        if  ind == len(content)-1 and ind != 0:
            if count != 1:
                ind = 0
                count = 1
            else:
                break
        else:
            ind+=1

    if len(content) is not 0:
        del content[len(content)-1]

    #REGEX shit

    newcontent = []
    regexlist = [r'ms', r'KBytes', r'Mbits/sec', r'Kbits/sec', r'MBytes', r'bits/sec',r'%',
                 r'^\[\s\d+\]', r'\d+\.\d+-\s*', r'\(', r'\)', r'\s+', r'\d+\/\d+',
                 r'Bytes', r'sec']

    for lines in content:
        test = re.sub("|".join(regexlist)," ", lines)
        testcoma = re.sub(r'\s+', ",", test)
        testcomma = re.sub(r'^\,',"", testcoma)
        #print(testcomma)
        newcontent.append(testcomma)
    with open("data1.txt", "w") as f2:

        for data in newcontent:
            s = data.split(",")
            lensize = len(s)
            if (float(s[lensize-2])) >= threshold or (float(s[1]) == 0.0):
                data+='1'
            else:
                data+='0'
            print(data)
            f2.write("%s\n" %data)
        f2.close()
    f.close()
