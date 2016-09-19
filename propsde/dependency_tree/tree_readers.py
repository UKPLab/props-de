import re, codecs, sys
from propsde.graph_representation.graph_wrapper import GraphWrapper, ignore_labels
from propsde.graph_representation.newNode import Node
from propsde.graph_representation.word import Word
from propsde.proposition_structure.syntactic_item import get_verbal_features

import os
from propsde.dependency_tree.tree import *
from propsde.utils.utils import encode_german_characters

# TIGER in conll09 format
#  1_2	Ross	Ross	_	NE	_	case=nom|number=sg|gender=masc	_	3	_	PNC	_	_	_	_
# 0: sentenceId_tokenId
# 1: word form
# 2/3: lemma
# 4/5: pos
# 6/7: feature
# 8/9: dep head
# 10/11: dep relation
TIGER_FILE = ''


def get_conll_from_tiger_file(sent_ids):
    target_ids = set(sent_ids)
    current_id = -1
    sentences = {}
    sent = []
    for line in codecs.open(TIGER_FILE, encoding='utf-8'):
        cols = line.strip().split('\t')
        ids = cols[0].split('_')
        if len(cols) != 15:
            if len(sent) > 0:
                sentences[current_id] = sent
        else:
            if current_id != ids[0] and ids[0] in target_ids:
                current_id = ids[0]
                sent = []
            if current_id == ids[0]:
                cols[0] = ids[1]
                sent.append(cols)
        if len(sentences) == len(target_ids):
            break
    return [sentences[id] for id in sent_ids]
        
def get_conll_from_parser_file(file_parsed):
    #   1	Dieser	dies	PDAT	PDAT	_	2	NK	_	_
    sentences = []
    sent = []
    for line in codecs.open(file_parsed, encoding='utf-8'):
        cols = line.strip().split('\t')
        if len(cols) == 10:
            cols = cols[0:6] + ['_','_'] + cols[6:7] + ['_'] + cols[7:8]
            sent.append(cols)
        else:
            if len(sent) > 0:
                sentences.append(sent)
                sent = []
    return add_morph_features(file_parsed, sentences)
    
def add_morph_features(file_parsed, sentences):
    if os.path.exists(file_parsed+'09'):
        morph = []
        map = {}
        for line in codecs.open(file_parsed+'09', encoding='utf-8'):
            cols = line.strip().split('\t')
            if len(cols) == 14:
                map[cols[0]] = cols[7]
            else:
                if len(map) > 0:
                    morph.append(map)
                    map = {}
        for i, sent in enumerate(sentences):
            for token in sent:
                token[7] = morph[i][token[0]]
    return sentences

def create_dep_graphs_from_conll(sentences_conll,HOME_DIR):

    graphs = []
    
    for sentence_conll in sentences_conll:
    
        curGraph = GraphWrapper("",HOME_DIR)
        nodesMap = {}
        
        # nodes
        for cols in sentence_conll:
            if cols[8] != '_':
                id = int(cols[0])
                word_form = cols[1]
                if not id in nodesMap:
                    nodesMap[id] = Node(text=[Word(index=id,word=word_form)],
                                     isPredicate=False,
                                     features={},
                                     gr=curGraph,
                                     orderText=True)
        nodesMap[0] = Node(text=[Word(index=0,word='ROOT')],
                             isPredicate=False,
                             features={},
                             gr=curGraph,
                             orderText=True)
        
        # edges
        for cols in sentence_conll:
            if cols[8] != '_':
                rel = encode_german_characters(cols[10])
                if int(cols[8]) in nodesMap and int(cols[0]) in nodesMap:
                    headNode = nodesMap[int(cols[8])]
                    depNode = nodesMap[int(cols[0])]
                    if curGraph.has_edge((headNode,depNode)): # stanford bug
                        curGraph.del_edge((headNode,depNode))
                    curGraph.add_edge(edge=(headNode,depNode), label=rel)

        graphs.append((curGraph,nodesMap))
        
    return graphs



# Input :   stream of dep trees converted by Stanford parser
# Output:   List of DepTree
def create_dep_trees_from_conll(sentences_conll, sent_id):

    dep_trees = []
    
    for sentence_conll in sentences_conll:
    
        init_flag = True
        wsj_id, sent_id = 0,0
        words = []
        
        dep_trees_data = {0:[]}
        dep_trees_nodes = {0:DepTree(pos="",word="ROOT",id=0,parent=None,parent_relation="",children=[],sent_id = int(sent_id))}
               
        for cols in sentence_conll:
            node = cols
            id = int(node[0])
            if not id in dep_trees_nodes:
                words.append(node[1])
                dep_trees_data[id]=node
                dep_trees_nodes[id]=DepTree(pos=node[4],word=node[1],id=node[0],parent=None,parent_relation=node[10],children=[],sent_id = int(sent_id),lemma=node[2],morph=node[7])
                
        # Going through all nodes and update connections between them
        for i in filter(lambda x:x,dep_trees_nodes.keys()):
           node_data = dep_trees_data[i]
           node = dep_trees_nodes[i]
           if node_data[8] != '_':
               parent_id = int(node_data[8])
               # Set node's parent
               node.set_parent(dep_trees_nodes[parent_id])
               # Set node's parent id
               node.set_parent_id(parent_id)
               # Set the node to the child list of the parent
               dep_trees_nodes[parent_id].add_child(node)
                   
        # Add parsed DepTree to the list
        dep_trees_nodes[0].original_sentence = u" ".join(words)
        dep_trees.append(copy.copy(dep_trees_nodes))
        
    return dep_trees


def missing_children(treeNode,graphNode):
    neighbors = graphNode.neighbors()
    ret = [Word(index=c.id,word=c.word) for c in treeNode.children if (c.parent_relation not in neighbors) or (c.id != neighbors[c.parent_relation][0].text[0].index) or (c.parent_relation in ignore_labels)]
    return []


def read_dep_graphs(sent_ids,file_parsed,HOME_DIR):

    if sent_ids:
        sentences_conll = get_conll_from_tiger_file(sent_ids)
        
    if file_parsed:
        sentences_conll = get_conll_from_parser_file(file_parsed)
    
    graphsFromFile = create_dep_graphs_from_conll(sentences_conll,HOME_DIR)
    trees = create_dep_trees_from_conll(sentences_conll,sent_ids)
    
    graphs = []
    for i,t in enumerate(trees):
        
        curGraph,nodesMap = graphsFromFile[i]
        curGraph.set_original_sentence(t[0].original_sentence)
        curGraph.tree_str = u"\n".join(t[0].to_original_format().split("\n")[1:])
        for node_id in nodesMap:
            int_node_id = node_id
            treeNode = t[int_node_id]
            child_dic = treeNode._get_child_dic()
            for rel in child_dic:
                if rel.startswith('CJ_'):    
                    conj_type = (rel[3:],[cc.id for cc in child_dic[rel]])
            else:
                conj_type = False
            graphNodes = [nodesMap[n] for n in nodesMap if n == node_id]
            for graphNode in graphNodes:
                graphNode.features = get_verbal_features(treeNode)
                if conj_type:
                    graphNode.features["conjType"] = conj_type
                graphNode.features["pos"]=treeNode.pos
                graphNode.isPredicate = treeNode.is_verbal_predicate()
                graphNode.original_text = treeNode.get_text()
                graphNode.surface_form += missing_children(treeNode,graphNode)
        curGraph.del_node(nodesMap[0]) # delete root
        
        graphs.append(curGraph)   
        
    return graphs
