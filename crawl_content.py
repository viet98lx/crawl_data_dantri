from bs4 import BeautifulSoup
import requests
from lxml import html
import json

list_obj = []
with open('D:\crawl_dantri\crawl_dantri\links_news.txt', 'r') as f:
    list_url = f.readlines()
    for idx, url in enumerate(list_url, 0):
        # print(url)
        page = requests.get(url=url.rstrip("\n"))
        # print(page)
        html_tree = html.fromstring(page.content)
        # print(html_tree)
        title = html_tree.xpath('//article[@class="dt-news__detail"]/h1[@class="dt-news__title"]')
        brief = html_tree.xpath('//article[@class="dt-news__detail"]/div[@class="clearfix"]/'
                                'div[@class="dt-news__body"]/div[@class="dt-news__sapo"]/h2/text()')
        list_contents = html_tree.xpath('//article[@class="dt-news__detail"]/div[@class="clearfix"]/'
                                'div[@class="dt-news__body"]/div[@class="dt-news__content"]/p')
        content = ""
        # print(list_contents)
        for p_tag in list_contents[:]:
            if p_tag.xpath('//span'):
                # print(p_tag)
                paragraph = p_tag.text_content()
                content += (paragraph+'\n')
                # print(paragraph)
            else :
                continue
        try:
            str_title = str(title[0].text_content()).strip()
            str_brief = str(brief[0]).strip()
            str_content = content.rstrip('\n')
            # print(f"Title: {str_title}")
            # print(f"Summary sentences: {str_brief}")
            # print(f"Content : {str_content}")
            list_obj.append({'title': str_title, 'brief': str_brief, 'content': str_content})

            n = (idx+1) % 2000
            if n == 0:
                save_file_path = 'D://text_crawl_dantri//text_dantri_' + str((idx-1999) / 2000) +'.json'
                with open(save_file_path, 'w', encoding='utf-8') as file:
                    file.write(json.dumps(list_obj, ensure_ascii=False))
                    file.close()
                list_obj.clear()

        except:
            print(f"cant parse link: {url}")
            continue

    f.close()
