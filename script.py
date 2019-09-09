#!/usr/bin/env python
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
import requests

class TitleParser(HTMLParser):
    trigger = False
    result_data = []

    def handle_starttag(self, tag, attrs):
        tag = str(tag)
        if 'div' in tag:
            if attrs and 'class' == attrs[0][0]:
                if "views-field views-field-title" == attrs[0][1]:
                    TitleParser.trigger = True

    def handle_endtag(self, tag):
        if 'div' in tag:
            TitleParser.trigger = False

    def handle_data(self, data):
        if TitleParser.trigger:
            data = data.encode('utf-8')
            if data != "  " and data != "        ":
                TitleParser.result_data.append(data)

    def result(self):
        return TitleParser.result_data


class WebParser(HTMLParser):
    trigger = False
    result_data = []

    def handle_starttag(self, tag, attrs):
        tag = str(tag)
        if 'div' in tag:
            if attrs and 'class' == attrs[0][0]:
                if "views-field views-field-field-emp-web" == attrs[0][1]:
                    WebParser.trigger = True

        if WebParser.trigger:
            if attrs[0][0] == "href":
                WebParser.result_data.append(attrs[0][1].encode('utf-8'))

    def handle_endtag(self, tag):
        if 'div' in tag:
            WebParser.trigger = False

    def result(self):
        return WebParser.result_data

title_parser = TitleParser()
web_parser = WebParser()

url = 'https://www.incibe.es/protege-tu-empresa/catalogo-de-ciberseguridad/buscador-empresas?combine=&field_emp_tipo_tid=All&term_node_tid_depth_join=All&tid=381&submit=Buscar&page={}'

for page in range(3):
    r = requests.get(url.format(page))
    html = r.text
    title_parser.feed(html)
    web_parser.feed(html)

titles = title_parser.result()
webs = web_parser.result()


print("# Empresas que se dedican a la ciberseguridad en Granada\n")
for x in range(len(titles)):
    t, w = titles[x], webs[x]
    print('-    [{}]({})'.format(t, w))
