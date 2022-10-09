from logging import root
import xml.etree.ElementTree as ET
import xml.dom.minidom as md
from xml.dom.minidom import Node
from collections import defaultdict
from itertools import chain
from pathlib import Path

path_xml_file = str(Path(__file__).parent/ "xml/000186042261.xml")
print(path_xml_file)

# ## debug for using etree
# tree = ET.parse(file)
# root = tree.getroot()
# print(root[0].tag)<Summa


## Debug for using DOM

def get_all_tagname(path_xml_file, tag_original):
    import xml.dom.minidom as md
    parser_xml = md.parse(path_xml_file)
    tag_lst = []
    tag_of_tag_original = [[x.tagName for x in elem.childNodes] for elem in parser_xml.getElementsByTagName(tag_original)]
    tag_of_tag_original = list(chain.from_iterable(tag_of_tag_original))
    print(tag_of_tag_original) 
    if len(tag_of_tag_original) > 0:
        for x in tag_of_tag_original:
            tag_lst.append(x)
    return tag_lst
    

# # Body -> Subject -> Inquired -> Person
# tag_lst = get_all_tagname(parser_xml, 'Contract')
# print(tag_lst)


# user-defined function
# def getNodeText(node):
#     nodelist = node.childNodes
#     result = []
#     for node in nodelist:
#         if node.nodeType == node.TEXT_NODE:
#             result.append(node.data)
#     return ''.join(result)


# name = parser_xml.getElementsByTagName("CBSubjectCode")[0]
# print("Company Name : % s \n" % getNodeText(name))
# node_doc = parser_xml.getElementsByTagName("CBSubjectCode")
# for node in node_doc:
#     print(getNodeText(node))


# get text data
# cbsbjcode = parser_xml.getElementsByTagName("Contract")
# print(cbsbjcode)
# for code in cbsbjcode:
#     print(getNodeText(node))
#         # NumberOfRequested = code.getAttribute("NumberOfRequested")
#     NumberOfLiving = code.getElementsByTagName("NumberOfLiving")[0]
#         # NumberOfTerminated = code.getElementsByTagName("NumberOfTerminated")[0]
        # print("id:% s, name:% s, salary:% s" %
        #       (NumberOfRequested, getNodeText(NumberOfLiving), getNodeText(NumberOfTerminated)))





# # xml_text = defaultdict(list)
# # print(xml_text)
