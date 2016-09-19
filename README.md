What is PropS?
------------
PropS offers an output representation designed to explicitly and uniformly express much of the proposition structure which is implied from syntax.

Semantic NLP applications often rely on dependency trees to recognize major elements of the proposition structure of sentences. 
Yet, while much semantic structure is indeed expressed by syntax, many phenomena are not easily read out of dependency trees, often leading to further ad-hoc heuristic post-processing or to information loss. 
For that end, PropS post-processes dependency trees to present a compelling representation for downstream tasks.

Find more details, examples, and an online demo at the [project page](http:/www.cs.biu.ac.il/~stanovg/props.html).


What is PropsDE?
------------
PropsDE is an adaption of the original PropS system to the German language. 
It can be used to transform German sentences into proposition structures and to extract Open IE tuples from them. 

The portation from English to German is described in the following paper that you might want to cite in case you use the software in your work:

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

English version:	[github repo](https://github.com/gabrielStanovsky/props) 

Online demo: 		[demo page](http:/www.cs.biu.ac.il/~stanovg/props.html) 

Contact person: Tobias Falke, lastname(at)aiphes.informatik.tu-darmstadt.de

http://www.aiphes.tu-darmstadt.de/

> This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication. 


Installation
------------
Run 'python ./setup.py install' from the props root directory.
This will install several python packages and other resources which PropS uses and relies upon (see [requirements.txt](props/install/requirements.txt) and [install.sh](props/install/install.sh) for the complete list).

MacOS users might run into issues installing JPype. An instruction to manually install JPype on MacOS can be found on the [berkely parser python interface repository](https://github.com/emcnany/berkeleyinterface#installation-and-dependencies).

PROPEXTRACTION_DE_HOME_DIR

Prerequisites
-------------

* python 2.7
* java 7 (make sure to set the JAVA_HOME enviroment variable (e.g., /usr/lib/[*your_java_folder*])


Running the system
-------------

to be added

