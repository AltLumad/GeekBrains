from Parser import Parse_All
from pprint import pprint

if __name__ == "__main__":
    res = Parse_All()
    pprint(res.iloc[1])
    res.to_csv('result.csv', encoding='utf-8')
    pass
