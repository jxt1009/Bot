from supreme import *
import sys
import requests

class test:
    use_early_link = False

    early_link = 'http://www.supremenewyork.com/shop/jackets/vn2t1jhs3'

    threadpool = []

    def kill(self):
        sys.exit(0)


    def start(self):
        session1 = requests.Session()
        session1.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/52.0.2743.116 Safari/537.36',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
        })
        s = bot()
        if self.use_early_link:
            try:
                response1 = session1.get(self.early_link)
                soup = bs(response1.text, 'html.parser')
                t = threading.Thread(target=s.start_checkout,args=(soup, self.early_link,self))
                t.setDaemon(True)
                self.threadpool.append(t)
                t.start()
            except Exception as e:
                print(e)
                sys.exit('Unable to connect to site...')
        else:
            try:
                url = s.base_url + '/shop/all/' + keywords_category[0] + '/'
                response1 = session1.get(url)
            except:
                sys.exit('Unable to connect to site...')
            soup = bs(response1.text, 'html.parser')
            links = soup.find_all('a', href=True)
            links_by_keyword = []
            for link in links:
                for keyword in keywords_category:
                    product_link = link['href']
                    if keyword in product_link and 'all' not in product_link:
                        if product_link not in links_by_keyword:
                            links_by_keyword.append(link['href'])
            for x in links_by_keyword:
                print(x)
                t = threading.Thread(target=s.product_page,args=x)
                self.threadpool.append(t)
                t.start()

if __name__ == '__main__':
    test = test()
    t = threading.Thread(target=test.start)
    t.start()