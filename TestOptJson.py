# -*- coding: utf-8 -*-
import json
import os,sys
#import pylab
import math
Base_Path=sys.path[0]
filepath=os.path.join(Base_Path,"result.txt")
fin=open(filepath,"r")
#filepath=os.path.join(Base_Path,"updateresult.txt")
#fout=open(filepath,"wt")
S_LinesDict={}
for line in fin:
    wordlist=line.strip().split(".")
    if len(wordlist) !=2:
        print("The struct of data is wrong")
    tmpstr_1="".join(wordlist[1:])
    wordlist_1=tmpstr_1.strip().split()
    num_wordlist_1=len(wordlist_1)
    tmpdict={}
    for word_index in range(num_wordlist_1-1):
        tmpword=str(wordlist_1[word_index+1]).split(":")
        if len(tmpword)==2:
            tmpdict[word_index]=[]
            tmpdict[word_index].append(tmpword[0])
            tmpdict[word_index].append(int(tmpword[1]))
    #print(str(wordlist[0]))
    S_LinesDict[str(wordlist[0]).strip()]=tmpdict
#print(S_LinesDict)
fin.close()
#print(S_LinesDict)
if 'qjky0326' in S_LinesDict:
    print("-----------------")
#for line in fin:
#    wordlist=line.strip().split("/")
#    strtmp="".join(wordlist[1:])
#    #print("----------------------")
#    #print(strtmp)
#    strtmp_1=strtmp.split()
#    strtmp_2=""
#    for n in range(len(strtmp_1)-1):
#        strtmp_2+=strtmp_1[n+1]+" "
#    #print(strtmp_2)
#    fout.write(strtmp_2)
#    fout.write("\n")
#fin.close()
#fout.close()


#filepath=os.path.join(Base_Path,"updateresult.txt")
#S_LinesList=[]#生成每一句逐个单词对应的类别
#fin=open(filepath,"r")
#for line in fin:
#    wordlist_1=line.rstrip().split()
#    wordlen_1=len(wordlist_1)
#    #print(wordlen_1)
#    #lineindex=0
#    wordindex=0
#    tmpdict={}
#     for n in range(wordlen_1):
#        tmpword=str(wordlist_1[wordindex]).split(":")
#        #print(tmpword)
#        if len(tmpword)==2:
#            tmpdict[wordindex]=int(tmpword[1])
#        wordindex=wordindex+1
#    S_LinesList.append(tmpdict)
#print(S_LinesList[4])
#fin.close()


filepath=os.path.join(Base_Path,"tone.B.txt")
fin=open(filepath,'r')
T_LinesDict={}
for line in fin:
    m_wordlist=line.split()
    m_str=m_wordlist[0].strip()
    m_wordlist_1=m_str.split(".")
    m_str_1=m_wordlist_1[0]
    m_wordlist_2=m_str_1.split("/")
    m_name=m_wordlist_2[-1]
    num_lines=0
    wordlist=line.split()
    strdata="".join(wordlist[1:])
    aa=json.loads(strdata)
    _line_content = aa["lines"]
    num_line_content = len(_line_content)
    LineDict={}
    num_LineDict=0
    for index_line_ in range(0,num_line_content):
        line_result = _line_content[index_line_]
        if line_result.has_key("words"):
            words_result=line_result["words"]
            num_words_result=len(words_result)
            for words_index in range(num_words_result):
                word_content=words_result[words_index]
                word_type=word_content["type"]
                if word_type !=2:
                    continue     
                #if word_type==4:
                #    continue
                #if word_type==0:#不用跳过
                #    continue
                #if word_type==5:
                #    continue
                #if word_content["type"]==1:
                #    print(word_content)
                tmplist=[]
                tmplist.append(word_content["text"])
                tmplist.append(word_content["accent"])
                LineDict[num_LineDict]=tmplist
                num_LineDict+=1
    T_LinesDict[m_name]=LineDict
#print(T_LinesDict)
num_T=len(T_LinesDict)
#print(num_T)
#print(T_LinesDict[1])
Static_Data=[]
for key_0 in T_LinesDict:
    if key_0 in S_LinesDict:
        m_dict_1=T_LinesDict[key_0]
        for key_1 in m_dict_1:
            if key_1 in S_LinesDict[key_0]:
                m_s_dict=S_LinesDict[key_0]
                if m_dict_1[key_1][0].strip()==m_s_dict[key_1][0].strip():
                    m_dict_1[key_1].append(m_s_dict[key_1][1])
                    #print("************")
                    #print(m_dict_1[key_1])
                    Static_Data.append(m_dict_1[key_1])             
    else:
        print("Have no matched data!")
#print(Static_Data)
#得到类别的统计数据
floatlabel_1=[]
floatlabel_2=[]
floatlabel_3=[]
#print(Static_Data)
num_Static=len(Static_Data)
for n in range(num_Static):
    tmplist=Static_Data[n]
    tmplabel=tmplist[2]
    tmpfloat=tmplist[1]
    if tmplabel==1:
        floatlabel_1.append(tmpfloat)
    elif tmplabel==2:
        floatlabel_2.append(tmpfloat)
    else:
        floatlabel_3.append(tmpfloat)

#画出图象
#pylab.plot(floatlabel_1)
#pylab.show()

