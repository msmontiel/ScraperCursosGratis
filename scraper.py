import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://freebiesglobal.com/dealstore/udemy'
HOME_URL2 = 'https://freebiesglobal.com/dealstore/udemy/page/2'
HOME_URL3 = 'https://freebiesglobal.com/dealstore/udemy/page/3'

XPATH_LINK_TO_ARTHICLE = '//a[@class="img-centered-flex rh-flex-center-align rh-flex-justify-center"]/@href'
XPATH_UDEMY_LINK = '//div/a[@class="re_track_btn btn_offer_block"]/@href'


def parse_notice(link, today):
    try:
        response = requests.get(link)

        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            link_udemy = parsed.xpath(XPATH_UDEMY_LINK)[0]
            with open(f'{today}/links.txt', 'a') as f:
                f.write(link_udemy)
                f.write("\n")
                f.close()

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home(url_in):
    try:
        response = requests.get(url_in)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTHICLE)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notice:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


def run():
    parse_home(HOME_URL)
    parse_home(HOME_URL2)


if __name__ == '__main__':
    run()
