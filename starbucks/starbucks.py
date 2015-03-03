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
            url = 'http://msr.istarbucks.co.kr/star/index.asp'
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
        card.username = re.findall(r'<input type="hidden" id="userId"        name="userId"        value="(.+?)"                          />', txt_card_info)[0].strip()
        card.nickname = re.findall(r'<input type="hidden" id="orgNickName"   name="orgNickName"   value="(.+?)" />', txt_card_info)[0].strip()
        card.number = re.findall(r'<span class="cardNo" id="cardNo">(.+?)</span>', txt_card_info)[0].strip()
        card.balance = re.findall(r'<input type="hidden" id="balance"       name="balance"       value="(.+?)"                          />', txt_card_info)[0].strip()
        return card
    
    def get_stars_count(self):
        url = 'http://msr.istarbucks.co.kr/star/index.do'
        r = self.session.get(url)
        
        if 'myRewardsHistory' in r.text:
            results = list(re.findall(r'<p class="h1_txt"><strong>(.+?)</strong>(.+?)</p>', r.text)[0])
            return '%s %s' % (
                results[0].encode('utf-8'),
                results[1].encode('utf-8')
            )
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
