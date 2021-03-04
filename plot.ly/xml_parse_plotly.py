import xml.etree.ElementTree as ET

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

	return data

print(parseXML('/home/user/Desktop/Project/test2Scan.xml'))