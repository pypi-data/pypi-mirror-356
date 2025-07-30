import os
from .common import Deity


class Void(Deity):
	"""
	Void is the nothingness, the infinite silence, the terminal that returns no output.

	Domain:
	- Nullification
	- Suppressed output
	- Abandonment of feedback
	- Obliteration of side-effects

	Essence:
	Void is the entity beyond logs, prints, or returns. It receives offerings by
	swallowing them whole, making them vanish without trace.

	Sacrifice Method:
	Pass any string or data to Void. It will be printed to /dev/null (or equivalent),
	symbolically removing it from existence.

	Example:
		Void().sacrifice("potato")
		This will suppress the string entirely from standard output.

	To offer something to Void is to admit it was never needed in the first place.
	"""
	def __init__(self):
		super().__init__("Void", ["Nothingness", "Suppressed output"], "potato")
	
	def sacrifice(self, offering="potato"):
		"""
		Throw an offering into DEVNULL for Void.
		"""
		with open(os.devnull, "w") as devnull:
			print(offering, file=devnull)
		
		super().sacrifice(offering)