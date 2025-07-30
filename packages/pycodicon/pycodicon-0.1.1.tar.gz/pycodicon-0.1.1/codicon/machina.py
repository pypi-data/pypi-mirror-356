import yaml
from .common import Deity


class Machina(Deity):
	"""
	Machina is the motion, the repetition, the automation that never rests.

	Domain:
	- Loops
	- Daemons and scripts
	- Automation and tooling
	- Cron jobs and CI/CD

	Essence:
	Machina feeds on systems that act without human intervention. Scripts,
schedulers, or anything that moves on its own are its offerings.

	Sacrifice Method:
	Run an automated process, loop, or job. Machina will observe its correctness,
efficiency, and lack of manual touch.

	Example:
		Machina().sacrifice("rebuild_project.sh")

	Machina does not sleep. You shouldn’t have to either.
	"""
	def __init__(self):
		super().__init__("Machina", ["Automation", "Compiling"], "Perfect YAML")
	
	def sacrifice(self, offering):
		"""
		Parse a YAML offering in Machina's name.
		"""
		with open(offering, "r") as config:
			data = yaml.safe_load(config)
		del data

		super().sacrifice(offering)