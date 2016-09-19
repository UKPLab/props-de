"""
Usage:
  parse_props.py [INPUT] (-g|-t) [--original] [--props] [--oie] [--dep] 
  parse_props.py (-h|--help)

Parse sentences into the PropS representation scheme

Arguments:
  INPUT   input file composed of one sentence per line. if not specified, will use stdin instead
  
Options:
  -h             display this help
  -t             print textual PropS representation
  -g             print graphical representation (in svg format)
  --original     print original sentence
  --props        print the PropS representation of the input
  --oie          print open-ie like extractions
  --dep          print the intermediate dependency representation 
"""

#!/usr/bin/env python
#coding:utf8

import os, sys, codecs, time, datetime
import fileinput
import os.path
from cStringIO import StringIO
from subprocess import call

from docopt import docopt
from propsde.applications.viz_tree import DepTreeVisualizer

import propsde.applications.run as run

#if not os.environ.get("PROPEXTRACTION_DE_HOME_DIR"):
#    print 'Please set PROPEXTRACTION_DE_HOME_DIR pointing to the PropS directory!'
#    exit()
#HOME_DIR = os.environ.get("PROPEXTRACTION_DE_HOME_DIR")+os.sep

def main(arguments):
    
    outputType = 'html'
    sep = "<br>"
    if arguments['-t']:
        outputType = 'pdf'
    sep = "\n"
        
    graphical = (outputType=='html')
    
    gs = run.parseSentences(arguments["file"])
        
    i = 0
    for g,tree in gs: 
    
        if arguments['INPUT']:
            file_name = os.path.splitext(arguments['INPUT'])[0] + unicode(i)
        else: 
            file_name = 'output' + unicode(i)
        
        # print sentence (only if in graphical mode)
        if (arguments["--original"]):
            sent = g.originalSentence
            print (sent+sep).encode('utf-8')
            
        #print dependency tree
        if (arguments['--dep']):
            if graphical:
                f = codecs.open(file_name + '_dep.svg', 'w', encoding='utf-8')
                try:
                    d = DepTreeVisualizer.from_conll_unicode(tree)
                    f.write(d.as_svg(compact=True,flat=True))
                except:
                    print 'error creating dep svg', file_name
                f.close()
            #else:
            print (tree).encode('utf-8')
        
        #print PropS output
        if (arguments['--props']):
            if graphical: 
                try:
                    dot = g.drawToFile("","svg")        
                    f = codecs.open(file_name + '_props.svg', 'w', encoding='utf-8')
                    f.write(dot.create(format='svg'))
                    f.close()
                except:
                    print 'error creating props svg', file_name
            #else:
            print unicode(g).encode('utf-8')
        
        #print open ie like extractions
        if (arguments["--oie"]):
            for prop in g.getPropositions('pdf'):
                print unicode(prop).encode('utf-8')
            
        print 
        i += 1
        

if __name__ == "__main__":
    arguments = docopt(__doc__)
    if arguments["INPUT"]:
        arguments["file"] = codecs.open(arguments["INPUT"], encoding='utf-8')
    else:
        arguments["file"] = sys.stdin
    main(arguments)


