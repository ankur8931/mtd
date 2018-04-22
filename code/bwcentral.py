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
        self.tree = ET.parse('/home/snac/ESORICS/mtd/data/ag-files/15/AttackGraph.xml')
        self.root = self.tree.getroot()

    def createGraph(self):

        arcs = self.root.find('arcs')

        for arc in arcs.findall('arc'):

            self.G.add_edge(int(arc.find('src').text), int(arc.find('dst').text))
        bw_central = nx.betweenness_centrality(self.G, normalized=False)

        bw_min = min(list(bw_central.values()))
        bw_max = max(list(bw_central.values()))

        for k,v in bw_central.items():

            bw_central[k] = round(((bw_central[k] - bw_min) / (bw_max - bw_min)),3)
            
        print(bw_central)


if __name__ == "__main__":

   bw = BWCentral()  
   bw.createGraph()

