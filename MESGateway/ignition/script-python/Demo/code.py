def startBatch(bid):
	bqe = system.mes.batch.queue.getEntry(bid)
	system.mes.batch.queue.executeEntryCommand(bqe, system.mes.batch.queue.COMMAND_START())
	
	
def simulatePremix(baseTagPath):
	tagPaths = []
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient A/Command_Number')	#0
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient A/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient A/SP_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient A/PV_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient B/Command_Number')	#4
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient B/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient B/SP_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient B/PV_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient C/Command_Number')	#8
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient C/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient C/SP_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient C/PV_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient D/Command_Number')	#12
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient D/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient D/SP_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient D/PV_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Mix/Command_Number')				#16
	tagPaths.append(baseTagPath + 'Batch Phases/Mix/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Mix/SP_Duration')
	tagPaths.append(baseTagPath + 'Batch Phases/Mix/PV_Duration')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/Command_Number')	#20
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/SP_TransferAmount')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/PV_TransferAmount')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/Sync_Flag_Initialize')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/Sync_Confirm_Initialize')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/Sync_Flag_Complete')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/Sync_Confirm_Complete')

	tagPaths.append(baseTagPath + 'Batch Details/State_Number')
	
	tagValues = system.tag.readBlocking(tagPaths, 1000)
	batchState = tagValues[len(tagPaths) - 1].value 
	for ndx in [0, 4, 8, 12, 16, 20]:
		commandValue = tagValues[ndx].value
		stateValue = tagValues[ndx + 1].value
		spValue = tagValues[ndx + 2].value
		pvValue = tagValues[ndx + 3].value
		if(stateValue == None):
			system.tag.writeBlocking([tagPaths[ndx + 1]], [1], 1000) #Set state to Idle	
		if(commandValue == 1): #Start
			system.tag.writeBlocking([tagPaths[ndx + 1]], [2], 1000) #Set state to Running
			if(ndx < 20):  #Add Ingredients and Mix
				system.tag.writeBlocking([tagPaths[ndx + 3]], [0], 1000)
			if(ndx == 20):
				total = tagValues[3].value + tagValues[7].value + tagValues[11].value + tagValues[15].value
#				system.tag.writeBlocking([tagPaths[ndx + 4], tagPaths[ndx + 6]], [False, False], 1000)
				system.tag.writeBlocking([tagPaths[ndx + 2], tagPaths[ndx + 3]], [total, 0], 1000)		
#				system.util.getLogger('Demo').warn(str(total))
		elif(commandValue == 2): #Pause
			system.tag.writeBlocking([tagPaths[ndx + 1]], [7], 1000) #Set state to Paused
		elif(commandValue == 3): #Resume
			system.tag.writeBlocking([tagPaths[ndx + 1]], [2], 1000) #Set state to Running
		elif(commandValue == 4): #Hold
			system.tag.writeBlocking([tagPaths[ndx + 1]], [9], 1000) #Set state to Held
		elif(commandValue == 5): #Restart
			system.tag.writeBlocking([tagPaths[ndx + 1]], [2], 1000) #Set state to Running				
		elif(commandValue == 6): #Stop
			system.tag.writeBlocking([tagPaths[ndx + 1]], [11], 1000) #Set state to Stopped				
		if(commandValue == 7): # and batchState <> 2): #Reset
			system.tag.writeBlocking([tagPaths[ndx + 1]], [1], 1000) #Set state to Idle	
			if(ndx == 20):		
				for ndx in [0, 4, 8, 12, 16, 20]:
					system.tag.writeBlocking([tagPaths[ndx + 2], tagPaths[ndx + 3]], [0, 0], 1000)
				system.tag.writeBlocking([tagPaths[ndx + 4]], [False], 1000)
				system.tag.writeBlocking([tagPaths[ndx + 5]], [False], 1000)
				system.tag.writeBlocking([tagPaths[ndx + 6]], [False], 1000)
				system.tag.writeBlocking([tagPaths[ndx + 7]], [False], 1000)
		else:
			if(ndx < 20):  #Add Ingredients and Mix
				if(stateValue == 2):
					if(pvValue < spValue):
						system.tag.writeBlocking([tagPaths[ndx + 3]], [pvValue + 1], 1000)
						total = tagValues[3].value + tagValues[7].value + tagValues[11].value + tagValues[15].value  ###
						system.tag.writeBlocking([tagPaths[20 + 2], tagPaths[20 + 3]], [total, 0], 1000)
					else:
						system.tag.writeBlocking([tagPaths[ndx + 1]], [3], 1000)
