#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs, os
from jpype import *
from nltk.tokenize import word_tokenize

"""
Interface for dependency parsing of sentences in German 
- calls mate-tools for parsing
- calls JoBimText for collapsing and propagation
For mate-tools, two options are possible:
1) call directly from python via jpype (allows models to be loaded for several calls)
2) call jars on command-line and read output (loads models on every call)
"""
class ParserDE(object):

    def __init__(self, jpype):
        self.isJPype = jpype
        self.tmp = 'tmp'
        self.model_path_lem = 'ext/mate-model/lemma-ger.model'
        self.model_path_parse = 'ext/mate-model/parser-ger.model'
        if not os.path.exists(self.model_path_lem) or not os.path.exists(self.model_path_lem):
            print 'mate-tools model not found!'
            exit()
        self.setup()
        
    # load models if using jpype 
    def setup(self):
        if self.isJPype:
            print 'loading mate-tools'
            startJVM(getDefaultJVMPath(), '-Xmx4g', '-Djava.class.path=ext/transition-1.30.jar')
            self.is2 = JPackage('is2')
            self.lem = self.is2.lemmatizer2.Lemmatizer(self.model_path_lem)
            self.parser = self.is2.transitionS2a.Parser(self.model_path_parse)
            print 'mate-tools ready'
        
    # shutdown JVM
    def shutdown(self):
        shutdownJVM()
        
    # delegate parsing to prefered method
    def parse(self, sentences):
        if self.isJPype:
            parsed_conll09 = self.parse_jype(sentences)
        else:
            parsed_conll09 = self.parse_external(sentences)
        return self.collapse(parsed_conll09)
        
    # call parser via jpype
    def parse_jype(self, sentences):
        conll = []
        for sent in sentences:
        
            sent = sent.replace(u"“"," ").replace(u"”","")
            tokens = [u'<root>'] + word_tokenize(sent, language="german")
            
            s = self.is2.data.SentenceData09()
            s.init(tokens)
            s = self.lem.apply(s)
            
            s2 = self.is2.data.SentenceData09()
            s2.createWithRoot(s)
            self.parser.apply(s2)
            
            conll.append(s2.toString())
            
        output = codecs.open(self.tmp+'/parsed.conll09', 'w', encoding='utf-8')
        for s in conll:
            output.write(s + '\n')
        output.close()
        
        return self.tmp+'/parsed.conll09'
    
    # call parser via external jar
    def parse_external(self, sentences):

        # save sentence to file 
        input = codecs.open(self.tmp+'/input.conll09', 'w', encoding='utf-8')
        for sent in sentences:
            sent = sent.replace(u"“"," ").replace(u"”","")
            i = 1
            for token in word_tokenize(sent, language="german"):
                input.write(u"\t".join([str(i),token] + ["_"]*13) + "\n")
                i += 1
            input.write("\n")
        input.close()

        print "running mate-tools"

        # lemmatizing
        cmd = 'java -cp ext/transition-1.30.jar is2.lemmatizer2.Lemmatizer -model '+self.model_path_lem+' -test '+self.tmp+'/input.conll09 -out '+self.tmp+'/lemmatized.conll09'
        print "lemmatizing"
        res = os.popen(cmd)
        res.close()

        # parsing -> joint parsing and tagging
        cmd = 'java -Xmx4g -cp ext/transition-1.30.jar is2.transitionS2a.Parser -model '+self.model_path_parse+' -test '+self.tmp+'/lemmatized.conll09 -out '+self.tmp+'/parsed.conll09'
        print "parsing + tagging"
        res = os.popen(cmd)
        res.close()
        
        return self.tmp+'/parsed.conll09'
        
    # collapse dependencies in given file
    def collapse(self, file):

        # convert to conll06
        input = codecs.open(file, encoding='utf-8')
        file06 = file.replace('.conll09','.conll06')
        output = codecs.open(file06,'w',encoding='utf-8')
        for line in input:
            cols = line.strip().split("\t")
            if len(cols) != 14:
                output.write(line)
            else:
                output.write("\t".join(cols[0:2]+cols[3:4]+cols[5:6]+cols[5:7]+cols[9:10]+cols[11:14]) + "\n")
        input.close()
        output.close()

        # dependency collapsing
        cmd = 'java -jar ext/org.jobimtext.collapsing.jar -i '+file06+' -o . -sf -l de -r ext/resources/german_modified.txt -f c -np -nt'
        print "collapsing"
        res = os.popen(cmd)
        res.close()

        return file.replace('.conll09','.conll')       
        