from mimetypes import init


class Lecture:
    def __init__(self,name,crn,num,sec,link):
        self.name = name
        self.crn = crn
        self.num = num
        self.sec = sec
        self.link = link
        self.inATL = False
        self.lecture = False
