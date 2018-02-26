# -*- coding: utf-8 -*-
from supreme import *
import threading


class Checkout():
    def __init__(self, soup, base_url, url, proxy, size, style, num_to_buy, results, bot):
        self.url = url
        self.soup = soup
        self.proxy = proxy;
        self.size = size;
        self.base_url = base_url
        self.style = style
        self.num_to_buy = num_to_buy
        self.bought = 0
        self.results = results
        self.bot = bot

    def add(self):
        product_name = self.soup.find('h1', {'itemprop': 'name'}).string.encode('ascii', errors='ignore')

        print('Adding {} to cart...'.format(product_name))
        session = requests.Session()
        # session.proxies.update(self.proxy)
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/52.0.2743.116 Safari/537.36',
            'X-XHR-Referer': 'http://www.supremenewyork.com/shop/all',
            'Referer': 'http://www.supremenewyork.com/shop/all/',
            'Accept': 'text/html, application/xhtml+xml, application/xml',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
            'DNT': '1'
        })
        form = self.soup.find('form', {'action': re.compile('(?<=/shop/)(.*)(?=/add)')})
        csrf_token = self.soup.find('meta', {'name': 'csrf-token'})['content']
        # find size
        sold_out = self.soup.find('fieldset', {'id': 'add-remove-buttons'}).find('b')
        has_size = form.find('select', {'id': 's'}) != None

        style_value = self.soup.find('input', {'id': 'st'})['value']
        if sold_out is not None:
            print'Sorry product is sold out!'
            sys.exit('Sorry, product is sold out!')
        elif (has_size):
            if self.size.upper() == 'OS':
                size_value = form.find('input', {'name': 'size'})['value']
            else:
                try:
                    size_value = self.soup.find('option', string=self.size.title())['value']
                except:
                    sys.exit('Sorry, {} is sold out!'.format(self.size))

        if form is not None:
            payload = {
                'utf8': '✓',
                'st': str(int(style_value)),
                'commit': 'add to cart'
            }
            if(has_size):
                payload['s'] = str(int(size_value))
            headers = {
                'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
                'Origin': 'http://www.supremenewyork.com',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': self.url,
                'X-XHR-Referer': None,
                'Accept-Encoding': 'gzip, deflate',
            }
            t = session.post(self.base_url + form['action'], data=payload, headers=headers, proxies=self.proxy)
            print('Added to cart!')
            i = self.checkout(session, form.find('input', {"name", 'authenticity_token'}), self.proxy)
            if i:
                self.results.append(i)
        else:
            sys.exit('Sorry, product is sold out!')

    def quit(self):
        sys.exit(0)

    def start(self):
        t = threading.Thread(target=self.add)
        t.setDaemon(True)
        t.start()
        return t

    def get_bought(self):
        return self.bought

    def format_phone(self, n):
        return '({}) {}-{}'.format(n[:3], n[3:6], n[6:])

    def format_card(self, n):
        return '{} {} {} {}'.format(n[:4], n[4:8], n[8:12], n[12:])

    def checkout(self, session, token, proxy):
        print('Filling out checkout info...')
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'authenticity_token': token,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.supremenewyork.com/shop/cart',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
        }
        response = session.get('https://www.supremenewyork.com/shop/cart', headers=headers,  proxies=proxy)
        soup = bs(response.text, 'html.parser')
        form = soup.find('form', {'action': '/checkout'})

        csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'X-CSRF-Token': csrf_token,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.supremenewyork.com/shop/cart',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
        }
        response = session.get("https://supremenewyork.com/checkout", headers=headers, proxies=proxy)
        soup = bs(response.text, 'html.parser')
        form = soup.find('form', {'action': '/checkout'})
        country_abbrv = shipping_country_abbrv
        if country_abbrv == 'US':
            country_abbrv = 'USA'
        payload = {
            'utf8': '✓',
            'authenticity_token': form.find('input', {'name': 'authenticity_token'})['value'],
            'order[billing_name]': first_name + ' ' + last_name,
            'order[email]': email,
            'order[tel]': self.format_phone(phone_number),
            'order[billing_address]': shipping_address_1,
            'order[billing_address_2]': shipping_apt_suite,
            'order[billing_zip]': shipping_zip,
            'order[billing_city]': shipping_city,
            'order[billing_state]': shipping_state,
            'order[billing_country]': country_abbrv,
            'same_as_billing_address': '1',
            'store_credit_id': '',
            'credit_card[type]': card_type,
            'credit_card[cnb]': self.format_card(card_number),
            'credit_card[month]': card_exp_month,
            'credit_card[year]': card_exp_year,
            'credit_card[vval]': card_cvv,
            'order[terms]': '1',
            'hpcvv': '',
            'cnt': '2'
        }
        response = session.get('https://www.supremenewyork.com/checkout', data=payload, headers=headers, proxies=proxy)
        payload = {
            'utf8': '✓',
            'authenticity_token': form.find('input', {'name': 'authenticity_token'})['value'],
            'order[billing_name]': first_name + ' ' + last_name,
            'order[email]': email,
            'order[tel]': self.format_phone(phone_number),
            'order[billing_address]': shipping_address_1,
            'order[billing_address_2]': shipping_apt_suite,
            'order[billing_zip]': shipping_zip,
            'order[billing_city]': shipping_city,
            'order[billing_state]': shipping_state_abbrv,
            'order[billing_country]': country_abbrv,
            'same_as_billing_address': '1',
            'store_credit_id': '',
            'credit_card[type]': card_type,
            'credit_card[cnb]': self.format_card(card_number),
            'credit_card[month]': card_exp_month,
            'credit_card[year]': card_exp_year,
            'credit_card[vval]': card_cvv,
            'order[terms]': '1',
            'hpcvv': ''
        }
        headers = {
            'Origin': 'https://www.supremenewyork.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://www.supremenewyork.com/checkout',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        response = session.post('https://www.supremenewyork.com/checkout', data=payload, headers=headers, proxies=proxy)

        if 'Your order has been submitted' in response.text:
            print('Checkout was successful!')
            return 1
        else:
            soup = bs(response.text, 'html.parser')
            print(soup.find('p').text)
            return 1
