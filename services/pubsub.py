from google.cloud import pubsub
import json
import os
import logging


class PubSub:
	def __init__(self, topic=None, project=None):
		self._project = project if project is not None else 'trying-artics-pipeline'
		self._topic = topic if topic is not None else 'notification_email_intraday'

		self._AT_GCP = os.environ.get('AT_GCP', False)

	def _initPublisher(self):
		if self._AT_GCP is True:
			publish_client = pubsub.PublisherClient()
		else:
			publish_client = pubsub.PublisherClient.from_service_account_json('../client_secrets.json')
		return publish_client

	def _initSubscriber(self):
		if self._AT_GCP is True:
			subscriber = pubsub.SubscriberClient()
		else:
			subscriber = pubsub.SubscriberClient.from_service_account_json('client_secrets.json')
		return subscriber

	def push(self, data):
		"""
		:param data: to put smth into pubSub, supporting dict(will dumps)
		:return: status (True/False)
		"""
		client = self._initPublisher()
		topic = client.topic_path(self._project, self._topic)
		prepared_data = json.dumps(data).encode()
		try:
			client.publish(topic, prepared_data)
		except Exception as e:
			logging.warning('pubSub: got error when publish data: %s' % e)
			return False
		return True

	def pull(self, max_messages=100, auto_acknowledge=True):
		"""
		:param max_messages: max_messages to recieve from pubSub
		:param auto_acknowledge: True/False
			remove this messages from pubSub if this True
		:return: (messages, ack_ids)
			messages: array of decoded source messages
			ack_ids: array of ack_ids
		"""
		client = self._initSubscriber()
		topic = client.subscription_path(self._project, self._topic)

		response = client.pull(topic, max_messages)

		messages = [i.message.data.decode() for i in response.received_messages]
		ack_ids = [i.ack_id for i in response.received_messages]

		if auto_acknowledge is True:
			client.acknowledge(topic, ack_ids)

		return messages, ack_ids

	def acknowledge(self, ack_ids):
		"""
		:param ack_ids: array of ids from pull
		:return: status (True/False)
		"""
		client = self._initSubscriber()
		topic = client.subscription_path(self._project, self._topic)

		try:
			client.acknowledge(topic, ack_ids)
		except Exception as e:
			logging.warning('pubSub: got error when acknowledge data: %s' % e)
			return False

		return True
