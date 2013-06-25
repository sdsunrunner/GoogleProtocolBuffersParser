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
    cppCodeStr = "struct CMD_FLASH"; 
    cppCodeStr += "\n{"; 
    cppCodeStr += "\n\tenum"; 
    
    cppCodeStr += "\n\t{"; 
    
    startIndex = protoIndexMin;
    
    valueArr = [];
    for proto in all_protos:
        if proto.attrib["interactType"] == "C2S": 
            cppCodeStr += "\n\t\t" + "CMD_" + proto.attrib["name"].upper() +"_REQ"+" = " + str(startIndex) + ",";            
        elif proto.attrib["interactType"] == "S2C":
            cppCodeStr += "\n\t\t" + "CMD_" + proto.attrib["name"].upper() +"_ACK"+" = " + str(startIndex) + ",";
        valueArr.append(startIndex);
        cppCodeStr +="\t\t/*"+proto.attrib["desc"] + "*/";
        if startIndex <= protoIndexMax:
            startIndex = startIndex+1;
    cppCodeStr += "\n";        
    
    valueIndex=0;
    
    addValue = [];
    for proto in all_protos:
        if proto.attrib["interactType"] == "C2S":  
            cppCodeStr += "\n\t\t" + "CMD_" + proto.attrib["name"].upper()+"_REQ"+"_AA_ME" +" = " + str(valueArr[valueIndex] + protoIndexMax) +",";  
        elif proto.attrib["interactType"] == "S2C":
            cppCodeStr += "\n\t\t" + "CMD_" + proto.attrib["name"].upper()+"_ACK"+"_AA_ME" +" = " + str(valueArr[valueIndex] + protoIndexMax) +",";
        addValue.append((valueArr[valueIndex] + protoIndexMax));
        valueIndex = valueIndex+1;
       
    cppCodeStr += "\n"; 
   
    addValueIndex=0;
    for proto in all_protos:
        if proto.attrib["interactType"] == "C2S": 
            cppCodeStr += "\n\t\t" + "CMD_" + proto.attrib["name"].upper()+"_REQ"+"_ME_AA" +" = " + str(addValue[addValueIndex] + protoIndexMax)+",";  
        elif proto.attrib["interactType"] == "S2C": 
            cppCodeStr += "\n\t\t" + "CMD_" + proto.attrib["name"].upper()+"_ACK"+"_ME_AA" +" = " + str(addValue[addValueIndex] + protoIndexMax)+",";
        addValueIndex = addValueIndex+1;
    cppCodeStr +="\n\t};";  
  
    cppCodeStr +="\n};"; 
   
    open('proto_def/match_proto.h', 'w', encoding = "UTF-8").write(cppCodeStr);
        
if __name__ == '__main__':
    parserProto('proto/proto.xml');   
    print("cpp code completed");
   
    