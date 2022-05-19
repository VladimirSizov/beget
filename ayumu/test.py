import re

text = '[1,2,3]'
parse = re.findall('([-+]?\d+)', text)
print(parse)
for i in parse:
	print(i)