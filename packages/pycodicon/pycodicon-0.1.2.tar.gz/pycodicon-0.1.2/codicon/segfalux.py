import ctypes
import time
from datetime import datetime
from .common import Deity


class Segfalux(Deity):
	"""
	Segfalux is the glitch, the segfault, the crash that reminds us we know nothing.

	Domain:
	- Memory corruption
	- Crashes and faults
	- Undefined behavior
	- Core dumps

	Essence:
	Segfalux accepts the most dangerous gifts: memory, especially misused. They revel
in the crash, the glitch, the system halt.

	Sacrifice Method:
	Offer units of RAM or memory manipulation. True devotion is shown through reckless
operations like null dereference.

	Example:
		Segfalux().sacrifice("512MB")
		May log and simulate corrupt allocation.

	Note: Segfalux does not guarantee survival.
	"""
	def __init__(self):
		super().__init__("Segfalux", ["Segfaults", "Crashes"], "RAM")
	
	def parse_size(self, value):
		value = value.lower().strip()
		multipliers = {
			"b": 1,
			"kb": 1024,
			"mb": 1024**2,
			"gb": 1024**3,
		}

		for unit in sorted(multipliers.keys(), key=len, reverse=True):
			if value.endswith(unit):
				number_part = value[:-len(unit)].strip()
				try:
					number = int(number_part)
				except ValueError:
					raise ValueError(f"Invalid size number: '{number_part}' in '{value}'")
				return number * multipliers[unit]

		try:
			return int(value)
		except ValueError:
			raise ValueError(f"Invalid size value: '{value}'")

	def sacrifice(self, offering):
		"""
		Sacrifice RAM to appease Segfalux.
		"""
		size = self.parse_size(offering)
		ptr = ctypes.create_string_buffer(size)
		for i in range(0, size, 4096):
			ptr[i] = b'\xAA'[0]
		del ptr
		super().sacrifice(offering)

	def log(self, offering):
		with open("sacrifice.log", "a") as log:
			log.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Sacrificed {offering} of RAM to {self.name}.\n")