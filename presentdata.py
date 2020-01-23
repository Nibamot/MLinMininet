#!/bin/env python
""" iperf3 changes made to avoid and regexlist"""
import re
import time

ind=0
avoid=['Sending', 'refused', 'datagrams', 'connecting', '--', '- -',
       'Interval', 'buffer', 'port', 'UDP', 'parameter', 'terminated',
       'Server', 'connection', 'iperf3', 'Kbits/sec']
with open("h1sh3c.txt", "r") as f:#iperftest h1sh2c
    try:
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
        regexlist = [r'ms', r'KBytes', r'Mbits/sec', r'Kbits/sec', r'MBytes', r'bits/sec',r'%',
                     r'^\[\s\d+\]', r'\d+\.\d+-\s*', r'\(', r'\)', r'\s+', r'\d+\/\d+',
                     r'Bytes', r'sec']
        leng = len(content)
        test = re.sub("|".join(regexlist)," ", content[leng-1])
        testcoma = re.sub(r'\s+', ",", test)
        testcomma = re.sub(r'^\,',"", testcoma)
        #print(testcomma)
        #newcontent.append(testcomma)
        with open("pdata1.txt", "w") as f2:
            #print(testcomma)
            f2.write("%s\n" %testcomma)
        f2.close()
    except IndexError:
        pass
    f.close()
