def initPremix(baseTagPath):
	tagPaths = []
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient A/Command_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient A/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient A/SP_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient A/PV_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient B/Command_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient B/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient B/SP_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient B/PV_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient C/Command_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient C/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient C/SP_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient C/PV_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient D/Command_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient D/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient D/SP_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Add Ingredient D/PV_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Mix/Command_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Mix/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Mix/SP_Duration')
	tagPaths.append(baseTagPath + 'Batch Phases/Mix/PV_Duration')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/Command_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/SP_TransferAmount')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/PV_TransferAmount')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/Sync_Flag_Initialize')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/Sync_Confirm_Initialize')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/Sync_Flag_Complete')
	tagPaths.append(baseTagPath + 'Batch Phases/Premix Transfer Out/Sync_Confirm_Complete')
	
	for ndx in [0, 4, 8, 12, 16, 20]:
		system.tag.writeBlocking([tagPaths[ndx + 1]], [1], 1000) #Set state to Idle	
		system.tag.writeBlocking([tagPaths[ndx + 2]], [0], 1000) 
		system.tag.writeBlocking([tagPaths[ndx + 3]], [0], 1000) 
		if(ndx == 20):		
			system.tag.writeBlocking([tagPaths[ndx + 4]], [False], 1000)
			system.tag.writeBlocking([tagPaths[ndx + 6]], [False], 1000)


def initReactor(baseTagPath):
	tagPaths = []
	tagPaths.append(baseTagPath + 'Batch Phases/Heat Reactor/Command_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Heat Reactor/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Heat Reactor/SP_Temp')
	tagPaths.append(baseTagPath + 'Batch Phases/Heat Reactor/PV_Temp')
	tagPaths.append(baseTagPath + 'Batch Phases/Recirculate/Command_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Recirculate/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Recirculate/SP_Duration')
	tagPaths.append(baseTagPath + 'Batch Phases/Recirculate/PV_Duration')
	tagPaths.append(baseTagPath + 'Batch Phases/Pump Out/Command_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Pump Out/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Pump Out/SP_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Pump Out/PV_Amount')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/Command_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/State_Number')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/SP_TransferAmount')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/PV_TransferAmount')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/Sync_Flag_Initialize')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/Sync_Confirm_Initialize')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/Sync_Flag_Complete')
	tagPaths.append(baseTagPath + 'Batch Phases/Reactor Transfer In/Sync_Confirm_Complete')
	
	for ndx in [0, 4, 8, 12]:
		system.tag.writeBlocking([tagPaths[ndx + 1]], [1], 1000) #Set state to Idle	
		system.tag.writeBlocking([tagPaths[ndx + 3]], [0], 1000) #Set state to Idle
		if(ndx == 12):		
			system.tag.writeBlocking([tagPaths[ndx + 4]], [False], 1000)
			system.tag.writeBlocking([tagPaths[ndx + 6]], [False], 1000)	
			
def initializeDemoTags():	
	initPremix('[MES]Enterprise/Site/Area/Process Cell/Premix 1/')
	initPremix('[MES]Enterprise/Site/Area/Process Cell/Premix 2/')
	initReactor('[MES]Enterprise/Site/Area/Process Cell/Reactor 1/')
	initReactor('[MES]Enterprise/Site/Area/Process Cell/Reactor 2/')
	