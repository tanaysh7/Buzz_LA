import re
import sys
from tika import parser
from urllib.parse import urljoin

raw = parser.from_file(sys.argv[1])
content = (raw['content'])

date = re.findall(pattern='[a-zA-Z]{3,} [0-9]{1,2}, [0-9]{4,}', string = content)
body = re.split('[a-zA-Z]{3,} [0-9]{1,2}, [0-9]{4,}', content)[1:]

base_url = "http://www.calstatela.edu/"
title = []
url = []
description = []
for b in body:
    title.append(b.split("\n\n")[0].split(" (")[0])
    url.append(urljoin(base_url, b.split("\n\n")[0].split(" (")[1].strip(")")))
    desc = [x for x in b.split("\n\n")[1:] if x]
    description.append((" ").join(desc))

data = []
contents = [content for content in zip(title,date,url,description)]

for content in contents:
    innerdict = {}
    innerdict["title"] = content[0]
    innerdict["date"] = content[1]
    innerdict["url"] = content[2]
    innerdict["description"] = content[3]
    data.append(innerdict)

directory = "../PDFtoJSON/"
if not os.path.exists(directory):
    os.mkdir(directory)
filename = "CALSTATE.json"
filepath = os.path.join(directory, filename)  
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(outerdict, f, sort_keys=True)
    print("Saving " + filename + " to " + filepath)