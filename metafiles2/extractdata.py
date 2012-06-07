# -*- coding: utf_8 -*-
import codecs
import glob
import os.path
from xml.etree import ElementTree as etree


""" reads and collects all text in xml """
def gettitel(fil):
    print fil
    meta = '{http://www.ilsp.gr/META-XMLSchema}'
    xmls = codecs.open(fil,'r').read()
    tree = etree.fromstring(xmls)
    name  = tree.find(meta+'identificationInfo').find(meta+'resourceName')
    print name.text
    return name.text

def mktable(fil):
    name = gettitel(fil)
    xs = [unicode(name),typ,ver,location,os.path.basename(fil)]
    return '\t'.join(xs)

def main():
   lines = [mktable(fil) for fil in glob.glob(os.path.join(lexicons,'*xml'))]
   codecs.open('out','w',encoding='utf8').write('\n'.join(lines))


lexicons = 'lexicon'
corpus   = 'corpus'
typ      =  u'lexicon' #u'corpus'
ver      =  u'Semi-automatically generated xml with manual revision'
location =  u'Språkbanken, Gothenburg, Sweden'
