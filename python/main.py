import requests
from bs4 import BeautifulSoup
import sys
from lecture import Lecture
import time 

st = time.time()

r = requests.session()
header = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding": "gzip, deflate, br",
"Connection": "keep-alive"
}


def classStringToValue(clName):
	data = []
	for i in range(3):
		data.append(clName[:clName.index(" - ")])
		clName = clName[clName.index(" - ")+3:]
	data.append(clName)
	return data



subject = "MATH"
classNumber = 1554



#-----------------------------
#Search for all classes
#-----------------------------
response = r.post("https://oscar.gatech.edu/bprod/bwckschd.p_get_crse_unsec",headers=header,data={
	"term_in": "202208",
	"sel_subj": [
		"dummy",
		subject
	],
	"sel_day": "dummy",
	"sel_schd": [
		"dummy",
		"%"
	],
	"sel_insm": "dummy",
	"sel_camp": [
		"dummy",
		"%"
	],
	"sel_levl": "dummy",
	"sel_sess": "dummy",
	"sel_instr": [
		"dummy",
		"%"
	],
	"sel_ptrm": [
		"dummy",
		"%"
	],
	"sel_attr": [
		"dummy",
		"%"
	],
	"sel_crse": classNumber,
	"sel_title": "",
	"sel_from_cred": "",
	"sel_to_cred": "",
	"begin_hh": "0",
	"begin_mi": "0",
	"begin_ap": "a",
	"end_hh": "0",
	"end_mi": "0",
	"end_ap": "a"
})
soup = BeautifulSoup(response.content, 'html.parser')
allClasses = []
for i in soup.find_all("a"):
	if i.get("href"):
		if "p_disp_detail_sched" in i.get("href"):
			temp = classStringToValue(i.text)
			allClasses.append(Lecture(temp[0],temp[1],temp[2],temp[3],"https://oscar.gatech.edu" + i.get("href")))
index = 0
for element in soup.find_all("td",{"class":"dddefault"}):
	if len(str(element)) > 400:
		if "Georgia Tech-Atlanta * Campus" in  str(element):
			setattr(allClasses[index],"inATL",True)
			
		if "Lecture*" in str(element):
			setattr(allClasses[index],"lecture",True)
		index += 1

ogUrl = response.url
soup = None



#-----------------------------
#Get Data of Each Class
#-----------------------------
for i in allClasses:
    stats = {"aCap":None,"aAc":None,"aRe":None,"wCap":None,"aAc":None,"aRe":None}
    tempData = []
    soup = BeautifulSoup(r.get(i.link,headers=header).content, 'html.parser')
    className = soup.find("th",{"class":"ddlabel"}).text
    for x in soup.find_all("td",{"class":"dddefault"}):
        if len(str(x)) < 40:
            tempData.append(int(x.text))
    stats["aCap"] = tempData[0]
    stats["aAc"] = tempData[1]
    stats["aRe"] = tempData[2]
    stats["wCap"] = tempData[3]
    stats["wAc"] = tempData[4]
    stats["wRe"] = tempData[5]
    setattr(i,"seats",stats)




for i in allClasses:
	print(i.__dict__)

print("Response time: ", time.time()-st)