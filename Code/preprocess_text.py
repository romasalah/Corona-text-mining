# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 00:06:57 2020

@author: theki
"""

import json
import os
import pickle
import re
import pdb
import numpy as np


def find_text(patternlist,textlist,combine=1):
    suppindices=[None]*len(patternlist)
    suppposindices=[None]*len(patternlist)
    nonsuppindices=[None]*len(patternlist)
    for patterni in range(len(patternlist)):
        supptemp=[]
        supppostemp=[]
        nonsupptemp=[]
        for texti, curtitle in enumerate(textlist):
            if not curtitle==None:
             if patternlist[patterni].lower() in curtitle.lower():
                 supptemp.append(texti)
                 supppostemp.append(curtitle.lower().find(patternlist[patterni].lower()))
             else:
                 nonsupptemp.append(texti)
        suppindices[patterni]=supptemp
        suppposindices[patterni]=supppostemp
        nonsuppindices[patterni]=nonsupptemp
    if combine==1:
        nonsuppindices=combine_indices(nonsuppindices,'intersection')
        suppindices=combine_indices(suppindices,'union')
    return nonsuppindices,suppindices,suppposindices

def filter_paragraphs(patternlist,textlist,method):
    patternindices=[None]*len(patternlist)
    patternposindices=[None]*len(patternlist)
    for patterni in range(len(patternlist)):
        supptemp=[]
        supppostemp=[]
        for texti, curtitle in enumerate(textlist):
            if not curtitle==None:
                curkeyword=patternlist[patterni].lower()
            if curkeyword in curtitle.lower():
                 supptemp.append(texti)
                 keywordpos=curtitle.lower().find(curkeyword)
                 endofsentences=re.findall('\.\s',curtitle)
                 presentencesend=endofsentences < keywordpos
                 startsentence_i=presentencesend[-1]
                 supppostemp.append(keywordpos)
        patternindices[patterni]=supptemp
        patternposindices[patterni]=supppostemp                
    # elementsin=[textlist[i][patternpos[i]:,] for i in elementsin_i]   
    # for skipintroi in elementsin:
          
        
def combine_indices(allindices,function):
    combined=[]
    for i in range(0,len(allindices)-1):
        if function=='union':
            combined.extend(np.union1d(allindices[i],allindices[i+1]))
        elif function=='intersection':
           combined.extend(np.intersect1d(allindices[i],allindices[i+1]))
    return combined
        
def filter_lists(titles,abstracts,bodies,indices):
    titles=[titles[i] for i in indices]
    abstracts=[abstracts[i] for i in indices]
    bodies=[bodies[i] for i in indices]
    return titles,abstracts,bodies

def load_text(basedir):
    os.chdir(basedir)
    files=os.listdir()
    bodies=[None]*len(files)
    titles=[None]*len(files)
    abstracts=[None]*len(files)
    for filesi in range(len(files)):
   # for filesi in range(1000):
        try:
            print(filesi)
            fp=open(files[filesi])
            loaded=json.load(fp)
            thisbody=loaded['body_text']
            thisabstract=loaded['abstract']
            titles[filesi]=loaded['metadata']['title']
            abstracts[filesi]=[None]*len(thisabstract)
            bodies[filesi]=[None]*len(thisbody)
            for bodyi in range(len(thisbody)):
                bodies[filesi][bodyi]=thisbody[bodyi]['text']
            for abstracti in range(len(thisabstract)):
                abstracts[filesi][abstracti]=thisabstract[abstracti]
        except:
            pass
    return titles,abstracts,bodies

basedir=r"D:\Professional\corona\text"
sectionsep="%Paragraph%"
suppkeywords=['Supplementary','appendi','material','figure']
reviewkeywords=['review','overview','surv']
resultskeywords=['esults: ','found ','emonstrate','etermine',
    'xplain','show','uggest','rovide*','shed light',
    'eveal','ncover','onclusion','conclude','verall',
    'ummary','ropose','eport','illustrat','identified'
    'present','indicate']
covidkeywords=['SARS-CoV-2','corona','COVI','coronavirus']

# load text
titles,abstracts,bodies=load_text(basedir)
# remove supplementary materials
nonsupp_i,supp_i,_=find_text(suppkeywords,titles)
titles,abstracts,bodies=filter_lists(titles,abstracts,bodies,nonsupp_i)
# remove reviews
pdb.set_trace()
nonreview_i,review_i,_=find_text(reviewkeywords,abstracts)
titles,abstracts,bodies=filter_lists(titles,abstracts,bodies,nonreview_i)
# keep covid articles
noncovid_i,covid_i,_=find_text(covidkeywords,abstracts,combine=0)
titles,abstracts,bodies=filter_lists(titles,abstracts,bodies,covid_i)
#
pdb.set_trace()
filter_paragraphs(resultskeywords,abstracts,'after')

pickle.dump(bodies,open("textbodies.dat","wb"))