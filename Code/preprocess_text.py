# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 00:06:57 2020

@author: theki
"""

import json
import os
import pickle
import re


def find_text(patternlist,textlist):
    indices=[None]*len(suppkeywords)
    for patterni in range(len(suppkeywords)):
        c=[]
        for texti, curtitle in enumerate(titles):
            if not curtitle==None:
             if suppkeywords[patterni].lower() in curtitle.lower():
                 c.append(texti)
        indices[patterni]=c    
        indices[patterni] = [i for i, curtitle in enumerate(titles) if suppkeywords[patterni] in curtitle]  
        



basedir=r"D:\Professional\corona\text"
sectionsep="%Paragraph%"
suppkeywords=['Supplementary','appendi','material','figure']
reviewkeywords=['review','overview','surv']
resultskeywords=['esults: ','found ','emonstrate','etermine',
    'xplain','show','uggest','rovide*','shed light',
    'eveal','ncover','onclusion','conclude','verall',
    'ummary','ropose','eport','illustrat','identified'
    'present','indicate']
covidkeywords=['SARS-CoV-2','corona ','COVID','coronavirus']

find_text(suppkeywords,titles)
os.chdir(basedir)
files=os.listdir()
filedir=basedir+"\\"+files[1]
textbodies=[None]*len(files)
titles=[None]*len(files)
abstracts=[None]*len(files)
for filesi in range(len(files)):
    try:
        print(filesi)
        fp=open(files[filesi])
        loaded=json.load(fp)
        thisbody=loaded['body_text']
        thisabstract=loaded['abstract']
        titles[filesi]=loaded['metadata']['title']
        abstracts[filesi]=[None]*len(thisabstract)
        textbodies[filesi]=[None]*len(thisbody)
        for bodyi in range(len(thisbody)):
            textbodies[filesi][bodyi]=thisbody[bodyi]['text']
        for abstracti in range(len(thisabstract)):
            abstracts[filesi][abstracti]=thisabstract[abstracti]
    except:
        pass
pickle.dump(textbodies,open("textbodies.dat","wb"))