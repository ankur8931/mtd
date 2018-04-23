#Dependencies: sudo apt-get install python-numpy python-scipy python-matplotlib
# networkx, Element Tree, json

import networkx as nx
import xml.etree.ElementTree as ET
import json
import matplotlib.pyplot as plt
import numpy as np
import mdptoolbox

class BWCentral:

    def __init__(self):

        self.G = nx.DiGraph()
        self.SG = nx.DiGraph()
        self.tree = ET.parse('/home/snac/ESORICS/mtd/data/ag-files/14/AttackGraph.xml')
        self.root = self.tree.getroot()

    def createGraph(self):

        arcs = self.root.find('arcs')

        for arc in arcs.findall('arc'):

            self.G.add_edge(int(arc.find('dst').text), int(arc.find('src').text))

        bw_central = nx.betweenness_centrality(self.G, normalized=False)

        bw_min = min(list(bw_central.values()))
        bw_max = max(list(bw_central.values()))

        for k,v in bw_central.items():

            bw_central[k] = round(((bw_central[k] - bw_min) / (bw_max - bw_min)),3)            
        
        ###Check attributes of the node ID####

        for node in self.G.nodes:
           
            for vertex in self.root.find('vertices'):

                if int(vertex.find('id').text) == int(node):

                   if 'vulExists' in vertex.find('fact').text:

                       self.G.node[node]['type'] = 'vulExists'

                   elif 'netAccess' in vertex.find('fact').text:

                       self.G.node[node]['type'] = 'netAccess'
                
                   elif 'execCode' in vertex.find('fact').text:

                       self.G.node[node]['type'] = 'execCode'

                   else:

                       self.G.node[node]['type'] = 'n-a'

        #####Check for successor of a given node####

        for node in self.G.nodes:

            if self.G.node[node]['type'] == 'vulExists':

                succNodes = list(nx.nodes(nx.dfs_tree(self.G, node)))

                for sNode in succNodes:

                    if self.G.node[sNode]['type'] == 'execCode' or self.G.node[sNode]['type'] == 'netAccess':

                       bw_central[node] = bw_central[sNode]


        print(bw_central)


if __name__ == "__main__":

   bw = BWCentral()  
   bw.createGraph()

