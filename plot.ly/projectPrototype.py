#library imports
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import os
from dash.dependencies import Input, Output, State

#in order to connect to the web app. go to 127.0.0.1:8050

#these functions are a mess right now, there are a lot of things that are not necessary
#for current functionality
import xml.etree.ElementTree as ET

def parseXML(filePath):
	tree = ET.parse(filePath)
	root = tree.getroot()

	#variables for data 
	data = {}
	tmpPortData = []
	hostList = []
	hostIP = ''

	for host in root: #reads each host 

		if host.tag == 'host':

			for hostData in host: #reads tags under host tag

				if hostData.tag == 'address':
					#print(hostData.attrib['addr'], "Address Type:", hostData.attrib['addrtype'])
					hostIP = hostData.attrib['addr'] 
					hostList += [hostIP]
				#</address>

				if hostData.tag == 'status':
					#print('Status:', hostData.attrib['state'])
					state = hostData.attrib['state']
				#</status>

				if hostData.tag == 'ports':
					for portData in hostData:#reads tags under ports tag

						if portData.tag == 'port':
							#print('	Port:', portData.attrib['portid'])	
							portNum = portData.attrib['portid']

							tmpPortData += [portNum]
						#</port>
				#</ports>

			if tmpPortData is not None:
				'''if len(tmpPortData) != 1000:
					for x in range(1000 - len(tmpPortData)):
						tmpPortData += [0]'''
				data[hostIP] = tmpPortData
				tmpPortData = []
			#else: 
				#data[hostIP] = ''
			
	#</host>
	return hostList, data

def compileGraphData(s1, s2=None, s3=None, s4=None, s5=None, s6=None, s7=None, s8=None):
	data = {'hosts': [], 'scantime': []}

	for host in s1:
		data['hosts'] += [host]
		data['scantime'] += [1]
	if s2 != None:
		for host in s2:
			data['hosts'] += [host]
			data['scantime'] += [2]
	if s3 != None:
		for host in s3:
			data['hosts'] += [host]
			data['scantime'] += [3]
	if s4 != None:
		for host in s4:
			data['hosts'] += [host]
			data['scantime'] += [4]
	if s5 != None:
		for host in s5:
			data['hosts'] += [host]
			data['scantime'] += [5]
	if s6 != None:
		for host in s6:
			data['hosts'] += [host]
			data['scantime'] += [6]
	if s7 != None:
		for host in s7:
			data['hosts'] += [host]
			data['scantime'] += [7]
	if s8 != None:
		for host in s8:
			data['hosts'] += [host]
			data['scantime'] += [8]

	return data

def mergeDicts(d1, d2=None, d3=None, d4=None, d5=None, d6=None, d7=None, d8=None):

	fullDictionary = d1

	if d2 != None: # if d2 doesnt exist, then no processing is required
		for host, portList in d2.items():
			#check if host in new dictionary is not in the full dict
			#if not, add it  
			if host not in fullDictionary:
				fullDictionary[host] = portList
	if d3 != None:
		for host, portList in d3.items(): 
			if host not in fullDictionary:
				fullDictionary[host] = portList
	if d4 != None:
		for host, portList in d4.items(): 
			if host not in fullDictionary:
				fullDictionary[host] = portList
	if d5 != None:
		for host, portList in d5.items(): 
			if host not in fullDictionary:
				fullDictionary[host] = portList
	if d6 != None:
		for host, portList in d6.items(): 
			if host not in fullDictionary:
				fullDictionary[host] = portList
	if d7 != None:
		for host, portList in d7.items(): 
			if host not in fullDictionary:
				fullDictionary[host] = portList
	if d8 != None:
		for host, portList in d8.items(): 
			if host not in fullDictionary:
				fullDictionary[host] = portList

	return fullDictionary


def displayPortInfo(portList):
	output = ''

	for port in portList:
		output += (str(port) + os.linesep)
	#print(output)
	return output

app = dash.Dash(__name__)
app.title = "Network Visualization"

#-------------------------------------------------------------------
scanData1 = parseXML('testScan.xml')
scanData2 = parseXML('test2Scan.xml')
scanData3 = parseXML('test3Scan.xml')

#create a new full dictionary that conatins info from all the scans. 
portInfo = mergeDicts(scanData1[1], scanData2[1], scanData3[1])

#compile the different scans into 1 dataframe (df) to be used by ploy.ly express (px)
df = compileGraphData(scanData1[0], scanData2[0], scanData3[0])
#-------------------------------------------------------------------
fig = px.scatter(df, x="scantime", y="hosts")
fig.update_yaxes(categoryorder='category ascending') # order hosts

app.layout = html.Div(children=[
    html.H1(children='Network Visualization Prototype'),

    html.Div(children='''
        Version 0.1
    '''),

    dcc.Graph(
        id='main-graph',
        figure=fig
    ),

    html.Div(children='''
        Enter a host to view its open ports
    '''),

    dcc.Input(
    	placeholder='Enter a host...',
    	type='text',
    	value='',
    	id='host_input'
    	),

    html.Button(id='search-button-state', n_clicks=0, children='Search'),

    html.Table(id='port_data')
])

'''
app.callback provides the functionality to the host search, it must be followed
 	by the callback function declaration (in this case update_output_div).
	offical documentation can be found here: https://dash.plotly.com/basic-callbacks
 		'''
@app.callback(
    Output(component_id='port_data', component_property='children'),
    Input('search-button-state', 'n_clicks'),
    State('host_input', 'value')       
)

# define what to do when the callback is activated 
def update_output_div(n_clicks, input_value):
	if input_value in portInfo:
		#return 'Ports: '  + str(portInfo[input_value])
		return displayPortInfo(portInfo[input_value])
	else:
		return 'Not a valid host'

@app.callback(
     Output(component_id='host_input', component_property='value'),
     Input(component_id='main-graph', component_property='clickData')
)

def display_click_data(clickData):
	if clickData is not None:
		json_object = json.loads(json.dumps(clickData, indent=2))
		inner_json_object = json_object["points"]
		y_value = inner_json_object[0]
		y_second_value = y_value["y"]
		test = [y_second_value]
		return y_second_value
	#return json.dumps(clickData, indent=2)

if __name__ == '__main__':
    app.run_server(debug=True)
