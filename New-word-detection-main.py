
#Python 3
#Written by ValK

import math
import sys
sys.setrecursionlimit(100000)


specialchar=['￥','……','…','@','#','$','%','^','&','*','-','+','=','_','/','·','`','~','(',')',' ','\n',',','\'','.','[',']',':',';','（','）',' ','“','”','，','。','！','？','；','：','‘','’','、','《','》','【','】']
context=[]
word=[]
appearance=[]
probibility=[]

le=0
re=0
entropy=[]#should be a bigger number

solid=[]#should be more than a huge number

cnt=0


def quicksort(l,r):
    if l>=r:
        return
    i=l
    j=r
    temp=probibility[l]
    while i!=j:
        if i>r or j<l:
            print("error")
            quit()
        while probibility[j]<=temp and i<j:
            j-=1
        while probibility[i]>=temp and i<j:
            i+=1
        if i<j:
            _t=probibility[i]
            probibility[i]=probibility[j]
            probibility[j]=_t
            _m=word[i]
            word[i]=word[j]
            word[j]=_m
            _k=appearance[i]
            appearance[i]=appearance[j]
            appearance[j]=_k
    _t=probibility[l]
    probibility[l]=probibility[i]
    probibility[i]=_t
    _m=word[l]
    word[l]=word[i]
    word[i]=_m
    _k=appearance[l]
    appearance[l]=appearance[i]
    appearance[i]=_k
    quicksort(l,i-1)
    quicksort(i+1,r)
    return


f=open("data.txt","r")
minwordlength=1
maxwordlength=int(input("Input the maximun length of word:"))


appearance_threshold=2
solid_threshold=80
entropy_threshold=0.02


if minwordlength>=maxwordlength:
    print("error\n")
    quit()


for i in f.read():
    if i not in specialchar:
        context.append(i)
f.close()


for _wordlength in range(minwordlength,maxwordlength+1):
    for i in range(0,len(context)-_wordlength+1):
        transword=context[i]
        for j in range(1,_wordlength):
            transword=transword+context[i+j]
        foundword=False
        for wordplace in range(len(word)):
            if word[wordplace]==transword:
                foundword=True
                appearance[wordplace]+=1
                cnt+=1
                break
        if foundword==False:
            word.append(transword)
            appearance.append(1)
            cnt+=1


context=[]


for i in range(len(appearance)):
    probibility.append(appearance[i]/cnt)
    solid.append(10000000.0)


quicksort(0,len(probibility)-1)
print("finished {}".format(len(word)))

for i in range(len(word)):
    re=0
    le=0
    for j in range(len(word)):
        if len(word[i]+word[j])>maxwordlength:
            continue
        for k in range(len(word)):
            if word[i]+word[j]==word[k]:
                re-=probibility[j]*math.log(probibility[j],math.e)
                solid[k]=min(solid[k],probibility[k]/(probibility[i]*probibility[j]))
                break
        for k in range(len(word)):
            if word[j]+word[i]==word[k]:
                le-=probibility[j]*math.log(probibility[j],math.e)
                solid[k]=min(solid[k],probibility[k]/(probibility[i]*probibility[j]))
                break
    entropy.append(min(re,le))
    print("{:.5f} {:.5f}".format(entropy[i],solid[i]))


for i in range(len(probibility)):
    if appearance[i]>appearance_threshold and solid[i]!=10000000.0 and entropy[i]>entropy_threshold and solid[i]>solid_threshold:
        print("{} :边界自由度:{:.5f},内部凝固度:{:.5f},出现{}次,出现概率{:.5f}%".format(word[i],entropy[i],solid[i],appearance[i],100*probibility[i]))
