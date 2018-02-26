#!/usr/bin/env python3
import requests
import random
import timeit
from bs4 import BeautifulSoup as bs
import time
from getconf import *

# User input
use_early_link = True
early_link = 'http://www.jimmyjazz.com/mens/footwear/adidas-ultraboost-laceless/CP9252?color=Dark%20Green'
use_keyword = False
shoe_size = '12'

headers ="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

# Functions
def add_to_cart(early_link, shoe_size):
    print('Adding to Cart')
    response = session.get(early_link, headers={"":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"})
    soup = bs(response.text, 'html.parser')

    available_sizes = []
    size_ids = []
    size_box = soup.find_all('a', {'class': 'box'})

    for a in size_box:
        for sizes in a.stripped_strings:
            available_sizes.append(sizes)
    for ids in size_box:
        size_ids.append(ids['id'][-8:])

    if shoe_size in available_sizes:
        pos = available_sizes.index(shoe_size)
        id = size_ids[pos]
        response = session.get('http://www.jimmyjazz.com/cart-request/cart/add/' + id + '/1', headers=headers)
        #time.sleep(.5)
        return 1
    else:
        return 0


def checkout():
    print('Checking Out')
    response = session.get('http://www.jimmyjazz.com/cart', headers=headers)

    response = session.get('https://www.jimmyjazz.com/cart/checkout', headers=headers)
    soup = bs(response.text, 'html.parser')
    form_id = soup.find('input', {'name': 'form_build_id'})['id']

    payload = {
        'billing_address1': billing_address_1,
        'billing_address2': billing_address_2,
        'billing_city': billing_city,
        'billing_country': billing_country,
        'billing_email': email,
        'billing_email_confirm': email,
        'billing_first_name': first_name,
        'billing_last_name': last_name,
        'billing_phone': phone_number,
        'billing_state': billing_state_abbrv,
        'billing_zip': billing_zip,
        'billing_same_as_shipping':'1',
        'cc_cvv': card_cvv,
        'cc_exp_month': card_exp_month,
        'cc_exp_year': card_exp_year,
        'cc_number': card_number,
        'cc_type': card_type,
        'email_opt_in': '0',
        'form_build_id': form_id,
        'form_id': 'cart_checkout_form',
        'gc_num': '',
        'shipping_address1': shipping_address_1,
        'shipping_address2': shipping_address_2,
        'shipping_city': shipping_city,
        'shipping_first_name': first_name,
        'shipping_last_name': last_name,
        'shipping_method': '1',
        'shipping_state': shipping_state_abbrv,
        'shipping_zip': shipping_zip
    }

    response = session.post('https://www.jimmyjazz.com/cart/checkout', data=payload, headers=headers)
    response = session.get('https://www.jimmyjazz.com/cart/confirm')
    soup = bs(response.text, 'html.parser')
    form_id = soup.find('input', {'name': 'form_build_id'})['id']

    payload = {
        'form_build_id': form_id,
        'form_id': 'cart_confirm_form'
    }
    response = session.post('https://www.jimmyjazz.com/cart/confirm', data=payload, headers=headers)
    try:
        soup = bs(response.text, 'html.parser')
        error = soup.find('div', {'class': 'messages error'}).text
        print(error)
    except:
        print('Checkout was successful!')

def get_user_agent():
        return random.choice([
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",
            "Mozilla/5.0 (iPad; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5",
            "Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true",
            "Mozilla/5.0 (Linux; U; en-us; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us; Silk/1.0.141.16-Gen4_11004310) AppleWebkit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true",
            "Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; Nexus S Build/GRJ22) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (Linux; Android 4.3; Nexus 7 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.72 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
            "Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+",
            "Mozilla/5.0 (Linux; Android 4.3; Nexus 10 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.72 Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 2.3; en-us; SAMSUNG-SGH-I717 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Linux; Android 4.2.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 2.2; en-us; SCH-I800 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        ])


# Main
start = timeit.default_timer()
session = requests.Session()


if use_early_link:
    if add_to_cart(early_link, shoe_size):
        checkout()
    else:
        print('Size ' + shoe_size + ' not available')

stop = timeit.default_timer()
print(stop - start)

