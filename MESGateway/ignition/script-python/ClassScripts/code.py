def createLot(lotNo, materialName, quantity, UOM, status):
	timeNow = system.date.toMillis(system.date.now())
	strTimeNow = str(timeNow)
	userId = strTimeNow
	name = 'Receiving' 
	beginDateTime = timeNow 
	endDateTime = timeNow 
	equipmentPath = 'Enterprise\\Site\\Area\\Warehouse\\RM Storage' 
	matOut = system.mes.trace.configureMaterial(
		userid = 'matOut_'+strTimeNow, 
		name = 'matOut', 
		lotNo = lotNo, 
		materialName = materialName, 
		quantity = quantity, 
		UOM = UOM, 
		status = status, 
		equipmentPath = equipmentPath, 
		autoCreateLot = True)
	system.mes.trace.recordOperation(
		userId=userId, 
		name=name, 
		beginDateTime=beginDateTime, 
		endDateTime=endDateTime, 
		equipmentPath = equipmentPath, 
		materialOut=[matOut])
	return strTimeNow

def mixOperation(LotID_A, matName_A,qty_A,LotID_B,matName_B,qty_B,LotID_FG,matName_FG,qty_FG,selectedUnit):
	rmEquipmentPath = 'Enterprise\\Site\\Area\\Warehouse\\RM Storage'
	fgEquipmentPath = 'Enterprise\\Site\\Area\\Warehouse\\FG Storage'
	
	opEquipmentPath ='Enterprise\\Site\\Area\\Process Cell\\'+selectedUnit
	
	timeNow = system.date.toMillis(system.date.now())
	strTimeNow = str(timeNow)
	
	matIn_A = system.mes.trace.configureMaterial(
		userid = 'matIn_A', 
		name = 'matIn_A', 
		lotNo = LotID_A, 
		materialName = matName_A, 
		quantity = qty_A, 
		UOM = 'Kg', 
		status = 'Complete', 
		equipmentPath = rmEquipmentPath, 
		autoCreateLot = False)
	matIn_B = system.mes.trace.configureMaterial(
		userid = 'matIn_B', 
		name = 'matIn_B', 
		lotNo = LotID_B, 
		materialName = matName_B, 
		quantity = qty_B, 
		UOM = 'Kg', 
		status = 'Complete', 
		equipmentPath = rmEquipmentPath, 
		autoCreateLot = False)
	matOut = system.mes.trace.configureMaterial(
		userid = 'matOut', 
		name = 'matOut', 
		lotNo = LotID_FG, 
		materialName = matName_FG, 
		quantity = qty_FG, 
		UOM = 'Kg', 
		status = 'Complete', 
		equipmentPath = fgEquipmentPath, 
		autoCreateLot = True)
	system.mes.trace.recordOperation(
		userId=strTimeNow, 
		name=strTimeNow,  
		equipmentPath = opEquipmentPath,
		materialIn=[matIn_A,matIn_B],
		materialOut=[matOut])
	return strTimeNow

def modifyOperation_matOut(newQty_FG,operationUserId):
	matOut = system.mes.trace.configureMaterial(
		userid = 'matOut', 
		quantity = newQty_FG)
	system.mes.trace.modifyOperation(
		userId=operationUserId, 
		materialOut=[matOut],
		endDateTime = system.date.now() )

