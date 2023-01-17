from Files import File
from CreateData import CreateData
import json

class PEELSorter:
    file = File()
    model = CreateData()
    bucketSelector = "point"
    
    currentFile = "file1"
    
    def PEELFile(self):
        data = self.model.createEmptyPeel()
        self.file.createJsonfile("file1", data)

    def sortPEEL(self, aEntry):
        pass

    def append(self):
        aEntry = self.model.createEmptyEntry()
        aEntry["name"] = "new title"
        data = self.file.readJsonFile(self.currentFile)
        
        data[self.bucketSelector].append(aEntry)
        
        dataToWrite = self.file.createJsonfile(self.currentFile, data)
        d = json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True)
        
    def toText(self):
        #data = self.getData(self.currentFile)
        data = self.file.readJsonFile("file1")

        """put in app"""
        text = ""
        
        name = []
        number = []
        point = []
        citation = []
        references = []
        expand = []
        link = []
        notes = []
        
        for entry in data["entry"]:
            name.append(entry["name"])
            number.append(entry["number"])
            point.append(entry["point"])
            citation.append(entry["Evidence"]["citation"])
            references.append(entry["Evidence"]["reference"])
            expand.append(entry["Expand"])
            link.append(entry["link"])
            notes.append(entry["notes"])
            

        pointStr = "POINT \n------------------------------------------------\n"
        evidenceStr = "EVIDENCE\n------------------------------------------------\n"
        expandStr = "EXPAND\n------------------------------------------------\n"
        linkStr = "LINK\n------------------------------------------------\n"
        referenceStr = "REFERENCES\n------------------------------------------------\n"
        
        for index in range(len(data["entry"])):
            """POINT"""
            pointStr += "point " + str(number[index]) + ", "
            pointStr += name[index] + "\n"
            pointStr += point[index] + "\n\n"

            """EVIDENCE"""  
            evidenceStr += "evidence " + str(number[index]) + ", "
            evidenceStr += name[index] + "\n"
            evidenceStr += citation[index] + "\n\n"

            """EXPAND"""
            expandStr += "Expand " + str(number[index]) + " " + name[index] + ",\n"
            expandStr += expand[index] + "\n\n"

            """LINK"""
            linkStr += "Link " + str(number[index]) + ", " + name[index] + "\n"
            linkStr += link[index] + "\n\n"

            """REFERENCE"""
            referenceStr += "reference " + str(number[index]) + ": \n"
            referenceStr += references[index] + "\n\n"

            
        #pointStr += "\n\nPOINT END\n________________________________________\n"
        #evidenceStr += "\n\nEVIDENCE END\n________________________________________\n"
        #expandStr += "\n\nEXPAND END\n________________________________________\n"
        #linkStr += "\n\nLINK END\n________________________________________\n"
        #referenceStr += "\n\nREFERENCES END\n________________________________________\n"

        
        text = pointStr + "\n\n\n\n" + evidenceStr + "\n\n\n\n" + expandStr + "\n\n\n\n" + linkStr + "\n\n\n\n" + referenceStr
        
        print(text)
        """8 use app version of this"""
        self.file.createTextFile("complete", text)
        #self.file.createTextFile("complete", text)

    def countEntries(self):
        data = self.file.readJsonFile("file1")

        count = 0
        for peelPart in data.keys():
            for entry in data["point"]:
                pass

        count + len(data["point"])
        count + len(data["explain"])
        count + len(data["evaluate"])

#tester = PEELSorter() 
#tester.toText()






