from google.cloud import datastore

class DataStoreObject:
	""" Прототип для работы с сущностями DataStore одного типа и пространства имен """
	def __init__(self, kind, namespace, local = False, client_secrets_path = 'client_secrets.json'):
		self.kind = kind
		self.namespace = namespace
		self.client = datastore.Client() if not local else datastore.Client.from_service_account_json(client_secrets_path)
	def getClient(self):
		return self.client
	def listEntities(self):
		query = self.client.query(kind = self.kind, namespace = self.namespace)
		return [e.key.id_or_name for e in query.fetch()]
	def queryEntities(self, property, value, compare = '='):
		query = self.client.query(kind = self.kind, namespace = self.namespace)
		query.add_filter(property, compare, value)
		return [e for e in query.fetch()]
	def getEntityByName(self, name):
		entity_key = self.client.key(self.kind, name, namespace = self.namespace)
		return self.client.get(key = entity_key)
	def setEntityValue(self, name, value):
		entity_key = self.client.key(self.kind, name, namespace = self.namespace)
		entity_value = datastore.Entity(key = entity_key)
		entity_value.update(value)
		self.client.put(entity_value)
		return self.client.get(key = entity_key)
