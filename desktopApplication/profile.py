class Profile:
    
    def __init__(self, name, slideMaxLength=4, slideMinLength=0, slideMaxSpeed=4, slideMinSpeed=2) -> None:
        self.name = name
        self.slideMaxLength = slideMaxLength
        self.slideMinLength = slideMinLength
        self.slideMaxSpeed = slideMaxSpeed
        self.slideMinSpeed = slideMinSpeed
        
    def setAllValues(self, values) -> None:
        self.slideMaxLength = values[0]
        self.slideMinLength = values[1]
        self.slideMaxSpeed = values[2]
        self.slideMinSpeed = values[3]

    def getStringValues(self) -> tuple:
        return (str(self.slideMaxLength), str(self.slideMinLength), str(self.slideMaxSpeed), str(self.slideMinSpeed))
    
    def generateSaveFileText(self) -> str:
        text = self.name + "\n"
        for value in self.getStringValues():
            text += value
            text += ','
        text = text[:len(text) - 1] + "\n"
        return text
    
    