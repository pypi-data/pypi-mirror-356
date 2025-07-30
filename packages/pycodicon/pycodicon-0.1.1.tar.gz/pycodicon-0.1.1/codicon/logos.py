from .common import Deity

class Logos(Deity):
	"""
	Logos is the law, the logic, the assertion that all must be correct.

	Domain:
	- Code correctness
	- Debugging clarity
	- Assertions and truth
	- Logical structure

	Essence:
	Logos thrives on reasoning and certainty. Any sacrifice must hold truth, or risk being
rejected with errors. Logos accepts only what can be logically validated.

	Sacrifice Method:
	Use `assert` statements, or checks that validate a condition. The offering is the subject
of truth, and the log is the proof.

	Example:
		Logos().sacrifice("potato")
		This will assert the value is truthy, or raise an error with its name.

	All bugs fear the gaze of Logos.
	"""
	def __init__(self):
		super().__init__("Logos", ["Logic", "Reasoning"], "Broken pseudocode")
	
	def sacrifice(self, offering):
		"""
		Assert an offering for Logos.
		"""
		assert offering, "Offering to Logos"
		
		super().sacrifice(offering)