#				elif(stateValue <> 3):
#					system.tag.writeBlocking([tagPaths[ndx + 3]], [0], 1000)
			else:
				#Handle the transfer out to the reactors
				if(stateValue == 2):
					initializeValue = tagValues[ndx + 5].value
					completeValue = tagValues[ndx + 7].value
					if(not initializeValue):
						total = tagValues[3].value + tagValues[7].value + tagValues[11].value + tagValues[15].value
						system.tag.writeBlocking([tagPaths[ndx + 4]], [True], 1000)		
						system.tag.writeBlocking([tagPaths[20 + 2], tagPaths[20 + 3]], [total, 0], 1000)  ### this is my add
					elif(not completeValue):
						if(pvValue < spValue):
							system.tag.writeBlocking([tagPaths[ndx + 3]], [pvValue + 1], 1000)
						else:
							system.tag.writeBlocking([tagPaths[ndx + 6]], [True], 1000)
					else:
						system.tag.writeBlocking([tagPaths[ndx + 1]], [3], 1000)							
				#elif(stateValue <> 3):

					
		
def simulateReactor(baseTagPath):
	logger = system.util.getLogger('myLogger')
	tagPaths = []
	tagPaths.append(baseTagPath + 'Batch Phases/Heat Reactor/Command_Number')			#0
	tagPaths.append(baseTagPath + 'Batch Phases/Heat Reactor/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Heat Reactor/SP_Temp')
	tagPaths.append(baseTagPath + 'Batch Phases/Heat Reactor/PV_Temp')
	tagPaths.append(baseTagPath + 'Batch Phases/Recirculate/Command_Number')			#4
	tagPaths.append(baseTagPath + 'Batch Phases/Recirculate/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Recirculate/SP_Duration')
	tagPaths.append(baseTagPath + 'Batch Phases/Recirculate/PV_Duration')
	tagPaths.append(baseTagPath + 'Batch Phases/Pump Out/Command_Number')				#8
	tagPaths.append(baseTagPath + 'Batch Phases/Pump Out/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Pump Out/SP_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Pump Out/PV_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/Command_Number')	#12
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/SP_TransferAmount')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/PV_TransferAmount')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/Sync_Flag_Initialize')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/Sync_Confirm_Initialize')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/Sync_Flag_Complete')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/Sync_Confirm_Complete')

	tagPaths.append(baseTagPath + 'Batch Details/State_Number')
	
	tagValues = system.tag.readBlocking(tagPaths, 1000)
	batchState = tagValues[len(tagPaths) - 1].value 
	for ndx in [0, 4, 8, 12]:
		commandValue = tagValues[ndx].value
		stateValue = tagValues[ndx + 1].value
		spValue = tagValues[ndx + 2].value
		pvValue = tagValues[ndx + 3].value

		if(ndx == 0 and spValue <> None):
			spValue = spValue - 50.0
		if(stateValue == None):
			system.tag.writeBlocking([tagPaths[ndx + 1]], [1], 1000) #Set state to Idle	
			system.tag.writeBlocking([tagPaths[ndx + 2], tagPaths[ndx + 3]], [0, 0], 1000)		

		if(commandValue == 1): #Start
			system.tag.writeBlocking([tagPaths[ndx + 1]], [2], 1000) #Set state to Running
			if(ndx == 8):
				PV_TransferAmount = tagValues[15].value
				system.tag.writeBlocking([tagPaths[ndx + 2]], [0], 1000)
				system.tag.writeBlocking([tagPaths[ndx + 3]], [PV_TransferAmount], 1000) 
		elif(commandValue == 2): #Pause
			system.tag.writeBlocking([tagPaths[ndx + 1]], [7], 1000) #Set state to Paused
		elif(commandValue == 3): #Resume
			system.tag.writeBlocking([tagPaths[ndx + 1]], [2], 1000) #Set state to Running
		elif(commandValue == 4): #Hold
			system.tag.writeBlocking([tagPaths[ndx + 1]], [9], 1000) #Set state to Held
		elif(commandValue == 5): #Restart
			system.tag.writeBlocking([tagPaths[ndx + 1]], [2], 1000) #Set state to Running				
		elif(commandValue == 6): #Stop
			system.tag.writeBlocking([tagPaths[ndx + 1]], [11], 1000) #Set state to Stopped				
		if(commandValue == 7): # and batchState <> 2): #Reset
			system.tag.writeBlocking([tagPaths[ndx + 1]], [1], 1000) #Set state to Idle
		else:
			if(ndx == 0):
				#Heat Reactor. Have the Pump Out reset the PV.
				if(stateValue == 2):
					if(pvValue < spValue):
						system.tag.writeBlocking([tagPaths[ndx + 3]], [pvValue + 1], 1000)
					else:
						system.tag.writeBlocking([tagPaths[ndx + 1]], [3], 1000)
				#elif(stateValue <> 3):
				#	system.tag.writeBlocking([tagPaths[ndx + 3]], [0], 1000)
				#set back to 0 after pump out complete
			elif(ndx == 4):
				#Recirculate
				if(stateValue == 2):
					if(pvValue < spValue):
						system.tag.writeBlocking([tagPaths[ndx + 3]], [pvValue + 1], 1000)
					else:
						system.tag.writeBlocking([tagPaths[ndx + 1]], [3], 1000)
				elif(stateValue <> 3):
					system.tag.writeBlocking([tagPaths[ndx + 3]], [0], 1000)
			elif(ndx == 8):
				#Handle the reactor pump out
				if(stateValue == 2):
					if(pvValue > 0):
						system.tag.writeBlocking([tagPaths[ndx + 3]], [pvValue - 1], 1000)
					else:
						system.tag.writeBlocking([tagPaths[ndx + 1]], [3], 1000)
						system.tag.writeBlocking([tagPaths[3]], [0], 1000)
			else:
				#Handle the transfer in from premix
				if(stateValue == 2):
					initializeValue = tagValues[ndx + 5].value
					completeValue = tagValues[ndx + 7].value
					if(not initializeValue):
						#system.tag.writeBlocking([tagPaths[10], tagPaths[11]], [0, 0], 1000)
						system.tag.writeBlocking([tagPaths[ndx + 4]], [True], 1000)
					elif(not completeValue):
						system.tag.writeBlocking([tagPaths[11]], [pvValue], 1000)
						if(pvValue >= spValue):
							system.tag.writeBlocking([tagPaths[ndx + 6]], [True], 1000)
					else:
						system.tag.writeBlocking([tagPaths[ndx + 1]], [3], 1000)
				elif(stateValue <> 3):
					#system.tag.writeBlocking([tagPaths[10], tagPaths[11]], [0, 0], 1000)
					#system.tag.writeBlocking([tagPaths[10]], [0], 1000)
					pass
		
def simulateAll():
	simulatePremix('[MES]Enterprise/Site/Area/Process Cell/Premix 1/')
	simulatePremix('[MES]Enterprise/Site/Area/Process Cell/Premix 2/')
	simulateReactor('[MES]Enterprise/Site/Area/Process Cell/Reactor 1/')
	simulateReactor('[MES]Enterprise/Site/Area/Process Cell/Reactor 2/')
		