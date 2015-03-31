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
        tmpdict={}
        for word_index in range(num_wordlist_1-1):
            tmpword=str(wordlist_1[word_index+1]).split(":")
            if len(tmpword)==2:
                tmpdict[word_index]=[]
                tmpdict[word_index].append(tmpword[0])
                tmpdict[word_index].append(int(tmpword[1]))
        S_LinesDict[str(wordlist[0]).strip()]=tmpdict
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
    return T_LinesDict

def GenStaticData(S_LinesDict,T_LinesDict):
    '''
    获得机器标注对象中单词对应人工标注的类别，及声调值
    '''
    num_T=len(T_LinesDict)
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
    return Static_Data

###
