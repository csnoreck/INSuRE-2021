#library imports
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import os
import fnmatch
import csv
from dash.dependencies import Input, Output, State
import pandas as pd

#in order to connect to the web app, first run this file, and go to 127.0.0.1:8050

#these functions are a mess right now, there are a lot of things that are not necessary
#for current functionality
import xml.etree.ElementTree as ET

#funcitons
#-----------------------------------------------------------------------------------------------------------
def parseXML(filePath):
    tree = ET.parse(filePath)
    root = tree.getroot()

    #variables for data 
    data = {}
    tmpPortProtocol = []
    tmpPortNum = []
    tmpPortStatus = []
    hostList = [0]
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
                            #print('    Port:', portData.attrib['portid'])  
                            portNum = portData.attrib['portid']
                            portProtocol = portData.attrib['protocol']

                            tmpPortNum += [portNum]
                            tmpPortProtocol += [portProtocol]
                            
                            for portInfo in portData:
                                if portInfo.tag == 'state':
                                    portStatus = portInfo.attrib['state']

                                    tmpPortStatus += [portStatus]
                        #</port>
                #</ports>

            if tmpPortNum is not None:
                data[hostIP] = [tmpPortProtocol, tmpPortNum, tmpPortStatus]
                tmpPortNum = []
                tmpPortStatus = []
                tmpPortProtocol = []
            #else: 
                #data[hostIP] = ''
        elif host.tag == 'runstats':
            for child in host:
                if child.tag == 'finished':
                    hostList[0] = child.attrib['timestr']
                #print(child)

    #</host>
    return hostList, data

#returns a dict read of a csv, which should be formatted as follows "PortNumber,ServiceName"
def parseCSV(filePath):
    file =open(filePath, "r")
    output = {}
    for line in file:
        tmp = line.rstrip().replace('"', '').split(',')
        output[tmp[0].upper()+tmp[1]] = tmp[2] #creates entry in python dict for each port/service // tmp[0] = Protocol | tmp[1] = PortNumber | tmp[2] = ServiceName
    return output

def compileGraphData(s1, s2=None, s3=None, s4=None, s5=None, s6=None, s7=None, s8=None):
    data = {'hosts': [], 'scantime': [], 'filtered': []}

    if s1 != None:
        scantime = s1[0]
        s1.remove(s1[0])
        for host in s1:
            data['hosts'] += [host]
            data['scantime'] += [scantime]
            data['filtered'] += ['No']
    if s2 != None:
        scantime = s2[0]
        s2.remove(s2[0])
        for host in s2:
            data['hosts'] += [host]
            data['scantime'] += [scantime]
            data['filtered'] += ['No']
    if s3 != None:
        scantime = s3[0]
        s3.remove(s3[0])
        for host in s3:
            data['hosts'] += [host]
            data['scantime'] += [scantime]
            data['filtered'] += ['No']
    if s4 != None:
        scantime = s4[0]
        s4.remove(s4[0])
        for host in s4:
            data['hosts'] += [host]
            data['scantime'] += [scantime]
            data['filtered'] += ['No']
    if s5 != None:
        scantime = s5[0]
        s5.remove(s5[0])
        for host in s5:
            data['hosts'] += [host]
            data['scantime'] += [scantime]
            data['filtered'] += ['No']
    if s6 != None:
        scantime = s6[0]
        s6.remove(s6[0])
        for host in s6:
            data['hosts'] += [host]
            data['scantime'] += [scantime]
            data['filtered'] += ['No']
    if s7 != None:
        scantime = s7[0]
        s7.remove(s7[0])
        for host in s7:
            data['hosts'] += [host]
            data['scantime'] += [scantime]
            data['filtered'] += ['No']
    if s8 != None:
        scantime = s8[0]
        s8.remove(s8[0])
        for host in s8:
            data['hosts'] += [host]
            data['scantime'] += [scantime]
            data['filtered'] += ['No']

    return data