#求均值和方差
sum_label_1=0.0
q_sum_label_1=0.0
sum_label_2=0.0
q_sum_label_2=0.0
sum_label_3=0.0
q_sum_label_3=0.0
var_label_1=0.0
var_label_2=0.0
var_label_3=0.0
for n in range(len(floatlabel_1)):
    sum_label_1+=floatlabel_1[n]
    q_sum_label_1+=floatlabel_1[n]**2
mean_label_1=sum_label_1/len(floatlabel_1)
var_label_1=q_sum_label_1/len(floatlabel_1)-mean_label_1**2

for n in range(len(floatlabel_2)):
    sum_label_2+=floatlabel_2[n]
    q_sum_label_2+=floatlabel_2[n]**2
mean_label_2=sum_label_2/len(floatlabel_2)
var_label_2=q_sum_label_2/len(floatlabel_2)-mean_label_2**2

for n in range(len(floatlabel_3)):
    sum_label_3+=floatlabel_3[n]
    q_sum_label_3+=floatlabel_3[n]**2
mean_label_3=sum_label_3/len(floatlabel_3)
var_label_3=q_sum_label_3/len(floatlabel_3)-mean_label_3**2

print("the label_1",mean_label_1,var_label_1)
print("the label_2",mean_label_2,var_label_2)
print("the label_3",mean_label_3,var_label_3)

#寻优
init_thre_l=mean_label_3
init_thre_r=mean_label_1
delt_l=(math.sqrt(var_label_3))/3.0
delt_r=(math.sqrt(var_label_1))/3.0
thelt=0.05
correctnum=0.0
direct_3=0.0
direct_1=0.0
D_l=-1
D_r=1
for n in range(num_Static):
    if Static_Data[n][1]<init_thre_l:
        Static_Data[n].append(3)
    elif Static_Data[n][1]>init_thre_r:
        Static_Data[n].append(1)
    else:
        Static_Data[n].append(2)
    if Static_Data[n][2]==Static_Data[n][3]:
        correctnum+=1
    if Static_Data[n][2]==3:
        tmpdirect_3=Static_Data[n][2]-Static_Data[n][3]
        direct_3+=tmpdirect_3
    if Static_Data[n][2]==1:
        tmpdirect_1=Static_Data[n][2]-Static_Data[n][3]
        direct_1+=tmpdirect_1
thre_l=init_thre_l
thre_r=init_thre_r
init_rate=correctnum/num_Static
rate=init_rate
Curnum=1
print(Static_Data)
print(init_thre_l,init_thre_r)
print(direct_3,direct_1)
print("---------------------")
while 1:
    #if direct_3>20:
        #D_l=1
    #else:
        #D_l=-1
    #if direct_1<-20:
        #D_r=-1
    #else:
        #D_r=1
    thre_l+=(D_l)*0.005
    thre_r+=(D_r)*0.005
    print(thre_l,thre_r)
    correctnum=0.0
    direct_3,direct_1=0,0
    for n in range(num_Static):
        if Static_Data[n][1]<thre_l:
            #print("三")
            Static_Data[n][3]=3
        elif Static_Data[n][1]>thre_r:
            Static_Data[n][3]=1
        else:
            Static_Data[n][3]=2
        if Static_Data[n][2]==Static_Data[n][3]:
            correctnum+=1
        if Static_Data[n][2]==3:
            tmpdirect_3=Static_Data[n][2]-Static_Data[n][3]
            direct_3+=tmpdirect_3
        if Static_Data[n][2]==1:
            tmpdirect_1=Static_Data[n][2]-Static_Data[n][3]
            direct_1+=tmpdirect_1
    print("the correctnum:",correctnum)
    tmprate=correctnum/num_Static
    if tmprate>rate:
        rate=tmprate
    #else:
        #if abs(rate-tmprate)<0.001:
            #print("Thelt break")
            #break
    Curnum+=1
    if(Curnum>=500):
        print("num enough")
        break
    print("%%%%%%%%%%%%%%%%%%%%%%%%")
    print(direct_3,direct_1)
    print(tmprate)
print(rate)     
#print(direct_3,direct_1)
#init_rate=correctnum/num_Static
#print(init_rate)

   



#---------对机测数据进行处理----------#
if 0:
    filepath=os.path.join(Base_Path,"tone.B.txt")
    fin=open(filepath,'r')
    T_LinesList=[]
    for line in fin:
        num_lines=0
        wordlist=line.split()
        #print(len(wordlist))
        strdata="".join(wordlist[1:])
        #print(strdata)
        #jsondata=dict(strdata)
        aa=json.loads(strdata)
        #print(aa)
        _line_content = aa["lines"]
        num_line_content = len(_line_content)
        LineDict={}
        num_LineDict=0
        for index_line_ in range(0,num_line_content):
            line_result = _line_content[index_line_]
            if line_result.has_key("words"):
                words_result=line_result["words"]
                num_words_result=len(words_result)
                for words_index in range(num_words_result):
                    word_content=words_result[words_index]
                    if word_content["type"]==4:
                        continue
                    tmplist=[]
                    tmplist.append(word_content["accent"])
                    LineDict[num_LineDict]=tmplist
                    num_LineDict+=1
                #print("--------")
                #print(LineDict)
                #print("---------")
        T_LinesList.append(LineDict)
    #print(T_LinesList[4])
    fin.close()
