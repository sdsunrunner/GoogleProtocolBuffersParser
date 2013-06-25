'''
Created on Mar 30, 2012

@author: songdu.greg
'''
import os
import shutil
import xml.etree.ElementTree as ET

def parserProto(fileName, type_str):    
    root = ET.parse(fileName).getroot();
    all_protos = root.findall('proto'); 
    protocoMessageStr = "";    
    for proto in all_protos:
        if proto.attrib["interactType"]== type_str:
            protocoMessageStr += "\n";
            if type_str == "C2S":
                    protocoMessageStr += "message " + proto.attrib["name"] + "Req{";
            elif type_str == "S2C":
                protocoMessageStr += "message " + proto.attrib["name"] + "Ack{";
                
            params = proto.findall('param');
            value = 0;
            for param in params:
                value +=1;
                typename = parserType(param.attrib["type"]);
                protocoMessageStr +="\n\t";
                protocoMessageStr += param.attrib["need_type"] +" "+ typename + " "+param.attrib["name"] + " = " +str(value)  + ";";
                protocoMessageStr += "//" + param.attrib["desc"];
            protocoMessageStr+="\n}";
          
    return protocoMessageStr;

def parserStructure(fileName):    
    root = ET.parse(fileName).getroot();
    all_structs = root.findall('struct'); 
    structMessageStr = "";    
    for struct in all_structs: 
        structMessageStr += "/****************"+struct.attrib["name"]+"**********************/"       
        structMessageStr += "\n";
        structMessageStr += "message " + struct.attrib["name"] + "{";
        members = struct.findall('member');
        value = 1;
        for member in members: 
            typename = parserType(member.attrib["type"]);
            structMessageStr += "\n\t";
            structMessageStr += member.attrib["need_type"]+" " + typename + " " + member.attrib["name"] + " = " + str(value) + ";";
            structMessageStr += "//" + member.attrib["desc"];
            value +=1;   
                
        structMessageStr +="\n}\n\n";   
    return structMessageStr;

def parserType(typeName):
    result = typeName;
    if result == "int":
        result = "int32";
    elif result == "int16":
        result = "int32";
    elif result == "String":
        result = "string";  
   
    return result;

def createCatalog():
#   google buf
    if os.path.exists("proto_def"):
        shutil.rmtree("proto_def")
    
    if os.path.exists("as_out"):
        shutil.rmtree("as_out")
        
    os.makedirs("proto_def");
   
    os.makedirs("as_out");
    
    

def creatGoogleBuf():
    structure_def = parserStructure('proto/item_structure.xml');       
   
    req_def = parserProto('proto/proto.xml', "C2S");
    ack_def = parserProto('proto/proto.xml', "S2C");

    proto_def_str = "package net.protobuf;\n";
    proto_def_str += structure_def;
    proto_def_str += req_def;
    proto_def_str += ack_def;
    
    open('proto_def/message.proto', 'w', encoding = "UTF-8").write(proto_def_str);
    
    print("proto def conplete");
    os.system('create_code.bat');
        
if __name__ == '__main__':
    createCatalog();
    os.system('CmdIdMapCreate.py');
    os.system('CmdInteractMapCreate.py');
    os.system('ProtoEnumParser.py');
    os.system('CppProto.py');
 
    creatGoogleBuf();
    
    
   
   
    