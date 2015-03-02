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
        return 'META HTTP-EQUIV' in r.text and not 'alert("' in r.text

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
        return 'Need to login!'

    def parse_card_info(self, txt_card_info):
        card = Card()
        card.username = re.findall(r'<input type="hidden" id="userId"        name="userId"        value="(.+?)"                          />', txt_card_info)[0]
        card.nickname = re.findall(r'<input type="hidden" id="orgNickName"   name="orgNickName"   value="(.+?)" />', txt_card_info)[0]
        card.number = re.findall(r'<span class="cardNo" id="cardNo">(.+?)</span>', txt_card_info)[0]
        card.balance = re.findall(r'<input type="hidden" id="balance"       name="balance"       value="(.+?)"                          />', txt_card_info)[0]
        return card


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
