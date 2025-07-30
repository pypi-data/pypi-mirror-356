import time
import os
from .common import Deity


class Archivus(Deity):
	"""
	Archivus is the keeper of change, the librarian of all that ever was.

	Domain:
	- Version control
	- Logs and history
	- Backups
	- Immutable record

	Essence:
	Archivus receives offerings through permanent storage — preferably committed, documented,
and pushed to the global memory.

	Sacrifice Method:
	Create or modify a file, and commit it with a sacred message. Archivus values descriptive
logs and timestamps.

	Example:
		Archivus().sacrifice("Added sacred logs")
		This will write to disk or call a git commit.

	To forget is mortal; to record is divine.
	"""
	def __init__(self):
		super().__init__("Archivus", ["Old code", "Git commits"], "Copy of FINAL main (MASTER COPY) v3 (2).zip")
	
	def sacrifice(self, offering="Copy of FINAL main (MASTER COPY) v3 (2).zip"):
		"""
		Record a file to Archivus's archives, entombing it forever in history.
		"""
		os.makedirs("archivus_sacrifices", exist_ok=True)
		with open(os.path.join("archivus_sacrifices", "offering_" + str(time.time())), "w") as sacrifice:
			if os.path.isfile(offering):
				with open(offering, "r") as f:
					sacrifice.write(f.read())
			else:
				sacrifice.write(offering)
		super().sacrifice(offering)