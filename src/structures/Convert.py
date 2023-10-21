import json

from bs4 import BeautifulSoup

class Convert:
	def __init__(self, content, indent=None):
		self.content = content
		self.indent = indent

	def convert_html_to_json(self):
		soup = BeautifulSoup(self.content, "html.parser")
		rows = soup.find_all("tr")

		headers = {}
		thead = soup.find("thead")
		if thead:
			thead = soup.find_all("th")
			for i in range(len(thead)):
				headers[i] = thead[i].text.strip().lower()
		data = []
		for row in rows:
			cells = row.find_all("td")
			if thead:
				items = {}
				if len(cells) > 0:
					for index in headers:
						if "TÉCNICO" in cells[index].text:
							data.append(items)
							items = {}
						print(headers)
						if headers[index] == "componente curricular":
							items[headers[index]] = cells[index].text.strip()
						else:
							items[headers[index]] = cells[index].text
			else:
				items = []
				for index in cells:
					if "TÉCNICO" in index.text:
						data.append(items)
						items = []
					items.append(index.text.strip())
				if items:
					data.append(items)
		return json.dumps(data, indent=self.indent)

	def remove_empty_array(self, array):
		return [item for item in array if item]