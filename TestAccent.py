# -*- coding: utf-8 -*-
import json
import os,sys
import OptModul as opt
import numpy
if 0:
    Base_Path=sys.path[0]
    filepath=os.path.join(Base_Path,"result.txt")
    ResultDict={}
    fin=open(filepath,"r")
    for line in fin:
        wordlist=line.strip().split(".")
        if len(wordlist) !=2:
            print("The struct of data is wrong")
        filename=wordlist[0].strip()
        linecontent="".join(wordlist[1:])
        if filename not in ResultDict:
            ResultDict[filename]=linecontent
    fin.close()

    filepath=os.path.join(Base_Path,"tone.B.txt")
    fin=open(filepath,"r")
    ToneDict={}
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
            words_line=[]
            if line_result.has_key("words"):
                words_result=line_result["words"]
                num_words_result=len(words_result)
                for words_index in range(num_words_result):
                    word_content=words_result[words_index]
                    word_accent=word_content["accent"]
                    word_text=word_content["text"]
                    word_type=word_content["type"]
                    if word_type !=4:
                        words_line.append(word_text)
                        words_line.append(word_accent)
            if m_name not in ToneDict:
                ToneDict[m_name]=words_line
    fin.close()
    filepath=os.path.join(Base_Path,"compare.txt")
    fout=open(filepath,"w")
    for key in ResultDict:
        if key in ToneDict:
            print("the same")
            str_result=ResultDict[key]
            fout.write(str(key))
            fout.write(":")
            fout.write(str_result)
            fout.write("\n")
            str_tone=str(ToneDict[key][0:])
            fout.write(str(key))
            fout.write(":")
            fout.write(str_tone)
            fout.write("\n")
    fout.close()
    
Base_Path=sys.path[0]
filepath=os.path.join(Base_Path,"result.txt")
S_LinesDict=opt.GenSLinesDict(filepath)
filepath=os.path.join(Base_Path,"tone.B.txt")
T_LinesDict=opt.GenTLinesDict(filepath)
Ensemble=opt.GenStaticData(S_LinesDict,T_LinesDict)
StaticDict=Ensemble[0]
LocationData=Ensemble[1]
#print(LocationData)
sum_word=opt.SumOfWord(StaticDict)
mean_result=opt.FindMeanVar(StaticDict)
#R=opt.GenPlot(StaticDict)
InitClassifyDict=opt.InitClassify(mean_result,StaticDict)
inithre=[]
inithre.append(mean_result[4])
inithre.append(mean_result[0])
ResultCla=opt.ResultOfCla(sum_word,inithre,InitClassifyDict)
curcount=0
left=inithre[0]
right=inithre[1]
thre_left=0.0
thre_right=0.0
OptStaticDate={}
tmp_rate=ResultCla["rate"]
thre=[]
while curcount<50:
    thre.append(left)
    thre.append(right)
    StaticDate=opt.JudeThre(thre,InitClassifyDict)
    FindCla=opt.ResultOfCla(sum_word,thre,StaticDate)
    left-=left/50
    if tmp_rate<FindCla["rate"]:
        tmp_rate=FindCla["rate"]
        thre_left=left
        OptStaticDate=StaticDate
    #print(FindCla)
    curcount+=1
    thre=[]


curcount=0
thre=[]
while curcount<50:
    left=thre_left
    thre.append(left)
    thre.append(right)
    StaticDate=opt.JudeThre(thre,OptStaticDate)
    FindCla=opt.ResultOfCla(sum_word,thre,StaticDate)
    right-=right/50
    if tmp_rate<FindCla["rate"]:
        tmp_rate=FindCla["rate"]
        thre_right=right
        OptStaticDate=StaticDate
    curcount+=1
    thre=[]

OptThreshold=[]
OptThreshold.append(thre_left)
OptThreshold.append(thre_right)
T_d=opt.Location(OptThreshold,LocationData)


filepath=os.path.join(Base_Path,"wrongdata.txt")
fout=open(filepath,'w')
for key in T_d:
    linecon=T_d[key]
    fout.write(str(key))
    fout.write(":")
    for index in range(len(linecon)):
        if abs(linecon[index][2]-linecon[index][3])==2:
            fout.write(str(linecon[index]))
            fout.write(" ")
    fout.write("\n")
fout.close()



'''
if 0:    
    Cplines={}
    for key in S_LinesDict:
        if key in T_LinesDict:
            T_content_line=T_LinesDict[key]
            S_content_line=S_LinesDict[key]
            for key_1 in T_content_line:
                if key_1 in S_content_line:
                    if T_content_line[key_1][0]==S_content_line[key_1][0]:
                        T_content_line[key_1].append(S_content_line[key_1][1])
        if key not in Cplines:
            Cplines[key]=T_content_line
    #print(Cplines)

    if 0:
        filepath=os.path.join(Base_Path,"compare_1.txt")
        fout=open(filepath,"w")
        for key in Cplines:
            fout.write(str(key))
            fout.write(":")
            fout.write(str(Cplines[key]))
            fout.write("\n")
        fout.close()
if 0:
    filepath=os.path.join(Base_Path,"static.txt")
    fout=open(filepath,"w")
    for key in Cplines:
        content_line=Cplines[key]
        label_1=[]
        label_2=[]
        label_3=[]
        static_line=[]
        for key_1 in content_line:
            if len(content_line[key_1])==3:
                m_type=content_line[key_1][2]
                m_float=content_line[key_1][1]
            if m_type==1:
                label_1.append(m_float)
            if m_type==2:
                label_2.append(m_float)
            else:
                label_3.append(m_float)
        mean_1=numpy.mean(label_1)
        var_1=numpy.var(label_1)
        mean_2=numpy.mean(label_2)
        var_2=numpy.var(label_2)
        mean_3=numpy.mean(label_3)
        var_3=numpy.var(label_3)
        static_line.append(str(key))
        static_line.append(mean_1)
        static_line.append(var_1)
        static_line.append(mean_2)
        static_line.append(var_2)
        static_line.append(mean_3)
        static_line.append(var_3)
        fout.write(str(static_line))
        fout.write("\n")
    fout.close()
    
    '''
    
    
        
