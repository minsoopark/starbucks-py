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
        
        card_image = raw.xpath('//img[@id="cardImage"]')[0]
        
        card.cardname = card_image.get('alt')
        card.img_url = card_image.get('src')
        card.nickname = raw.xpath('//*[@name="orgNickName"]')[0].get('value')
        card.balance = raw.xpath('//*[@name="balance"]')[0].get('value')
        card.username = raw.xpath('//*[@name="userName"]')[0].get('value')
        card.number = raw.xpath('//*[@name="card_number"]')[0].get('value')
        
        return card
    
    def get_cards(self):
        url = 'http://msr.istarbucks.co.kr/mycard/index.do'
        r = self.session.get(url)
        
        raw = html.fromstring(r.text)
        
        raw_cards = raw.xpath('//ul')[0].getchildren()
        reg_numbers = []

        for card in raw_cards:
            link = card.xpath('.//a')[0].get('href')
            reg_number = re.findall(r'\'(.+?)\'', link)[0]
            reg_numbers.append(str(reg_number))

        cards = []
        for reg_number in reg_numbers:
            card = self.get_card_info(reg_number)
            cards.append(card)

        return cards
    
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
      
    def get_beverage(self, id):
        url = 'http://www.istarbucks.co.kr/mobile/products/beverage_view.asp?Product_cd=%s' % id
        
        r = self.session.get(url)
        
        raw = html.fromstring(r.text)
        
        beverage = Beverage()
        beverage.id = id
        beverage.name = raw.xpath('//h3[@class="prdTitle"]')[0].text
        beverage.img_url = raw.xpath('//div[@id="thumb"]')[0].xpath('.//img')[0].get('src')
        beverage.description = raw.xpath('//p[@class="subTitle"]')[0].text_content()
        
        return beverage
    
    def get_beverages(self):
        prods = ['P020100', 'P020200', 'P020300', 'P020400', 'P020500', 'P020700', 'P020800']
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
            link = el_menu.xpath('.//a')[0].get('href')
            beverage.id = re.findall(r'\'.+?\'', link)[1]
            beverage.name = el_menu.xpath('.//strong[last()]')[0].text_content()
            beverage.img_url = el_menu.xpath('.//img')[0].get('src')
            beverages.append(beverage)
            
        return beverages
    
    def get_coupons(self):
        url = 'http://msr.istarbucks.co.kr/coupon/valid.do'
        r = self.session.get(url)

        raw = html.fromstring(r.text)

        table = raw.xpath('//table[@class="bbsList"]')[0]
        tbody = table.xpath('.//tbody')[0]
        trs = tbody.xpath('.//tr')

        coupons = []
        
        for tr in trs:
            coupon = Coupon()
            coupon.name = tr.xpath('.//span')[0].text.strip()
            coupon.created_at = tr.xpath('.//td[@class="dataT"]')[0].text_content().strip()
            coupon.expired_at = re.sub(r'[\t\n]', '', tr.xpath('.//td')[3].text_content().strip())
            coupon.img_url = tr.xpath('.//img')[0].get('src')
            coupons.append(coupon)
        
        return coupons


class Card(object):

    cardname = None
    username = None
    nickname = None
    number = None
    balance = None
    img_url = None

    def __repr__(self):
        return '%s [%s - %s] Card Number : %s, Balance : %s, Image : %s' % (
            self.cardname.encode('utf-8'),
            self.username.encode('utf-8'),
            self.nickname.encode('utf-8'),
            self.number.encode('utf-8'),
            self.balance.encode('utf-8'),
            self.img_url.encode('utf-8'),
        )


class Beverage(object):

    id = None
    name = None
    img_url = None
    description = None

    def __repr__(self):
        return '%s - [%s] Image : %s' % (
            self.id.encode('utf-8'),
            self.name.encode('utf-8'),
            self.img_url.encode('utf-8'),
        )


class Coupon(object):
    
    name = None
    created_at = None
    expired_at = None
    img_url = None
    
    def __repr__(self):
        return '[%s] Created : %s, Expired : %s, Image : %s' % (
            self.name.encode('utf-8'),
            self.created_at.encode('utf-8'),
            self.expired_at.encode('utf-8'),
            self.img_url.encode('utf-8'),
        )
