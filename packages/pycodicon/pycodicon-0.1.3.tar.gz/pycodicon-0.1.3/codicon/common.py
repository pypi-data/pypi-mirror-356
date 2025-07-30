from datetime import datetime


class Deity:
	"""
	Generic base class for a deity of the Codicon.
	"""
	def __init__(self, name, domain, sacrifice):
		self.name = name
		self.domain = domain
		self.preferred_sacrifice = sacrifice

	def sacrifice(self, offering):
		self.log(offering)
	
	def log(self, offering):
		with open("sacrifice.log", "a") as log:
			log.write(f"[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] Sacrificed '{offering}' to {self.name}.\n")
	
	def get_domain(self):
		return self.domain