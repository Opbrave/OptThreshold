# -*- coding: utf-8 -*-
import json
import os,sys
import pylab
import math
import numpy

def GenSLinesDict(FileIn):
    '''
    读取人工标注文本，
    获得单词与类别的匹配Dict
    '''
    fin=open(FileIn,"r")
    S_LinesDict={}
    for line in fin:
        wordlist=line.strip().split(".")
        if len(wordlist) !=2:
            print("The struct of data is wrong")
        tmpstr_1="".join(wordlist[1:])
        wordlist_1=tmpstr_1.strip().split()
        num_wordlist_1=len(wordlist_1)
        linelist=[]  #修改
        for word_index in range(num_wordlist_1-1):
            tmpword=str(wordlist_1[word_index+1]).split(":")
            if len(tmpword)==2:
                tmplist=[]
                tmplist.append(tmpword[0])
                tmplist.append(int(tmpword[1]))
                linelist.append(tmplist)
        S_LinesDict[str(wordlist[0]).strip()]=linelist
    fin.close()
    return S_LinesDict

def GenTLinesDict(FileIn):
    '''
    读取机器标注的文本
    获取文本内容，以及音调评分值
    '''
    fin=open(FileIn,'r')
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
        LineList=[] #
        num_LineDict=0
        for index_line_ in range(0,num_line_content):
            line_result = _line_content[index_line_]
            if line_result.has_key("sample"):
                line_sample=line_result["sample"]
                #print(line_sample)
            if line_result.has_key("words"):
                words_result=line_result["words"]
                num_words_result=len(words_result)
                for words_index in range(num_words_result):
                    word_content=words_result[words_index]
                    word_type=word_content["type"]
                    if word_type !=2:
                        continue     
                    tmplist=[]
                    tmplist.append(word_content["text"])
                    tmplist.append(word_content["accent"])
                    LineList.append(tmplist)
                    num_LineDict+=1
        T_LinesDict[m_name]=LineList
    return T_LinesDict

def GenStaticData(S_LinesDict,T_LinesDict):
    '''
    获得机器标注对象中单词对应人工标注的类别，及声调值
    '''
    num_T=len(T_LinesDict)
    Static_Data={}
    for key_0 in S_LinesDict:
        if key_0 in T_LinesDict:
            m_list_S=S_LinesDict[key_0]
            m_list_T=T_LinesDict[key_0]
            num_S_list=len(m_list_S)
            num_T_list=len(m_list_T)
            #print(num_S_list,num_T_list)
            index_T=0
            index_S=0
            index_list=0
            #print(key_0)
            list_tmp=[]
            same_count=0
            error_S=0
            error_T=0
            while index_T<num_T_list-1 and index_S<num_S_list-1:
                if m_list_S[index_S][0]==m_list_T[index_T][0]:
                   m_list_T[index_T].append(m_list_S[index_S][1])
                   list_tmp.append(m_list_T[index_T])
                   index_T+=1
                   index_S+=1
                   same_index_S=index_S
                else:
                    index_S+=1
                    error_S+=1
                if error_S>=4:
                    index_S=index_S-error_S
                    index_T+=1
                    error_S=0
                    #f(same_index_S==index_S):
                        #same_count+=1
                #if same_count==3:
                    #index_S+=1
                    #same_count=0
            Static_Data[key_0]=list_tmp
            list_tmp=[]
    return Static_Data

def FindMean(StaticDict):
    label1_float=[]
    label2_float=[]
    label3_float=[]
    result=[]
    for key in StaticDict:
        line_content=StaticDict[key]
        num_line_content=len(line_content)
        for index in range(num_line_content):
            if line_content[index][2]==1:
                label1_float.append(line_content[index][1])
            elif line_content[index][2]==2:
                label2_float.append(line_content[index][1])
            else:
                label3_float.append(line_content[index][1])
    mean_1=numpy.mean(label1_float)
    var_1=numpy.var(label1_float)
    mean_2=numpy.mean(label2_float)
    var_2=numpy.var(label2_float)
    mean_3=numpy.mean(label3_float)
    var_3=numpy.var(label3_float)
    result.append(mean_1)
    result.append(var_1)
    result.append(mean_2)
    result.append(var_2)
    result.append(mean_3)
    result.append(var_3)
    print(result)
    return result

def InitThreshold(result,StaticDict):
    right=result[1]
    left=result[4]
    thre_right=right
    thre_left=left
    for key in StaticDict:
        line_content=StaticDict[key]
        num_line_content=len(line_content)
        for index in range(num_line_content):
            if line_content[index][1]<thre_left:
                line_content[index].append(3)
            elif line_content[index]>thre_right:
                line_content[index].append(1)
            else:
                line_content[index].append(2)
    correct=0.0
    allnum=0.0
    for key in StaticDict:
        line_content=StaticDict[key]
        num_line_content=len(line_content)
        for index in range(num_line_content):
            allnum+=1
            if line_content[index][2]==line_content[index][3]:
                correct+=1
    initrate=correct/allnum
    print(correct)
    print(allnum)
    return initrate

def Recur(StaticDict,left,right):
    dir_err_1=0
    dir_err_3=0
    maxrate=0.0
    thre_result=[0.0,0.0]
    for key in StaticDict:
        line_content=StaticDict[key]
        num_line_content=len(line_content)
        for index in range(num_line_content):
            if line_content[index][2]==1:
                tmp_1=line_content[index][2]-line_content[index][3]
                dir_err_1+=tmp_1
            if line_content[index][2]==3:
                tmp_3=line_content[index][2]-line_content[index][3]
                dir_err_3+=tmp_3
    print(dir_err_1,dir_err_3)
    rate=0.0
    rec_count=0
    thre_left=left
    thre_right=right
    while rate<0.54 and rec_count<1000:
        thre_left-=left/1000
        for key in StaticDict:
            line_content=StaticDict[key]
            num_line_content=len(line_content)
            for index in range(num_line_content):
                if line_content[index][1]<thre_left:
                    line_content[index][3]=3
                elif line_content[index]>thre_right:
                    line_content[index][3]=1
                else:
                    line_content[index][3]=2
            correct=0.0
            allnum=0.0
        for key in StaticDict:
            line_content=StaticDict[key]
            num_line_content=len(line_content)
            for index in range(num_line_content):
                allnum+=1
                if line_content[index][2]==line_content[index][3]:
                    correct+=1
        rate=correct/allnum
        if maxrate<rate:
            maxrate=rate
            thre_result[0]=thre_left
        rec_count+=1
        print(maxrate)
    thre_result[1]=thre_right
    rec_count=0
    while rate<0.54 and rec_count<1000:
        thre_right+=right/1000
        thre_left=thre_result[0]
        for key in StaticDict:
            line_content=StaticDict[key]
            num_line_content=len(line_content)
            for index in range(num_line_content):
                if line_content[index][1]<thre_left:
                    line_content[index][3]=3
                elif line_content[index]>thre_right:
                    line_content[index][3]=1
                else:
                    line_content[index][3]=2
            correct=0.0
            allnum=0.0
        for key in StaticDict:
            line_content=StaticDict[key]
            num_line_content=len(line_content)
            for index in range(num_line_content):
                allnum+=1
                if line_content[index][2]==line_content[index][3]:
                    correct+=1
        rate=correct/allnum
        if maxrate<rate:
            maxrate=rate
            thre_result[1]=thre_right
        rec_count+=1
        print("right",maxrate)
    print(StaticDict)
    return thre_result
                
###
