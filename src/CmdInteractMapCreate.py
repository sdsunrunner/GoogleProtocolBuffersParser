'''
Created on Mar 30, 2012

@author: songdu.greg
'''
import xml.etree.ElementTree as ET

def parserProto(fileName):    
    root = ET.parse(fileName).getroot();
    all_protos = root.findall('proto'); 
    
    commandInteractTypeStr = "package net\n{\n\t";
    commandInteractTypeStr += "public class CommandInteractType" + "\n\t{\n";
   
    commandInteractTypeStr += "\t\tpublic static const STARTAPP_COMMAND:String = \"STARTAPP_COMMAND\";\n";
    commandInteractTypeStr += "\t\tpublic static const STARTAPP_ASYNC_COMMAND:String = \"STARTAPP_ASYNC_COMMAND\";\n";
    commandInteractTypeStr += "\t\tpublic static const CONNECT_CALL_BACK_STATUS_ERROR_COMMAND:String = \"CONNECT_CALL_BACK_STATUS_ERROR_COMMAND\";\n";
    commandInteractTypeStr += "\t\tpublic static const CONNECT_TIME_OUT_COMMAND:String = \"CONNECT_TIME_OUT_COMMAND\";\n";
    commandInteractTypeStr += "\t\tpublic static const REQ_CONNECT_COMMAND:String = \"REQ_CONNECT_COMMAND\";\n";
    commandInteractTypeStr += "\t\tpublic static const RESPONSE_CONNECTED_SUCCESS_COMMAND:String = \"RESPONSE_CONNECTED_SUCCESS_COMMAND\";\n";
    commandInteractTypeStr += "\t\tpublic static const RESPONSE_CONNECTED_FAIL_COMMAND:String = \"RESPONSE_CONNECTED_FAIL_COMMAND\";\n";
    commandInteractTypeStr += "\t\tpublic static const CONNECT_SECURITY_ERROR_COMMAND:String = \"CONNECT_SECURITY_ERROR_COMMAND\";\n";
    
    commandInteractTypeStr += "//----------------------------------------------------------------------------------------\n";
    commandInteractTypeStr += "//CommandInteractType\n";
    commandInteractTypeStr += "//----------------------------------------------------------------------------------------\n";
    
    for proto in all_protos:
        if proto.attrib["interactType"] == "C2S":
            currentC2SCmdName = proto.attrib["name"];
            commandInteractTypeStr += "\t\tpublic static const C2S_" + proto.attrib["name"].upper() + "_REQ_COMMAND:String";
            commandInteractTypeStr +=" = \"" + "C2S_" + proto.attrib["name"].upper()+ "_REQ_COMMAND\";\n";
            
            findS2CCmd = 0;
            for proto in all_protos:
                if proto.attrib["name"] == currentC2SCmdName:
                    if proto.attrib["interactType"] == "S2C":
                        findS2CCmd=1;
            if  findS2CCmd == 0:
                    commandInteractTypeStr += "\t\tpublic static const S2C_" + currentC2SCmdName.upper() + "_ACK_COMMAND:String";
                    commandInteractTypeStr +=" = \"" + "S2C_" + currentC2SCmdName.upper()+ "_ACK_COMMAND\";\n";
                    
        elif proto.attrib["interactType"] == "S2C":
            commandInteractTypeStr += "\t\tpublic static const S2C_" + proto.attrib["name"].upper() + "_ACK_COMMAND:String";
            commandInteractTypeStr +=" = \"" + "S2C_" + proto.attrib["name"].upper()+ "_ACK_COMMAND\";\n";
   
    commandInteractTypeStr +="\n\t}";   
    commandInteractTypeStr +="\n}";  
    return commandInteractTypeStr;
        
if __name__ == '__main__':
    mapStr = parserProto('proto/proto.xml');
    open('as_out/CommandInteractType.as', 'w', encoding = "UTF-8").write(mapStr);
    print("commandInteractType map completed");
    