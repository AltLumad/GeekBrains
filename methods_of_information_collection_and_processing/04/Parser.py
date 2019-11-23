from lxml import html
import requests
from time import sleep
from datetime import datetime

class INewsParser(object):
    def __init__(self, link, xpath_new):
        self._header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
        self._link = link
        self._load_main_link()
        self._xpath_news = xpath_new
        self._list_news = self._get_list_news()
        self.result = None

    def get_html(self):
        return self._html

    def _get_list_news(self):
        return self._root.xpath(self._xpath_news)

    def news2dict(self, news):
        raise NotImplementedError('news2dict')

    def parse_all(self):
        print('-------{}---------'.format(self._link))
        self.result = []
        for news in self._list_news:
            self.result.append(self.news2dict(news))
        print('{} completed!\n\n\n'.format(self._link))
        return self.result

    def _drill_down(self, link):
        sleep(0.5)
        self._html = requests.get(url=link, headers=self._header).text
        return html.fromstring(self._html)

    def _load_main_link(self):
        self._root = self._drill_down(self._link)

class MailNewsParser(INewsParser):
    def __init__(self):
        INewsParser.__init__(self, "https://mail.ru",
                             "//div[contains(@class,'news')]/div[contains(@class,'news-item_main')] | //div[contains(@class,'news')]/div[contains(@class,'news-item_inline')]")

    def news2dict(self, news):
        res = {}
        res['link'] = news.xpath('.//a[contains (@class,"news-item__link")]/@href|.//a[contains (@target,"_blank")]/@href')[-1]
        root = self._drill_down(res['link'])
        try:
            res['header'] = root.xpath("//h1")[0].text
        except:
            try:
                res['header'] = news.xpath('.//h3')[0].text  # бывают и такие
            except:
                print(res['link']) # shit happens
        info = root.xpath("//span[contains(@class,'note__text')]")
        res['date'] = info[0].get('datetime', None)
        try:
            res['source'] = info[1].xpath('./..//span[contains(@class,"link__text")]')[0].text
        except:
            root.xpath('//span[@class="note"]/a/span[@class="link__text"]')[0].text
        return res

class LentaNewsParser(INewsParser):
    def __init__(self):
        INewsParser.__init__(self, "https://lenta.ru",
                             "//section[contains(@class,'js-top-seven')]/div[contains(@class,'span4')]/div[contains(@class,'item')]")

    def news2dict(self, news):
        res = {}
        info = news.xpath('.//a[contains (@href,"news")]/time')[0]
        res['link'] = news.xpath('.//a[contains (@href,"news")]/@href')[0]
        res['header'] = info.tail
        res['source'] = self._link
        res['date'] = info.get('datetime', None)
        return res


'''
def Parse_All():
    keys = input("Input key words: ").replace('+', '%2B')
    n = 10  # количество страниц
    hh_keys = keys.replace(' ', '+')
    sj_keys = keys.replace(' ', '%20')

    hh_parser = HHParser(hh_keys)
    sj_parser = SJParser(sj_keys)
    return  {'HH': hh_parser.parse_all(n), 'SJ': sj_parser.parse_all(n)}

'''

if __name__ == "__main__":
    raise Exception("run main.py")