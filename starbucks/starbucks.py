from lxml import html

import re

import requests


class Starbucks(object):

    session = requests.session()

    def __init__(self):
        self.session.headers["User-Agent"] = \
            "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)"

    def login(self, id, password):
        url = 'https://www.istarbucks.co.kr/Mem/login_proc.asp'
        data = {
            'userID': id,
            'userPW': password
        }
        r = self.session.post(url, data=data)
        
        success = 'META HTTP-EQUIV' in r.text and not 'alert("' in r.text
        if success:
            url = 'http://www.istarbucks.co.kr/index.asp'
            r = self.session.get(url)
            return 'STARBUCKS' in r.text
        return False

    def logout(self):
        url = 'https://www.istarbucks.co.kr/Mem/login_out.asp'
        r = self.session.get(url)

        logout_confirm = 'http://www.istarbucks.co.kr/Menu/product_list.asp'
        return logout_confirm in r.text

    def get_card_info(self, card_reg_number):
        url = 'http://msr.istarbucks.co.kr/mycard/cardInfo.do?card_reg_number=%s' % card_reg_number
        r = self.session.get(url)

        if 'orgNickName' in r.text:
            return self.parse_card_info(r.text)
        return 'Can\'t get the card information.'

    def parse_card_info(self, txt_card_info):
        card = Card()
        
        raw = html.fromstring(txt_card_info)

        for child in raw.getchildren()[0].getchildren():
            if child.get('name') == 'orgNickName':
                card.nickname = child.get('value')
            elif child.get('name') == 'balance':
                card.balance = child.get('value')
            elif child.get('name') == 'userName':
                card.username = child.get('value')

            if len(child.getchildren()) > 0:
                for more in child.getchildren():
                    if more.get('name') == 'card_number':
                        card.number = more.get('value')
        
        return card
    
    def get_stars_count(self):
        url = 'http://msr.istarbucks.co.kr/star/index.do'
        r = self.session.get(url)
        
        if 'myRewardsHistory' in r.text:
            return self.parse_stars_count(r.text)
        return 'Can\'t get the count of stars.'
    
    def parse_stars_count(self, txt_stars_info):
        raw = html.fromstring(txt_stars_info)

        for child in raw.getchildren()[1].getchildren()[2].getchildren():
            for more in child.getchildren():
                if more.get('class') == 'h1_txt':
                    content = more.text_content()
                    content = content.replace(',', '')
                    return re.findall(r'\b\d+\b', content)[0]
        return 'Can\'t get the count of stars.'


class Card(object):

    username = None
    nickname = None
    number = None
    balance = None

    def __repr__(self):
        return '[%s - %s] Card Number : %s, Balance : %s' % (
            self.username.encode('utf-8'),
            self.nickname.encode('utf-8'),
            self.number.encode('utf-8'),
            self.balance.encode('utf-8'),
        )
