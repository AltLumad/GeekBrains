from pymongo import MongoClient
from pymongo.errors import BulkWriteError


class MongoWrap:
    _client = None

    @staticmethod
    def GetIntanceDB():
        if not MongoWrap._client:
            MongoWrap._client = MongoClient('localhost',27017)
        return MongoWrap._client['vacancies']

    @staticmethod
    def StoreDataCollection(collection, data):
        if data is not None and not []:
            collection.create_index("link", unique=True)  # Предпологается что ссылка однозначно определяет и задаёт уникальность вакансии в пределах сайта
            try:
                collection.insert_many(data)
            except BulkWriteError:
                pass # игнорим ошибку не уникальности

    @staticmethod
    def StoreData(hh_data, sj_data):
        db = MongoWrap.GetIntanceDB()
        MongoWrap.StoreDataCollection(db.HH, hh_data)
        MongoWrap.StoreDataCollection(db.SJ, sj_data)
        print('Vacancies stored!')

    @staticmethod
    def FindSalaryGreater(min_salary_limit):
        db = MongoWrap.GetIntanceDB()
        HH = db.HH.find({'min_salary': {'$gte': min_salary_limit}})
        SJ = db.SJ.find({'min_salary': {'$gte': min_salary_limit}})
        res = []
        for h in HH:
            res.append(h)
        for s in SJ:
            res.append(s)
        return res


