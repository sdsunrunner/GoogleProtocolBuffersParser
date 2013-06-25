'''
Created on Feb 7, 2012

@author: songdu.greg
'''
import xml.etree.ElementTree as ET

def load_xml_file(fileName):
    
    
    root = ET.parse(fileName).getroot()
    all_enums = root.findall('enum')
    
    for enum in all_enums: 
        enumStr = "package net.enum\n{\n\t"
        enumStr += "public class " + enum.attrib["name"]
        enumStr += "\n\t{"
        enumMembers = enum.findall('member')
        for member in enumMembers: 
            enumStr += "\n\t\t" + "public static const "+ member.attrib["name"] +":Number"+ " = " + member.attrib["value"] + ";"
        enumStr += "\n\t}"
        enumStr += "\n}"
        open("as_out/" + enum.attrib["name"] + '.as', 'w', encoding = "utf-8").write(enumStr);
            
if __name__ == '__main__':
    load_xml_file('proto/enum.xml')
    print("enum as code complete");