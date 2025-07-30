import rel
from catmail.util import Loggy
from catmail.config import config

class Scanner(Loggy):
	def __init__(self, reader):
		self.scanners = {}
		self.reader = reader
		self.ticker = rel.timeout(None, self.tick)

	def criteria(self, sender=None, subject=None, unseen=True):
		crits = []
		if sender:
			crits.append('FROM "%s"'%(sender,))
		if subject:
			crits.append('SUBJECT "%s"'%(subject,))
		if unseen:
			crits.append("UNSEEN")
		return "(%s)"%(" ".join(crits),)

	def scan(self, sender=None, subject=None, unseen=True, count=1, mailbox="inbox"):
		return self.check(self.criteria(sender, subject, unseen), count, mailbox)

	def check(self, crit="UNSEEN", count=1, mailbox="inbox"):
		self.log("scanning", mailbox, "for", crit)
		return self.reader.inbox(count, crit, mailbox=mailbox)

	def tick(self):
		founds = []
		for crit, scanner in self.scanners.items():
			msgs = self.check(crit, scanner["count"], scanner["mailbox"])
			if msgs:
				for msg in msgs:
					scanner["cb"](msg)
				founds.append(crit)
		for found in founds:
			del self.scanners[found]
		return self.scanners # Falsy when empty

	def on(self, scanopts, cb=None, count=1, mailbox="inbox"):
		if not self.scanners:
			self.log("starting scanner")
			self.ticker.add(config.scantick)
		crit = self.criteria(**scanopts)
		self.log("watching for", crit)
		self.scanners[crit] = {
			"count": count,
			"mailbox": mailbox,
			"cb": cb or self.reader.show
		}