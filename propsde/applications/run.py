#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs, os, sys
from propsde.dependency_tree.tree_readers import *
from propsde.dependency_tree.german_parser import ParserDE
from propsde.graph_representation.graph_wrapper import GraphWrapper
from propsde.graph_representation.convert import convert

"""
Call to MateParser and parsing of output
"""

parser = None
#HOME_DIR = os.environ.get("PROPEXTRACTION_DE_HOME_DIR", ".") + os.sep

def loadParser():
    global parser
    parser = ParserDE(True)

def parseSentences(sentences):
    global parser

    if not parser:
        parser = ParserDE(False)

    # call the dependency parser
    output_file = parser.parse(sentences)
    
    # read and process output
    graphs = read_dep_graphs(None, output_file)
    
    ret = []
    i = 0
    for graph in graphs:  
        g = convert(graph)
        ret.append((g,g.tree_str))
        i += 1

    if not graphs:#Berkley bug?
        ret.append((GraphWrapper("",""),""))
        
    return ret
 