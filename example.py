from services import DataStoreObject, CloudTasks, CloudQueue

if __name__ == '__main__':
	ds = DataStoreObject('Configurations', 'Worker', local = True)
	ct = CloudTasks('europe-west3', 'trying-artics-pipeline', local = True)
	
	# List Entities in DataStore namespace
	names_collection_in_ds = ds.listEntities()
	print(names_collection_in_ds)

	# Get Entity by its name
	entity_from_ds = ds.getEntityByName(names_collection_in_ds[0])
	print(entity_from_ds)
	print(entity_from_ds['IMPORT_ROWS_COUNT'])

	# Update Entity and print updated value
	entity_from_ds['IMPORT_ROWS_COUNT'] = 10000
	updated_entity = ds.setEntityValue(names_collection_in_ds[0], entity_from_ds)
	print(updated_entity['IMPORT_ROWS_COUNT'])

	# List Queues
	queues_in_appengine = ct.returnQueuesList()
	print(queues_in_appengine[0])

	# Get Queue Status
	queue_path_name = queues_in_appengine[0].name
	simplified_queue_name = queue_path_name.split('/')[-1]
	tq = CloudQueue('europe-west3', 'trying-artics-pipeline', simplified_queue_name, local = True)
	print(tq.getQueueStatus())

	# Get Queue Object and inspect it

	selected_queue = tq.getQueue()
	print(selected_queue.state)
