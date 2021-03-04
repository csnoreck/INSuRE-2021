import networkx as nx
#import matplotlib.pyplot as plt
from bokeh.io import output_file, show
from bokeh.plotting import figure, from_networkx
#from bokeh.models import ColumnDataSource

import xml.etree.ElementTree as ET

def parseXML(fileName):
	tree = ET.parse(fileName)
	root = tree.getroot()

	#variables for data 
	data = {}
	tmpPortData = []
	hostIP = ''

	for host in root: #reads each host 

		if host.tag == 'host':

			for hostData in host: #reads tags under host tag

				if hostData.tag == 'address':
					hostIP = hostData.attrib['addr'] #
				#</address>

				if hostData.tag == 'status':
					state = hostData.attrib['state']
				#</status>

				if hostData.tag == 'ports':
					for portData in hostData:#reads tags under ports tag

						if portData.tag == 'port':
							portNum = portData.attrib['portid']

							for portDataDetails in portData:#reads tags under port tag

								#display port information
								if portDataDetails.tag == 'state':
									portState = portDataDetails.attrib['state']
									portReason = portDataDetails.attrib['reason']
								#</state>

								if portDataDetails.tag == 'service':
									portName = portDataDetails.attrib['name']
								#</service>

							tmpPortData += [portNum, [portState, portReason, portName]]
						#</port>
				#</ports>

			if tmpPortData is not None: 
				data[hostIP] = tmpPortData
				tmpPortData = []
			#else: 
				#data[hostIP] = ''
			
	#</host>

	return data

hosts = parseXML('/home/user/Desktop/Project/test2Scan.xml')
'''{"192.168.1.1": "TestData",
			 "192.168.1.2": "TestData",
			 "192.168.1.3": "TestData",
			 "192.168.1.4": "TestData"}'''

hostConnections = [["192.168.1.1", "192.168.1.2"], ["192.168.1.9", "192.168.1.18"]]

#G = nx.Graph()
G = nx.Graph()
G.add_nodes_from(hosts)
G.add_edges_from(hostConnections)



plot = figure(title="Networkx - Bokeh Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
              tools="hover, pan, box_zoom")

graph = from_networkx(G, nx.planar_layout, center=(0,0))
plot.renderers.append(graph)

output_file("networkx_graph.html")
show(plot)