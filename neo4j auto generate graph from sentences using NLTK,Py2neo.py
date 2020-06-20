# -*- coding: utf-8 -*-
"""
Created on Fri May  1 21:04:24 2020

@author: Asad
"""

from py2neo import *
from nltk import pos_tag,word_tokenize
"""<-----------------------------------Helper Functions------------------------------>"""
def mergeHelpingverbs(stringList): # to make verb with underscore
    a=""
    if len(stringList)==0:
        return ""
    if len(stringList)<1:
        a=a+stringList.pop(0)
        return a.upper()
    for i in stringList:
        if(stringList[-1]!=i):
            a+=i+"_"
        elif(stringList[-1]==i):
            a+=i
    return a.upper()
def split_sentences(string): # to make sentences from paragraph.
    listofsentences=string.split('.')
    if(listofsentences[-1]=='' and len(listofsentences)<3):
        return [string]
    listofsentences.pop()
    return listofsentences
def generate_Tokens(sentences):
    tokens=word_tokenize(sentences)
    return tokens

def generate_parts_of_speech(tokens):
    pos=pos_tag(tokens)
    return pos

def process_Data(sentence):
    tokens=generate_Tokens(sentence)
    postTaggList=generate_parts_of_speech(tokens)
    nouns=[]
    verbs=[]
    properties=[]
    for item in postTaggList:
        if item[1] in ["NNP", 'NN', 'NNS', "NNS","JJ"]:
            nouns.append(item[0])
        elif item[1] in ["VBZ", "VBD", "VBG", "DT", "IN","VBP","TO","VB"]:
            verbs.append(item[0])
        elif item[1] in ["VBN", "RB"]:
            properties.append(item[0])
    return nouns,verbs,properties
"""<------------------------------------------Main Function-------------------->"""
def main():
    graph=Graph(password="asad1234") # enter correct password of neo4j graph
    input_paragraph="Cat is an animal.Cat has fur.Cat has blue eyes.Cat has long tail. Cat sat on mat. Bruce is a Cat. Bruce likes to eat Fish. Cat is a Mammal."
    #input_paragraph="Ali is a man. Ali likes Fish."
    lists=split_sentences(input_paragraph)
    print("Finalized list of sentences is"+str(lists))
    for eachSentence in lists:
        nouns, verbs, properties = process_Data(eachSentence)
        if len(properties)!=0:
            if len(nouns) == 2:
                nouns[1] = properties[0] + " " + nouns[1]
                properties[0]=nouns[1]
            for nodes in nouns:
                createNode = "MERGE(m:Node{ name:'" + nodes + "'}) on CREATE SET m.name='" + nodes + "'"
                graph.run(createNode)
            for prop in properties:
                createNodeProps = "MERGE(m:Node{ name:'" + prop + "'}) on CREATE SET m.name='" + prop + "' return m"
                graph.run(createNodeProps)
            relation = mergeHelpingverbs(verbs)
            query="MATCH(m:Node{name:'"+nouns[0]+"'}),(n:Node{name:'"+properties[0]+"'}) create unique (m)-[:"+relation+"]->(n)"
            graph.run(query)
        else:
            for nodes in nouns:
                createNode = "MERGE(m:Node{ name:'" + nodes + "'}) on CREATE SET m.name='" + nodes + "'"
                graph.run(createNode)
            rel=mergeHelpingverbs(verbs)
            query="MATCH(m:Node{name:'"+nouns[0]+"'}),(n:Node{name:'"+nouns[1]+"'}) create unique(m)-[:"+rel+"]->(n)"
            graph.run(query)

main()