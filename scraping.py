"""
<div data-qa="vacancy-serp__results" id="a11y-main-content"
    <div class="vacancy-serp-item__layout">

        <h3 data-qa="bloko-header-3" class="bloko-header-section-3">
            <span data-page-analytics-event="vacancy_search_suitable_item">
                <a class="bloko-link" target="_blank" href="https://adsrv.hh.ru/click?
                                                                                b=853594&amp;
                                                                                place=35&amp;
                                                                                meta=FBpG5CfgInZjcaeLA5fbKRNvF08wiOGnwZ4COwBrlZaG3VdOQ7l2EA8Po7But0QtFeT5k2OgEDmrMTShcIF81iYKv2VojKNHaJBqElyK4FchbeaEgf2pZC36kq24saYOxudu_1jRwuuXh3CN6mGgBE7IGOtOtrIBzvQFjm1LzRhHKIkjZvxFPjFDy0mQezY6dlHKwUFrlknyoh2xeDjFnCZjGxdj1hfz0nA5aX_MK3th2_XBpnbB031akpxErRyVNLdPD5_vaSrrm3HkgZxcfjKPCaybPuLN_DUTURvfefX5ojUeAXTxobL01thZ0LEK-xArTMvOD7Y4A8c-62LHMKvX2IYgkrObue4hE-7y1tmSicMYbEfT8jxuGDD_WWrLGuSD-lrohLqSo5aBIZtQgcFolQcsNpyiKJ5EMU6UbfgK-Mjmvc7AzbY9U219dOfZsGaDEhW8lEsQ2voV9uBBvHILyQ4cZBZhdjKBY8o04bvhw0s2d7Okq5kFHuaeihZM8N0ibMCv2R50F-FOF_eKwg%3D%3D&amp;
                                                                                clickType=link_to_vacancy">
                    <span class="serp-item__title" data-qa="serp-item__title">Сетевой и системный администратор</span>
                </a>
            </span>

        </h3>

        <div class="vacancy-serp-item-company">

            <div data-qa="vacancy-serp__vacancy-address" class="bloko-text">Санкт-Петербург</div>
        </div>
    </div>
</div>
"""


import bs4
import fake_headers
import requests
import lxml.html as html
from pprint import pprint
import json
import re

URL = "https://spb.hh.ru/search/vacancy/?text=python&area=1&area=2"

def gen_headers():
    headers_gen = fake_headers.Headers(os="win", browser="chrome")
    return headers_gen.generate()

response = requests.get(URL, headers=gen_headers())
main_html = response.text
main_page = bs4.BeautifulSoup(main_html, "lxml")


vacancy_list_tag = main_page.find("div", class_="sticky-sidebar-and-content--NmOyAQ7IxIOkgRiBRSEg")
vacancy_tags = vacancy_list_tag.find_all("div", class_="serp-item vacancy-serp-item_clickme")

vacancy_data = []
vacancy_description = []

for vacancy_tag in vacancy_tags:
    h3_tag = vacancy_tag.find("h3", class_="bloko-header-section-3")
    a_tag = h3_tag.find("a")
    tag_span = h3_tag.find("span", class_="serp-item__title")
    city_tag_div = vacancy_tag.find("div", class_="vacancy-serp-item__info")
    city_tags = city_tag_div.find_all("div", class_="bloko-text")


    link_relative = a_tag["href"]
    link_absolute = f"{link_relative}"
    header = tag_span.text.strip()
    for city_tag in city_tags:
        city = city_tag.text.strip()


    response = requests.get(link_absolute, headers=gen_headers())
    vacancy_html = response.text
    vacancy_page = bs4.BeautifulSoup(vacancy_html, "lxml")
    vacancy_body_tag = vacancy_page.find("div", class_="vacancy-description")
    vacancy_body_tag_div = vacancy_body_tag.find("div", class_="g-user-content")

    vacancy_text =vacancy_body_tag_div.text.strip()


    vacancy_data.append(
        {
            "header": header,
            "city": city,
            "text": vacancy_text,
        }
    )

header_dict = {}
item_dict = []
what_search = "Python"
for item in vacancy_data:
     pattern = r"Python+"
     key_world_header = re.search(pattern, item["header"])
     pattern_world1_desc = r"Django+"
     pattern_world2_desc = r"Flask+"
     key_world_description = re.search(pattern, item["text"])
     key_world_description_1 = re.search(pattern_world1_desc, item["text"])
     key_world_description_2 = re.search(pattern_world2_desc, item["text"])
     #print(key_world_header, key_world_description)
     if key_world_header != None or (key_world_description != None and key_world_description_1 != None and key_world_description_2 != None):
        if item["city"] == "Санкт-Петербург" or item["city"] == "Москва":
            item_dict.append(item)
header_dict["vacation"] = item_dict

capitals_json = json.dumps(header_dict, ensure_ascii=False)
with open("capitals.json", "w", encoding='utf-8') as my_file:
     my_file.write(capitals_json)

