
# PropsDE

What is PropsDE?
------------
PropsDE is an adaption of the original PropS system to the German language. 
It can be used to transform German sentences into proposition structures and to extract Open IE tuples from them.

[original English version](https://github.com/gabrielStanovsky/props) 

[online demo for English and German](http:/www.cs.biu.ac.il/~stanovg/props.html)  

The portation from English to German is described in the following paper. Please cite it in case you use the software in your work:

```
@InProceedings{TUD-CS-2016-0181,
  author    = {Tobias Falke and Gabriel Stanovsky and Iryna Gurevych and Ido Dagan},
  title     = {Porting an Open Information Extraction System from English to German},
  booktitle = {Proceedings of the 2016 Conference on Empirical Methods in Natural Language
Processing (EMNLP)},
  month     = {November},
  year      = {2016},
  address   = {Austin, Texas},
  publisher = {Association for Computational Linguistics},
  pages     = {(to appear)},
  url       = {(to appear)}
}
```

Contact person: Tobias Falke, lastname(at)aiphes.informatik.tu-darmstadt.de

http://www.aiphes.tu-darmstadt.de/

> This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication. 

What is PropS?
------------
PropS offers an output representation designed to explicitly and uniformly express much of the proposition structure which is implied from syntax.

Semantic NLP applications often rely on dependency trees to recognize major elements of the proposition structure of sentences. 
Yet, while much semantic structure is indeed expressed by syntax, many phenomena are not easily read out of dependency trees, often leading to further ad-hoc heuristic post-processing or to information loss. 
For that end, PropS post-processes dependency trees to present a compelling representation for downstream tasks.


Prerequisites
-------------

* python >= 2.7 (tested with 2.7.6)
* java >= 7 (JAVA_HOME has to be set)

Installation
------------

1. Clone this repository and navigate into the root folder.

        git clone https://github.com/tbsflk/props-de.git 
		cd props-de

2. Install required python packages.

		pip install -r requirements.txt
		
3. Download java dependencies (Mate-Tools with models and JoBimText).

		./ext/load_java_dependencies.sh
		
4. (Optional) To produce graphical output with the parsing script, [graphviz](http://www.graphviz.org/) has to be installed and callable from command line.

5. (Optional) To produce graphical output in the web demo, you need a copy of [brat](http://brat.nlplab.org/) and point to it in the server script.



Running
-------------

Two scripts are available in the root folder to use PropsDE:

- *parse_props.py*

    Can be called to parse sentences in a file. The file must have one sentence per line. Example:
	
		python parse_props.py -t --props --oie example.txt
		
	Use -h to see all options. Graphical representations are produced as SVG files in the same directory as the input file.

- *parse_server.py*

	Can be called to start a bottle webserver serving a small demo web page. This also shows how to call the dependency parser via JPype, requiring the model to be loaded only once when starting the server.

