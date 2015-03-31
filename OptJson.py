# -*- coding: utf-8 -*-
import OptModul as opt
import os,sys
import pylab
import numpy
Base_Path=sys.path[0]
filepath=os.path.join(Base_Path,"result.txt")
S_LinesDict=opt.GenSLinesDict(filepath)
filepath=os.path.join(Base_Path,"tone.B.txt")
T_LinesDict=opt.GenTLinesDict(filepath)
Static_Data=opt.GenStaticData(S_LinesDict,T_LinesDict)
floatlabel_1=[]
floatlabel_2=[]
floatlabel_3=[]
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


mean_label_1=numpy.mean(floatlabel_1)
var_label_1=numpy.var(floatlabel_1)
mean_label_2=numpy.mean(floatlabel_2)
var_label_2=numpy.var(floatlabel_2)
mean_label_3=numpy.mean(floatlabel_3)
var_label_3=numpy.var(floatlabel_3)
rank_1=[]
rank_2=[]
rank_3=[]
if 1:
    for n in range(len(floatlabel_1)):
        rank_1.append(1)
    for n in range(len(floatlabel_2)):
        rank_2.append(2)
    for n in range(len(floatlabel_3)):
        rank_3.append(3)

    pylab.plot(rank_1,floatlabel_1,'ro',rank_2,floatlabel_2,'bo',rank_3,floatlabel_3\
               ,'go')
    pylab.axis([0,4,-10,10])
    pylab.show()
if 0:
    '''
    绘制类别图像
    '''
    for n in range(500):
        rank_1.append(mean_label_1)
        rank_2.append(mean_label_2)
        rank_3.append(mean_label_3)

        
    pylab.plot(range(len(floatlabel_1)),floatlabel_1,'ro',range(len(floatlabel_2)),\
               floatlabel_2,'bo',range(len(floatlabel_3)),floatlabel_3,'go')
    pylab.plot(range(len(rank_1)),rank_1,'r-',linewidth=4)
    pylab.plot(range(len(rank_2)),rank_2,'b-',linewidth=4)
    pylab.plot(range(len(rank_3)),rank_3,'g-',linewidth=4)
    pylab.show()
##
