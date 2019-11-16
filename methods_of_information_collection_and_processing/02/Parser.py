from random import randrange
from bs4 import BeautifulSoup as bs
import requests
from time import sleep
import re
import pandas as pd


class IParser(object):
    @staticmethod
    def _random_sleep():
        n = randrange(3) + 1
        print('wait {} seconds...'.format(n))
        sleep(n)


    def __init__(self, vacancy_name, link, source):
        self._vacancy_name = vacancy_name
        self._main_link = link
        self._source = source
        self._header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0', }
        self._html = None
        self.result = None
        self._page_count = 0
        self._current_page = 0
        self._html_tree = None


    def set_next_page(self):
        raise NotImplementedError('set_next_page')

    def execute_page(self):
        raise NotImplementedError('execute_page')

    def _get_currency(self, string):
        raise NotImplementedError('_get_currency')

    def _get_salary(self, string):
        currency = self._get_currency(string)
        if  currency is None:
            return None
        result = string.replace(currency, '').replace('.', '').strip()
        return result


    def prepare(self):
        self._page_count = 0
        self._current_page = 0
        self.result = []


    def set_page_count(self, count):
        if count < 1:
            raise ArithmeticError('The "Count" parameter must be >= 1')
        self._page_count = int(count)

    def next_page(self):
        if self._current_page < self._page_count:
            if not self.set_next_page():
                return False
            self._current_page += 1
            return True
        return False

    def get_html(self):
        return self._html

    def parse_html(self):
        self._html_tree = bs(self._html, 'lxml')

    def input_name(self):
        self._vacancy_name = input("Input somethings").replace('+', '%2B').replace(' ', '+')

    def parse_all(self, page_count):
        print('-------{}---------'.format(self._source))
        self.prepare()
        self.set_page_count(page_count)
        while self.next_page():
            self.parse_html()
            self.execute_page()
            print('--->PAGE {}: SUCCESS!!!'.format(self._current_page))
        print('{} completed!\n\n\n'.format(self._source))

        return self.result

    def _fill_salary(self, vacancy, salary):
        vacancy["min_salary"] = None
        vacancy["max_salary"] = None
        vacancy['currency'] = None
        if salary is not None:
            salary = salary.get_text().split('-')
            if len(salary) == 1:
                salary = salary[0][3:].strip()
                vacancy["min_salary"] = self._get_salary(salary)
                vacancy['currency'] = self._get_currency(salary)
            elif len(salary) == 2:
                vacancy["min_salary"] = salary[0].strip()
                salary = salary[1].strip()
                vacancy["max_salary"] = self._get_salary(salary)
                vacancy['currency'] = self._get_currency(salary)
            else:
                raise Exception('WTF?????')


class HHParser(IParser):
    def __init__(self, vacancy_name):
        IParser.__init__(self, vacancy_name, "https://hh.ru/", "Head Hanter")

    def _get_currency(self, string):
        return re.findall('\w+', string)[-1]

    def set_next_page(self):
        if self._current_page == 0:
            url = self._main_link + '/search/vacancy?st=searchVacancy&text={}'.format(self._vacancy_name)
        else:
            postfix = self._html_tree.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
            if postfix is None:
                return False
            url = self._main_link + postfix['href']
        self._random_sleep()
        self._html = requests.get(url=url, headers=self._header).text
        return True

    def execute_page(self):
        crude_vacancies = self._html_tree.find_all('div', {'class': 'vacancy-serp-item'})
        for crude_vacancy in crude_vacancies:
            vacancy = {}

            main_info = crude_vacancy.find('span', {'class': 'g-user-content'})
            vacancy['name'] = main_info.get_text()
            link = main_info.find('a', recursive=False)['href']
            vacancy['link'] =link
            vacancy['source'] = self._source
            salary = crude_vacancy.find('div', {'class': 'vacancy-serp-item__compensation'})
            self._fill_salary(vacancy, salary)
            self.result.append(vacancy)


class SJParser(IParser):
    def __init__(self, vacancy_name):
        IParser.__init__(self, vacancy_name, "https://www.superjob.ru", "Super Job")

    def _get_currency(self, string):
        res = re.findall('\W+', string)
        return None if not res else res[-1]

    def set_next_page(self):
        if self._current_page == 0:

            url = self._main_link + '/vacancy/search/?keywords={}&geo%5Bc%5D%5B0%5D=1'.format(self._vacancy_name)
        else:
            postfix = self._html_tree.find_all('a', {'rel': 'next'})
            if not postfix:
                return False
            url = self._main_link + postfix[0]['href']
        self._random_sleep()
        self._html = requests.get(url=url, headers=self._header).text
        return True

    def execute_page(self):
        crude_vacancies = self._html_tree.find_all('div', {'class': '_3syPg _3P0J7 _9_FPy'})
        for crude_vacancy in crude_vacancies:
            vacancy = {}

            main_info = crude_vacancy.find('a', {'class': 'icMQ_'})
            vacancy['name'] = main_info.get_text()
            vacancy['link'] = self._main_link + main_info['href']
            vacancy['source'] = self._source
            salary = crude_vacancy.find('span', {'class': 'f-test-text-company-item-salary'})
            self._fill_salary(vacancy, salary)
            self.result.append(vacancy)



def Parse_All():
    keys = input("Input key words: ").replace('+','%2B')
    n = 10  # количество страниц
    hh_keys = keys.replace(' ','+')
    sj_keys = keys.replace(' ','%20')

    hh_parser = HHParser(hh_keys)
    sj_parser = SJParser(sj_keys)
    res = hh_parser.parse_all(n) + sj_parser.parse_all(n)
    return pd.DataFrame(res)


if __name__ == "__main__":
    raise Exception("run main.py")