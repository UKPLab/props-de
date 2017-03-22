#!/bin/bash

# Load non-python dependencies for PropsDE

# Mate-Tools Dependency Parser
# > parser
wget 'https://drive.google.com/uc?export=download&id=0B-qbj-8rtoUMbVEzWDlvd0ZxVFU' -O transition-1.30.jar
# > models
mkdir -p mate-model
wget 'https://drive.google.com/uc?export=download&id=0B-qbj-8rtoUMaUVsWUFuOE81ZW8' -O mate-model/lemma-ger.model

#wget 'https://docs.google.com/uc?export=download&id=0B-qbj-8rtoUMLUg5NGpBVW9JNkE' -O mate-model/parser-ger.model

# JoBimText Dependency Collapsing
wget 'http://ltmaggie.informatik.uni-hamburg.de/jobimtext/wordpress/wp-content/uploads/2015/10/collapsing-asl.zip' -O collapsing-asl.zip
unzip collapsing-asl.zip
mv collapsing-asl/org.jobimtext.collapsing.jar org.jobimtext.collapsing.jar 
mv collapsing-asl/org.jobimtext.collapsing_lib org.jobimtext.collapsing_lib
rm -r collapsing-asl
rm collapsing-asl.zip

# Create temp folder for parsing
cd ..
mkdir -p tmp
