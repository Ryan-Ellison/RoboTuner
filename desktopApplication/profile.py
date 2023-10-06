class Profile:
    
    def __init__(self) -> None:
        defaultSlideMaxLength = 4
        defaultSlideMinLength = 0
        defaultSlideMaxSpeed = 4
        defaultSlideMinSpeed = 2

        self.slideMaxLength = defaultSlideMaxLength
        self.slideMinLength = defaultSlideMinLength
        self.slideMaxSpeed = defaultSlideMaxSpeed
        self.slideMinSpeed = defaultSlideMinSpeed
        
    def getStringValues(self) -> tuple:
        return (str(self.slideMaxLength), str(self.slideMinLength), str(self.slideMaxSpeed), str(self.slideMinSpeed))
    
    