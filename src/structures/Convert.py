import json
import pandas as pd

from bs4 import BeautifulSoup

class Convert:
	def __init__(self, content, indent=None):
		self.content = content
		self.indent = indent

	def convert_json_to_dataframe(self):
		if self.content.endswith(".json"):
			self.content = open(self.content, "r").read()

		df = pd.read_json(self.content)

		return df