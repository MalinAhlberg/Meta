# -*- coding: utf_8 -*-
## OBS the root are called MS!!

import re
import codecs
import os.path
from xml.etree import ElementTree as etree
import xmlindent
from collections import defaultdict

# Empty corpus
start = '<corpus><body></body></corpus>'

# Creates a tree for one sentence
def mkSent(n,lines):
  n = n+1
  s = etree.fromstring(start).makeelement('s',{'id':'s'+str(n)})
  g = etree.SubElement(s,'graph')
  etree.SubElement(g,'terminals')
  etree.SubElement(g,'nonterminals')
  unrooted = set([])
  deprs    = {}
  root = None
  map(lambda i: unrooted.add(i+1),range(len(lines)-2))
  for (i,line) in enumerate(lines):
    tabs = line.split('\t')
    if line.strip()!='' and tabs!=[]:
      w    = tabs[0]
      p2   = tabs[1]
      pos  = tabs[2]
      wf   = tabs[3]
      lex  = tabs[4]
      sal  = tabs[5]
      pref = tabs[6] 
      suff = tabs[7] 
      depr = tabs[10].strip('\n')
      deprs.update({i:depr})
      t = g.find('terminals')
      etree.SubElement(t,'t',{'id':mkref('w',n,i),'form':w, 'postag':pos, 'lemma':form(wf)
                             ,'lex':form(lex),'saldo':form(sal),'pos':p2
                             ,'prefix':form(pref),'suffix':form(suff)}) #-- Use or not?
      nt = g.find('nonterminals')
      x = etree.SubElement(nt,'nt',{'id':mkref('p',n,i),'form':w, 'postag':pos})
      etree.SubElement(x,'edge',{'idref':mkref('w',n,i),'label':'--'})
      if depr=='ROOT':     # if this is the root, add info to graph node
         g.attrib.update({'root':mkref('p',n,i)})
         unrooted.discard(i) # the node does not need another parent
         root = i
      for (j,line) in enumerate(lines):
      # for all words with this as head, add an edge from this one with correct label
        tabs = line.split('\t')
        if line.strip()!= '' and tabs!=[]:
          head = tabs[9]
          depr = tabs[10].strip('\n')
          if head and int(head)==i: 
           unrooted.discard(j)
           etree.SubElement(x,'edge',{'idref':mkref('p',n,j),'label':label(depr)})
  fixroot(g,unrooted,deprs,n,root)
  return s

# ROOTs should be called MS as the added root needs the 'ROOT'-name
def label(s):
  if s=='ROOT':
    return 'MS'
  else:
    return s

# add an artificial root if needed
def fixroot(g,unrooted,deprs,n,root):
#  if len(unrooted)>0:
    g.attrib.update({'root':mkref('p',n,0)})
    nt = g.find('nonterminals')
    x  = etree.SubElement(nt,'nt',{'id':mkref('p',n,0),'form':'--', 'postag':'ROOT'})
    for i in unrooted:
      depr = deprs.get(i)
      if depr is None:
        print unrooted,deprs,n,i
      etree.SubElement(x,'edge',{'idref':mkref('p',n,i),'label':depr})
    if root is not None:
      etree.SubElement(x,'edge',{'idref':mkref('p',n,root),'label':'MS'})
      
      
  
# Formatting for xml-values
def form(w):
    if w.strip()=='|':
       return '--'
    return w.strip('|')

# Creates a name eg. "s1_2"
def mkref(name,n,i):
    return name+str(n)+'_'+str(i)

# Converts vrt-files to tigerxml
def createtiger():
   import glob
   import os.path
   for fil in glob.glob('vrt/*'):
     name = os.path.basename(fil).split('.')[0]
     txt = open(fil,'r').read()
     xml = etree.fromstring('<doc>'+txt+'</doc>')
     ss = xml.findall('sentence')
     xmls = etree.fromstring(start) 
     body = xmls.find('body')
     xmls.attrib.update({'id':(name)})
     for (i,s) in enumerate(ss):
       stxt = '\n'.join(list(s.itertext()))
       body.append(mkSent(i,stxt.split('\n')))
     xmlindent.indent(xmls)
     open('hej/'+name+'.xml','w').write(etree.tostring(xmls,encoding='utf8'))
   



################################################################################
# UNFINISHED AND UNUSED TO CREATE HEAD  
################################################################################
#     head = open('header.xml','r').read()
#     xmls.insert(0,etree.fromstring(head))
#generatehead(xml)
def generatehead(xml):

  ts = body.findall('s.graph.terminals')
  ns = body.findall('s.graph.nonterminals')
  terms    = set([x.attrib.items() for x in ts])
  nonterms = set([x.attrib.items() for x in ns])
  for (k,v) in terms+nonterms:
       if k=='pos':
         addList(findfeatuer(ts,v)) # find feature, 'pos'
  for (k,v) in terms+nonterms:
       if k=='postag':
         addList(find(k),v) # find feature, 'pos')
  edges = set([x.attrib.items() for x in body.findall('s.graph.nonterminals.nt.edge')])
  for (k,v) in edges:
    addList(findfeature(ns,'edgelabel'),v)

def findfeature(xml,name):
  vs = xml.findall('feature')
  value = [(f for (n,v) in v.attrib.items() if n=='name'and v==name) for f in fs]
  if value!=[]:
    return value[0]

def addList(tree,val):
  vs = feat.findall('value')
  value = [(v for (n,k) in v.attrib.items() if n=='name'and k==val) for v in vs]
  if value==None:
    etree.SubElement(feat,'value',{'name':val})

