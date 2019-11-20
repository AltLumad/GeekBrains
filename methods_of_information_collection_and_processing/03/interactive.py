from Parser import Parse_All
from db import MongoWrap
from pprint import pprint

def ParseAndStored():
    res = Parse_All()
    MongoWrap.StoreData(res['HH'], res['SJ'])

def FindBySalary():
    u = int(input('Input min salary limit: '))
    pprint(MongoWrap.FindSalaryGreater(u))


def UserInteractive():
    n = ''
    actions = {1: ParseAndStored, 2:  FindBySalary}
    while n not in [1, 2]:
        print("Available actions")
        print("1. Parse and save vacancies by key words")
        print("2. Find stored vacancies by key words")
        try:
            n = int(input('Input the number: '))
            actions[n]()
        except:
            n = ''