def mergeDicts(s1, s2=None, s3=None, s4=None, s5=None, s6=None, s7=None, s8=None):
    timeStamp = s1[0][0]#pulls timstamp from scandata, first key is accesses hostdata, second speciefies the actual timestamp from the hostlist
    fullDictionary = {timeStamp: s1[1]} #creates a 2d dict [time][hostlist]

    if s2 != None: # if s2 doesnt exist, then no processing is required
        timeStamp = s2[0][0]#set timestamp to new scan's timestamp
        fullDictionary[timeStamp] = s2[1]#assign new scantimes data to 2d dict [time][hostlist]
    if s3 != None: 
        timeStamp = s3[0][0]
        fullDictionary[timeStamp] = s3[1]
    if s4 != None: 
        timeStamp = s4[0][0]
        fullDictionary[timeStamp] = s4[1]
    if s5 != None: 
        timeStamp = s5[0][0]
        fullDictionary[timeStamp] = s5[1]
    if s6 != None: 
        timeStamp = s6[0][0]
        fullDictionary[timeStamp] = s6[1]
    if s7 != None: 
        timeStamp = s7[0][0]
        fullDictionary[timeStamp] = s7[1]
    if s8 != None: 
        timeStamp = s8[0][0]
        fullDictionary[timeStamp] = s8[1]  
    
    return fullDictionary

def displayPortInfo(portInfo, ip):
    #add ports to table if there are ports
    if portInfo:#checks if there is data for the ports

        #define initial table header
        portTable = [
        html.Tr(),
        html.Th(children='Port Number'),
        html.Th(children='Protocol'),
        html.Th(children='Service'),
        html.Th(children='State'),
        html.Th(children='Scan Time'),
        html.Tr()
        ]
        for timeStamp in portInfo:#loop through 2d array
            try:#if ip is not in this time, then skip this interation of the for ie skip this timestamp
                portProtocolList = portInfo[timeStamp][ip][0]
                portNumList = portInfo[timeStamp][ip][1]
                portState = portInfo[timeStamp][ip][2]
            except:
                continue                
            #parse portDictionary csv file
            portDictionary = parseCSV('portDictionaryLarge.csv')

            #add ports to table, creating a new row for each port
            for x in range(len(portProtocolList)):
                dicKey = portProtocolList[x].upper()+portNumList[x]
                #if port is know to dictonary, display service name
                if dicKey in portDictionary:
                    portTable += [html.Tr(),
                                  html.Td(children=str(portNumList[x])), 
                                  html.Td(children=str(portProtocolList[x])), 
                                  html.Td(children=str(portDictionary[dicKey])),
                                  html.Td(children=str(portState[x])),
                                  html.Td(children=str(timeStamp))]
                else:
                    portTable += [html.Tr(),
                                  html.Td(children=str(portNumList[x])), 
                                  html.Td(children=str(portProtocolList[x])), 
                                  html.Td(children='Unknown Service'),
                                  html.Td(children=str(portState[x])),
                                  html.Td(children=str(timeStamp))]
            #add formating row to make table more readable
            portTable += [
                html.Tr(),
                html.Th(children='----------'),
                html.Th(children='----------'),
                html.Th(children='--------------------'),
                html.Th(children='-----'),
                html.Th(children='---------------')
            ]
        return portTable
    else:
        return 'No Open Ports detected'

def findAndFlag(df, searchterm):
    indices = [i for i, x in enumerate(df['hosts']) if fnmatch.fnmatch(x, searchterm)] #loops and finds all indices of the searchterm
    
    if indices != []:
        for i in indices:
            df['filtered'][i] = 'Yes'

        #define color index for graph color coding
        colorsIdx = {'No': 'rgb(0,0,255)', 'Yes': 'rgb(0,255,0)'}
        #recreate graph with filter applied
        fig = px.scatter(df, x="scantime", y="hosts", color = 'filtered', color_discrete_map=colorsIdx)
        #style graph
        fig.update_yaxes(categoryorder='category ascending')
        fig.update_traces(marker=dict(line=dict(width=1.1, color='DarkSlateGrey')), selector=dict(mode='markers'))
        fig.update_xaxes(dtick = 1)

        #flip filter flags back to 'No' for filter integrity (since df was already used the graph will still update correctly)
        for i in indices:
            df['filtered'][i] = 'No'

        return fig
    else:
        #create graph and style it
        colorsIdx = {'No': 'rgb(0,0,255)', 'Yes': 'rgb(0,255,0)'}
        fig = px.scatter(df, x="scantime", y="hosts", color = 'filtered', color_discrete_map=colorsIdx)
        fig.update_yaxes(categoryorder='category ascending')
        fig.update_traces(marker=dict(line=dict(width=1.1, color='DarkSlateGrey')), selector=dict(mode='markers'))
        fig.update_xaxes(dtick = 1)
        return fig

