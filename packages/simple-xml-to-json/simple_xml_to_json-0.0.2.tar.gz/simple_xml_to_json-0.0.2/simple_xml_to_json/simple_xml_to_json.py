from lxml import etree
import json

class Element:
    
    def __init__(self, element):
        self.element = element
        
    def toDict(self):
        
        data = {}       
        if self.element.attrib:
           data['@attributes'] = dict(self.element.attrib)
           
        text = self.element.text.strip() if self.element.text and self.element.text.strip() else None
        if text and not list(self.element):
            return { self.element.tag: text if not data else {**data, '#text': text}}
        
        for child in self.element:
            child_dict = Element(child).toDict()
            tag = child.tag 
            value = child_dict[tag]
            
            if tag in data:
                if not isinstance(data[tag], list):
                    data[tag] = [data[tag]]
                data[tag].append(value)
            else:
                data[tag] = value
                
        return {self.element.tag: data}
            
class XmlDocument:
    
    def __init__(self, xml="<emtpy />", filename=None):
        self.set(xml, filename)
        
    
    def set(self, xml=None, filename=None):
        if filename is not None:
            self.tree = etree.parse(filename)
            self.root = self.tree.getroot()
        else:
            self.root = etree.fromstring(xml)
            self.tree = etree.ElementTree(self.root)
            

    def dump(self):
        return etree.dump(self.root)
        
    
    def getXml(self):
        return etree.tostring(self.root)
    
    
    def nodes(self):
        return self.root.iter('*')
    
    
    def toDict(self):
        return Element(self.root).toDict()
    
    
    def toJson(self, indent=None):
        return json.dumps(self.toDict(), indent=indent)
    
    
if __name__ == '__main__':
    xml = "reed.xml"
    response = XmlDocument(filename=xml)
    with open("reed.json", "w") as file:
        file.write(response.toJson(indent=4))