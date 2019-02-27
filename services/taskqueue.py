import time
import json

from google.cloud import tasks_v2beta3
from google.api_core.exceptions import GoogleAPIError
from google.api_core.exceptions import RetryError

class CloudTasks:
	"""Parent Class for Cloud Tasks Interface"""
	def __init__(self, location, gae_project, local = False, client_secrets_path = 'client_secrets.json'):
		self.loc = location
		self.project = gae_project
		if not local:
			self.client = tasks_v2beta3.CloudTasksClient()
		else:
			self.client = tasks_v2beta3.CloudTasksClient.from_service_account_json(client_secrets_path)
		self.parent = self.client.location_path(self.project, self.loc)
	def getClient(self):
		return self.client
	def returnQueuesList(self):
		results = []
		for queue in self.client.list_queues(self.parent):
			results.append(queue)
			pass
		return results
	def createQueue(self, queue_name, service_name):
		queue = {
			'name': self.client.queue_path(self.project, self.loc, queue_name),
			'app_engine_http_queue': {
				'service': service_name
			}
		}
		return self.client.create_queue(self.parent, queue)
	def deleteQueue(self, queue_name):
		self.client.delete_queue(self.client.queue_path(self.project, self.loc, queue_name))
		return True

class CloudQueue(CloudTasks):
	"""Class for Cloud Tasks Queue operations"""
	def __init__(self, loc, pr, name, local = False, path = 'client_secrets.json'):
		super().__init__(loc, pr, local, path)
		self.queue_name = name
		self.queue_parent = self.client.queue_path(self.project, self.loc, self.queue_name)
		self.queue = self.client.get_queue(self.queue_parent)
		self.__queue_states = ['STATE_UNSPECIFIED', 'RUNNING', 'PAUSED' , 'DISABLED']
	def getQueueStatus(self):
		return self.__queue_states[self.queue.state]
	def getQueue(self):
		return self.queue
	def getQueueTasks(self, raw_return = False):
		if raw_return:
			return self.client.list_tasks(self.queue_parent)
		tasks = []
		for task in self.client.list_tasks(self.queue_parent):
			tasks.append({
				'name': task.name,
				'created': task.create_time,
				'dispatch_count': task.dispatch_count,
				'response_count': task.response_count,
				'last_attempt': task.last_attempt
			})
			pass
		return tasks
	def pauseQueue(self):
		return self.client.pause_queue(self.queue_parent)
	def resumeQueue(self):
		return self.client.resume_queue(self.queue_parent)
	def purgeQueue(self):
		return self.client.purge_queue(self.queue_parent)
	def addQueueTask(self, path, payload=None, name=None):
		if name is None:
			name = str(int(time.time()) * 1000000)
		name = 'projects/{0!s}/locations/{1!s}/queues/{2!s}/tasks/{3!s}'.format(self.project, self.loc, self.queue_name, name)
		task_body = {
			'name': name,
			'app_engine_http_request': {
				'http_method': 'POST',
				'relative_uri': path
			}
		}
		if payload is not None:
			payload = json.dumps(payload)
			converted_payload = payload.encode()
			task_body['app_engine_http_request']['body'] = converted_payload
		try:
			response = self.client.create_task(self.queue_parent, task_body)
			return {'scheduled': str(response.schedule_time).rstrip(), 'name': name}
		except GoogleAPIError as e:
			return {'error': 'GoogleAPIError', 'info': str(e), 'name': name}
		except RetryError as e:
			return {'error': 'RetryError', 'info': str(e), 'name': name}
