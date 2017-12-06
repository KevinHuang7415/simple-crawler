import requests


PTT_URL = 'https://www.ptt.cc'
SOFTJOB_URI = '/bbs/Soft_Job/index.html'


def get_web_page(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print('Invalid URL:', resp.url)
        return None
    else:
        return resp.text

if __name__ == '__main__':
    current_page = get_web_page(PTT_URL + SOFTJOB_URI)