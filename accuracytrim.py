#!/bin/env python
""" Frills"""
import matplotlib.pyplot as plt
import numpy as np

threshold = 6.0
TPR = []
FPR = []
#decisionthreshold = 0.0
space = np.linspace(0,1,11)
print(space)
for decisionthreshold in space:
    totalP = 0
    totalTP = 0
    totalFP = 0
    totalN = 0
    totalTN = 0
    totalFN = 0

    with open("2020h1h3pred052.15.txt", "r") as f:
        with open("Accuracy.txt", "w") as f2:
            lines = f.readlines()
            for l in lines:
                if "Verdict" not in l:
                    det = l.replace("\n","")
                    ln = det.split("\t")

                    if 1:#float(ln[3]) <=0.80
                        if float(ln[0]) >= threshold or float(ln[1]) == 0.0:
                            det += "\tP\t"

                            if float(ln[2]) >= decisionthreshold and decisionthreshold < 1.0:
                                det += "TP\n"
                            else:
                                det += "FN\n"
                        elif float(ln[0]) < threshold:
                            det += "\tN\t"
                            if float(ln[2]) < decisionthreshold :
                                det += "TN\n"
                            else:
                                det += "FP\n"
                #else:
                    #print("Error")
                    totalP += det.count("\tP\t")
                    totalTP += det.count("TP")
                    totalFP += det.count("FP")
                    totalN += det.count("\tN\t")
                    totalTN += det.count("TN")
                    totalFN += det.count("FN")
                    f2.write("%s" %det)

    print(totalTP)
    TPR = np.append(TPR, (float(totalTP)/float(totalP)))
    FPR = np.append(FPR, (float(totalFP)/float(totalN)))
    print("Threshold = "+str(decisionthreshold)+"\n")
    print("TPR = "+str((float(totalTP)/float(totalP))))
    print("FPR = "+str((float(totalFP)/float(totalN))))
    print("TNR = "+str(float(totalTN)/float(totalN)))
    #print("PPV = "+str(float(totalTP)/(float(totalTP)+float(totalFP))))
    #print("NPV = "+str(float(totalTN)/(float(totalTN)+float(totalFN))))
    print("FNR = "+str(float(totalFN)/float(totalP)))
    print("Accuracy = "+str((float(totalTP)+float(totalTN))/(float(totalN)+float(totalP))))

#plt.ylim(0.0,1.0)
#plt.xlim(0.0,1.0)
plt.plot(FPR, TPR, marker='o')
plt.xlabel('False positve rate')
plt.ylabel('True positve rate')
plt.title('ROC')
plt.show()
auc = np.abs(np.trapz(TPR, FPR))
print(auc)
