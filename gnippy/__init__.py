# -*- coding: utf-8 -*-
# gnippy - GNIP for Python

__title__ = 'gnippy'
__version__ = '0.1.2'
__author__ = 'Abhinav Ajgaonkar'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2012 Abhinav Ajgaonkar'

import threading
import requests

class PowerTrackClient():
	""" 
		PowerTrackClient allows you to connect to the GNIP
		power track stream and fetch data
	"""
	def __init__(self, url, auth, callback):
		self.url = url
		self.auth = auth
		self.callback = callback
	
	def connect(self):
		self.worker = Worker(self.url, self.auth, self.callback)
		self.worker.setDaemon(True)
		self.worker.start()
	
	def disconnect(self):
		self.worker.stop()
		self.worker.join()
	

class Worker(threading.Thread):
	""" Background worker to fetch data without blocking """
	def __init__(self, url, auth, callback):
		super(Worker, self).__init__()
		self.url = url
		self.auth = auth
		self.on_data = callback
		self._stop = threading.Event()
	
	def stop(self):
		self._stop.set()
		
	def stopped(self):
		return self._stop.isSet()
	
	def run(self):
		r = requests.get(self.url, auth=self.auth, stream=True)
		for line in r.iter_lines():
			if self.stopped():
				break
			elif line:
				self.on_data(line)
