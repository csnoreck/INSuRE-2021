import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import xml.etree.ElementTree as ET
#testesttest

#in order to connect to the web app. go to 127.0.0.1:8050

#these functions are a mess right now, there are a lot of things that are not necessary
#for current functionality
def parseXML_mod(filePath):
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
				if len(tmpPortData) != 1000:
					for x in range(1000 - len(tmpPortData)):
						tmpPortData += [0]
				data[hostIP] = tmpPortData
				tmpPortData = []
			#else: 
				#data[hostIP] = ''
			
	#</host>
	return hostList

def parseXML(filePath):
	tree = ET.parse(filePath)
	root = tree.getroot()

	#variables for data 
	data = {}
	tmpPortData = []
	hostIP = ''

	for host in root: #reads each host 

		if host.tag == 'host':

			for hostData in host: #reads tags under host tag

				if hostData.tag == 'address':
					#print(hostData.attrib['addr'], "Address Type:", hostData.attrib['addrtype'])
					hostIP = hostData.attrib['addr'] #
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

							for portDataDetails in portData:#reads tags under port tag

								#display port information
								if portDataDetails.tag == 'state':
									#print('		PortState:', portDataDetails.attrib['state'], '\n' 
										#'		Reason:', portDataDetails.attrib['reason'])
									portState = portDataDetails.attrib['state']
									portReason = portDataDetails.attrib['reason']
								#</state>

								if portDataDetails.tag == 'service':
									#print('		Service:', portDataDetails.attrib['name'])
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

def compileData(s1, s2, s3):
	data = {'hosts': [], 'scantime': []}

	for host in s3:
		data['hosts'] += [host]
		data['scantime'] += [3]

	for host in s1:
		data['hosts'] += [host]
		data['scantime'] += [1]

	for host in s2:
		data['hosts'] += [host]
		data['scantime'] += [2]

	

	return data


app = dash.Dash(__name__)
app.title = "Network Visualization"

#-------------------------------------------------------------------
scanData1 = parseXML_mod('test2Scan.xml')
scanData2 = parseXML_mod('testScan.xml')
scanData3 = parseXML_mod('test3Scan.xml')

df = compileData(scanData1, scanData2, scanData3)
#-------------------------------------------------------------------
fig = px.scatter(df, x="scantime", y="hosts")
fig.update_yaxes(categoryorder='category ascending')

app.layout = html.Div(children=[
    html.H1(children='Network Visualization Prototype'),

    html.Div(children='''
        Version 0.1
    '''),

    dcc.Graph(
        id='main-graph',
        figure=fig
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