app = dash.Dash(__name__)
app.title = "Network Visualization"

#-----------------------------------------------------------------------------------------------------------
scanData1 = parseXML('testScan.xml')
scanData2 = parseXML('test2Scan.xml')
scanData3 = parseXML('test3Scan.xml')
scanData4 = parseXML('test1000scan')

#create a new full dictionary that conatins info from all the scans. 
portInfo = mergeDicts(scanData1, scanData2, scanData3, scanData4)

#compile the different scans into 1 dataframe (df) to be used by ploy.ly express (px)
df = compileGraphData(scanData1[0], scanData2[0], scanData3[0], scanData4[0])
#-----------------------------------------------------------------------------------------------------------
#define color index for graph color coding
colorsIdx = {'No': 'rgb(0,0,255)', 'Yes': 'rgb(0,255,0)'}

#create graph and style it
fig = px.scatter(df, x="scantime", y="hosts", color = 'filtered', color_discrete_map=colorsIdx)
fig.update_yaxes(categoryorder='category ascending') # order hosts
fig.update_traces(marker=dict(line=dict(width=1.1, color='DarkSlateGrey')), selector=dict(mode='markers'))
fig.update_xaxes(dtick = 1);

#screens
#-----------------------------------------------------------------------------------------------------------
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#-----------------------------------------------------------------------------------------------------------
index_page = html.Div([
    dcc.Link('Go to Upload', href='/Upload_Page'),
    html.Br(),
    dcc.Link('Go to Graph', href='/Graph_Page'),
])

#primary app screen, includes graph and port widget
#-----------------------------------------------------------------------------------------------------------
graph_page = html.Div(children=[
    html.H1(children='Network Visualization Prototype'),

    html.Div(children='''
        Version 0.1
    '''),

    dcc.Input(
        placeholder='Filter Hosts',
        type='text',
        value='',
        id='host_filter_input'
        ),

    html.Button(id='host_search_button_state', n_clicks=0, children='Filter'),

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
        id='port_host_input'
        ),


    html.Button(id='port_search_button_state', n_clicks=0, children='Search'),

    #define the port table
    html.Table(id='port_data', children =[
        html.Tr(),
        html.Th(children='Port Number'),
        html.Th(children='Service')
        ]
    )
])

#callbacks for screen functionality
@app.callback(
    Output(component_id='port_data', component_property='children'),
    Input('port_search_button_state', 'n_clicks'),
    State('port_host_input', 'value')       
)

# define what to do when the callback is activated 
def update_port_data(n_clicks, input_value):
    if input_value in df['hosts']:
        #return 'Ports: '  + str(portInfo[input_value])
        #print('Big info' + portInfo)
        return displayPortInfo(portInfo, input_value) 
    else:
        return 'Not a valid host'

@app.callback(
     Output(component_id='port_host_input', component_property='value'),
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

@app.callback(
    Output(component_id='main-graph', component_property='figure'), 
    Input('host_search_button_state', 'n_clicks'),
    #Input('main-graph', 'figure'),
    State('host_filter_input', 'value')       
)

#click functionality
def update_graph(n_clicks, input_value):
    #checks if input on app is in the dataframe of the graph, if yes, then apply filter, else load original
    if input_value != '':
        #add wildcards to value to 
        input_value = input_value + '*'
        #may want this block to check here, but i belive that it is effciently checked in findAndFlag
        '''for host in df['hosts']:
            if fnmatch.fnmatch(host, input_value):'''
        return findAndFlag(df, input_value)
    else:
        return fig

#Upload page
#-----------------------------------------------------------------------------------------------------------
upload_page = html.Div(children=[
    html.H2(children='Placeholder Upload Page')
    
])

#-------------------------------------------------------------------------------------------------------------    
# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Graph_Page':
        return graph_page
    elif pathname == '/Upload_Page':
        return upload_page
    else:
        return index_page
    # You could also return a 404 "URL not found" page here
'''
app.callback provides the functionality to the host search, it must be followed
    by the callback function declaration (in this case update_output_div).
    offical documentation can be found here: https://dash.plotly.com/basic-callbacks
        '''


if __name__ == '__main__':
    app.run_server(debug=True)
