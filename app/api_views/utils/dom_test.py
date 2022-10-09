import xml.dom.minidom as md
from pathlib import Path

path_xml_file = str(Path(__file__).parent/ "xml/000186042261.xml")
print(path_xml_file)

## Debug for using DOM
parser_xml = md.parse(path_xml_file)
tag = parser_xml.getElementsByTagName('CommonData')
for elem in tag:
    # print(elem.getAttribute('CBContractCode'))
    node  = elem.getElementsByTagName('CBContractCode')[0]
    print(node)
    nodelist = node.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    result = ''.join(result)
    break


print(result)



