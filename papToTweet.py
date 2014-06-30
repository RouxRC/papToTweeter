#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Josh Rendek 2009 bluescripts.net
# No liability blah blah use at your own risk, etc

import lxml.html as html
import re
#from twitter import Twitter, OAuth

#raw xml

papPage = "http://www.pap.fr/annonce/locations-appartement-paris-1er-g37768g37769g37770g37771g37772g37773g37774g37776g37777g37778g37779g37785g37786g37787-jusqu-a-1600-euros-a-partir-de-55-m2-40-annonces-par-page"

#xml parsed
doc = html.parse(papPage)
doc = doc.getroot()
annonces = doc.find_class("annonce")

stringAnnonces = []

re_clean_html = re.compile("[\n\s\r\t]+", re.M)
re_annonce = re.compile("^.*(\d\D+pièces.*€).*$")
re_tel = re.compile("((\d{2}\W*?){4}\d{2})")
for annonce in annonces:
    tweet = ""
    header = annonce.find_class("header-annonce")[0].text_content().encode("utf-8")
    header = re_clean_html.sub(" ", header)
    header = re_annonce.sub(r"\1", header)
    header = header.replace(".", "").replace("Paris ", "")
    tweet += header
    try:
        metro = annonce.find_class("metro")[0].text_content().encode("utf-8")
        tweet += "\nmetro" + re_clean_html.sub(" ", metro)
    except: pass
    try:
        description = annonce.find_class("description")[0].text_content().encode("utf-8")
        tweet += " " + re_tel.search(description.strip()).group(0)
    except: pass
    url = annonce.xpath("div[@class='header-annonce']/a/@href")[0]
    tweet += "\nhttp://www.pap.fr" + url
    stringAnnonces.append(tweet+"\n")

try:
    with open("lastAnnonces.txt") as f:
        for l in f.readlines():
            lastAnnonces.append(l.replace("\t", "\n"))
except:
    lastAnnonces = []

for annonce in stringAnnonces:
    if annonce in lastAnnonces:
        pass
    else:
        print annonce
        #twitter.statuses.new(annonce)

with open("lastAnnonces.txt","w") as f:
    for string in stringAnnonces :
        f.write(string.replace("\n", "\t")+"\n")
