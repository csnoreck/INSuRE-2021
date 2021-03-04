import pandas as pd
import plotly.express as px

#df = pd.read_csv('/home/user/Desktop/Project/BigScans/2021-01-06-1609951803-telnet_9527')

app = dash.Dash(__name__)
app.title = "Network Visualization"

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

df = pd.DataFrame.from_dict(parseXML('/home/user/Desktop/Project/test2Scan.xml'), dtype = str, orient = 'index')

app.layout = html.Div([
      visdcc.Network(id = 'net', 
                     options = dict(height= '600px', width= '100%')),
      dcc.Input(id = 'label',
                placeholder = 'Enter a label ...',
                type = 'text',
                value = ''  ),
      html.Br(),html.Br(),
      dcc.RadioItems(id = 'color',
                     options=[{'label': 'Red'  , 'value': '#ff0000'},
                              {'label': 'Green', 'value': '#00ff00'},
                              {'label': 'Blue' , 'value': '#0000ff'} ],
                     value='Red'  )             
])

@app.callback(
    Output('net', 'data'),
    [Input('label', 'value')])

def myfun(x):
    data ={'nodes':[{'id': 1, 'label':    x    , 'color':'#00ffff'},
                    {'id': 2, 'label': '192.168.1.1'},
                    {'id': 4, 'label': 'Node 4'},
                    {'id': 5, 'label': 'Node 5'},
                    {'id': 6, 'label': 'Node 6'}                    ],
           'edges':[{'id':'1-3', 'from': 1, 'to': 3},
                    {'id':'1-2', 'from': 1, 'to': 2} ]
           }
    return data

@app.callback(
    Output('net', 'options'),
    [Input('color', 'value')])

def myfun(x):
    return {'nodes':{'color': x}}
if __name__ == '__main__':
    app.run_server(debug=True)