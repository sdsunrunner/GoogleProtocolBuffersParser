'''
Created on Mar 30, 2012

@author: songdu.greg
'''
import xml.etree.ElementTree as ET

def parserProto(fileName):    
    root = ET.parse(fileName).getroot();
    section = root.find('proto_section'); 
     
    protoIndexMin = int(section.attrib["min_proto_index"]);
    protoIndexMax = int(section.attrib["max_proto_index"]);
    
    all_protos = root.findall('proto');    
    
    
    msgTypeStr = "";
       
    cmdMapStr = "package net"; 
    cmdMapStr += "\n{"; 
    cmdMapStr += "\n\timport protoMap.ProtocolMap;"; 
       
    cmdMapStr += "\n\tpublic class ProtoIndexMap extends ProtocolMap";    
    cmdMapStr += "\n\t{"; 
    cmdMapStr += "\n\t\tprivate static var _instance:ProtoIndexMap = null;"
    cmdMapStr += "\n\t\tpublic function ProtoIndexMap()";
    cmdMapStr += "\n\t\t{"; 
    cmdMapStr += "\n\t\t\tsuper();";
    cmdMapStr += "\n\t\t\tsetMinIndex("+str(protoIndexMin)+");";
    cmdMapStr += "\n\t\t\tsetMaxIndex("+str(protoIndexMax)+");";
    cmdMapStr += "\n";
    startIndex = protoIndexMin;
    for proto in all_protos:                   
        cmdMapStr += "\n";
        if proto.attrib["interactType"] == "C2S":
            cmdMapStr += "\t\t\taddItem(" + str(startIndex) +",\"" + proto.attrib["name"] + "\");";
        elif proto.attrib["interactType"] == "S2C":
            cmdMapStr += "\t\t\taddItem(" + str(startIndex) +",\"" + proto.attrib["name"] + "Ack\");";
            msgTypeStr += "_msgFacade.addSocketMsg(" + str(startIndex)+ ", " + proto.attrib["name"] + "Ack);\n"
            
        if startIndex <= protoIndexMax:
            startIndex = startIndex+1;
    cmdMapStr +="\n\t\t}"; 
    cmdMapStr +="\n"; 
    cmdMapStr +="\n\t\tpublic static function get instance():ProtoIndexMap";
    cmdMapStr +="\n\t\t{";
    cmdMapStr +="\n\t\t\treturn _instance ||= new ProtoIndexMap();";
    cmdMapStr +="\n\t\t}";
    
    cmdMapStr +="\n\t}";   
    cmdMapStr +="\n}"; 
    
    open('as_out/ProtoIndexMap.as', 'w', encoding = "UTF-8").write(cmdMapStr);
    open('as_out/msgTypeStr.as', 'w', encoding = "UTF-8").write(msgTypeStr);
        
if __name__ == '__main__':
    parserProto('proto/proto.xml');   
    print("CMD id map completed");
   
    