def getTraceGraph(lotNumber, lotSequenceNumber):
	try:
		result = system.mes.trace.getTraceabilityData(lotNumber, lotSequenceNumber)
	except:
		return 'No data for that lot / sequence'
	respSegUUID = result[0]['segmentUUID']
	
	markup = ''
	if len(respSegUUID) > 0:
		seg = system.mes.loadMESObject(respSegUUID)
		
		print '## ' + seg.getName()
		print '- Started: ' +str(seg.getPropertyValue('BeginDateTime'))
		print '- Ended: ' +str(seg.getPropertyValue('EndDateTime'))
		print ' '
				
		operationUUID = seg.getPropertyValue('OperationsResponseRefUUID')
		opResponse = system.mes.loadMESObject(operationUUID)
		
		#Get the MES object link of where the operation is running
		eqLink = opResponse.getEquipmentLink()
		
		print '### Processing Equipment'
		print '- Type: '+ str(eqLink.getMESObjectType())
		print '- Name: '+ eqLink.getName()
		
		complexProps = seg.getComplexPropertyCount('ResponseMaterial')
		
		props = {}
		uiList = []
		for i in range(complexProps):
			prop = seg.getComplexProperty('ResponseMaterial',i)
			#material prop name
			propName = prop.getName()
			if prop.hasSegmentRefUUID():
				#lot number
				lotName = prop.getMaterialLot().getName()
				#material def name
				matName = prop.getMaterialRef().getName()
				#location
				location = prop.getEquipmentRef().getName()
				#quantity
				quantity = prop.getQuantity()
				#begintime
				begin = prop.getBeginDateTime()
				#end time
				end = prop.getEndDateTime()
				#use
				use = prop.getUse()
				
				lotSequence = prop.getLotRefSequence()
				eqPath = prop.getEquipmentRef().getMESObject().getEquipmentPath()
				
				customProps = []
				lot = system.mes.loadMaterialLot(lotName, lotSequence, eqPath, False)
				
				for cp in lot.getAllCustomProperties():
					customProps.append(cp.getName() + ':' + str(cp.getValue()))
				
				#Sublots
				sublots = []
				for lot in lot.getChildCollection():
					sublots.append(system.mes.getMESObjectLink(lot).getName())
				
				finalProp = {use:
					{
						'propName' : propName,
						'lotName' : lotName,	
						'matName' : matName,
						'location' : location,
						'quantity' : quantity,
						'begin' : begin,
						'end': end,
						'customProps': customProps,
						'sublots':sublots
					}
				}
		
			else:
				finalProp = {'unused':{'propName':propName}}
				
			#update relevant material
			if props.has_key(finalProp.keys()[0]):
				props[finalProp.keys()[0]].append(finalProp[finalProp.keys()[0]])
			#create new list of material
			else:
				props.update({finalProp.keys()[0]:[finalProp[finalProp.keys()[0]]]})
		
		useOrder = ['In','Out','Consumable','By-Product']
		for use in useOrder:
			first = True
			for key, values in props.items():
				if key == use:
					for matProp in values:
						if first == True:
							print ' '
							print '## MATERIAL - ' + key.upper()
						print '### ' + matProp['propName'] + ':'
						print '- Lot No: ' + matProp['lotName']
						print '- Material:' + matProp['matName']
						print '- Location:' + matProp['location']
						print '- Quantity:' + str(matProp['quantity'])
						print '- Begin Date Time:' + str(matProp['begin'])
						print '- End Date Time:' + str(matProp['end'])
						#custom properties
						if matProp['customProps']:
							for cp in matProp['customProps']:
								print '- ' + cp.split(':')[0] + ': ' + cp.split(':')[1]
						first = False
						#sublots
						if matProp['sublots']:
							for sublot in matProp['sublots']:
								print '- '+ sublot

if 1==2:
	createLot(lotNo='AA3', materialName='Ingredient B2', quantity=5000, UOM='Kg', status='Complete')
if 1==2:
	LotID_A = 'AA1'
	matName_A = 'Ingredient A1'
	qty_A = 2.1
	LotID_B = 'AA3'
	matName_B = 'Ingredient B2'
	qty_B = 1.3
	LotID_FG = 'Mix 4'
	matName_FG = 'Mix Product'
	qty_FG = 3.4
	selectedUnit = 'Premix 2'
	mixOperation(LotID_A, matName_A,qty_A,LotID_B,matName_B,qty_B,LotID_FG,matName_FG,qty_FG,selectedUnit)
if 1==2:
	newQty_FG = 3.0
	operationUserId = '1741880048861'
	modifyOperation_matOut(newQty_FG,operationUserId)
if 1==2:
	import pprint
	pprint.pprint(system.mes.trace.getInventory(lotNumber='Mix 4')) 
if 1==2:
	getTraceGraph('Mix 4', lotSequenceNumber=1)