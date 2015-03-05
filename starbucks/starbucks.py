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
        
        card.nickname = raw.xpath('//*[@name="orgNickName"]')[0].get('value')
        card.balance = raw.xpath('//*[@name="balance"]')[0].get('value')
        card.username = raw.xpath('//*[@name="userName"]')[0].get('value')
        card.number = raw.xpath('//*[@name="card_number"]')[0].get('value')
        
        return card
    
    def get_stars_count(self):
        url = 'http://msr.istarbucks.co.kr/star/index.do'
        r = self.session.get(url)
        
        if 'myRewardsHistory' in r.text:
            return self.parse_stars_count(r.text)
        return 'Can\'t get the count of stars.'
    
    def parse_stars_count(self, txt_stars_info):
        raw = html.fromstring(txt_stars_info)
        
        content = raw.xpath('//*[@class="h1_txt"]')[0].text_content()
        content = content.replace(',', '')
        
        return re.findall(r'\b\d+\b', content)[0]
    
    def get_beverages(self):
        prods = ['P020100', 'P020200', 'P020300', 'P020400', 'P020500']
        result = ''
        
        url = 'http://www.istarbucks.co.kr/Menu/product_list_ajax.asp'
        for prod in prods:
            data = {
                'Prod': prod
            }
            r = self.session.post(url, data=data)
            result += r.text
        
        raw = html.fromstring(result)

        beverages = []
        el_menus = raw.xpath('//li')

        for el_menu in el_menus:
            beverage = Beverage()
            beverage.name = el_menu.xpath('.//strong')[0].text_content()
            beverage.img_url = el_menu.xpath('.//img')[0].get('src')
            beverages.append(beverage)
            
        return beverages


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


class Beverage(object):

    name = None
    img_url = None

    def __repr__(self):
        return '[%s] Image : %s' % (
            self.name.encode('utf-8'),
            self.img_url.encode('utf-8'),
        )