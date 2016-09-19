#!/usr/bin/env python
#coding:utf8
import os.path, sys, time, datetime
import codecs
from cStringIO import StringIO
from subprocess import call

from bottle import route, run, get, post, request, response, static_file
from nltk.tokenize.punkt import PunktSentenceTokenizer

from propsde.applications.run import loadParser, parseSentences
from propsde.visualizations.brat_visualizer import BratVisualizer

try:
    PORT = int(sys.argv[1])
except:
    PORT = 8081
    
sent_tokenizer = PunktSentenceTokenizer()

@get('/gparse')
def gparse():
    print "in gparse"
    
    input = request.GET.get('text').strip().decode("utf8")
    print input
    
    sents = sent_tokenizer.tokenize(input)
    gs = parseSentences(sents[:1])
    g,tree = gs[0]
    
    b = BratVisualizer()
    ret = b.to_html(g)
       
    ret = ret.replace('PROPOSITIONS_STUB', '<br>'.join([unicode(prop) for prop in g.getPropositions('html')]))
    
    print "returning...." 
    return ret
    
@route('/brat/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./propsde/visualizations/brat')
    
@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='./propsde/webinterface')

loadParser()
run(host='',port=PORT)
