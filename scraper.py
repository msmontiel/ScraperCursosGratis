import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://freebiesglobal.com/dealstore/udemy'
HOME_URL2 = 'https://freebiesglobal.com/dealstore/udemy/page/2'

XPATH_LINK_TO_ARTHICLE ='//a[@class="img-centered-flex rh-flex-center-align rh-flex-justify-center"]/@href'
XPATH_TITLE = '//div[@class="title_single_area"]/text-fill[not(@class)]/text()'
XPATH_UDEMY_LINK = '//div/a[@class="re_track_btn btn_offer_block"]/@href'



def parse_notice(link, today,i):
    try:
        response = requests.get(link)
        
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            link_udemy = parsed.xpath(XPATH_UDEMY_LINK)[0]
            print(link_udemy)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                print(title)
                
                
            except IndexError:
                return

            with open(f'{today}/file{i}.txt', 'w', encoding='utf-8') as f:
                f.write(link_udemy)
               
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL2)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTHICLE)
            #print(links_to_notice)
            i=0

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)


            for link in links_to_notice:
                i+=1
                parse_notice(link, today, i)
        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)



def run():
    parse_home()


if __name__ == '__main__':
    run()
