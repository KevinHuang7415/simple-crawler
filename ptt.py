import time
import requests

class Page:
    """description of class"""

    PTT_URL = 'https://www.ptt.cc'

    def __init__(self):
        self.set_url(use_join=True)


    def __str__(self):
        return str(self.url)


    def set_url(self, uri=None, use_join=False):
        if not use_join:
            self.url = uri
        else:
            if uri:
                self.url = '/'.join(['/bbs', uri, 'index.html'])
            else:
                self.url = '/bbs/index.html'


    def get_web_page(self, t=0.4):
        '''Get web page content.'''
        # to avoid being detected as DDOS
        time.sleep(t)
        resp = requests.get(self.PTT_URL + self.url)

        if resp.status_code == 200:
            return resp.text
        print('Invalid URL:', resp.url)
        return None
