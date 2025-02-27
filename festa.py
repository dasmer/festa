from __future__ import print_function

import sys
import csv
import io
import os

from bs4 import BeautifulSoup

title = sys.argv[1]
csv_file_name = sys.argv[2]
back_text_file_name = sys.argv[3]
output_file_name = sys.argv[4]

# Creates a temporary csv file that has no non-ascii characters
clean_csv_file_name = "festa_clean_" + csv_file_name
with io.open(csv_file_name,'r',encoding='utf-8',errors='ignore') as infile, \
     io.open(clean_csv_file_name,'w',encoding='ascii',errors='ignore') as outfile:
    for line in infile:
        print(*line.split(), file=outfile)
infile.close()
outfile.close()

file = open(back_text_file_name, "r")
back_text = "<br />".join(file.read().split("\n"))
file.close()

css = open('style.css').read()
csv = csv.DictReader(io.open(clean_csv_file_name, "r", encoding = "utf-8-sig"))

html = "<html><head><style>" + css + "</style></head><body>"
html += "<div class='cover-page'><b>Labels</b><br />"
items = []

for item in csv:
    i = 0
    quantity = item["item_quantity"]
    quantity = 0 if quantity == "" else int(quantity)
    if quantity > 0:
        html += str(quantity) + " " + item["item_name"] + "<br />"
    while i < quantity:
        items.append(item)
        i += 1;
html += "</div>"

for index, item in enumerate(items, start=0):
    if index % 4 == 0:
        html +=  "<div class='label-page'>"

    html += "<div class='label-item'>"
    html += "<div class='label-item-back'>"
    html += "<div class='label-item-back-text'>"
    html += back_text
    html +=  "</div>"
    html +=  "</div>"
    html += "<div class='label-item-front'>"
    html += "<div class='label-item-title'>"
    html += title
    html +=  "</div>"
    html += "<div class='label-item-name'>"
    html += item["item_name"]
    html +=  "</div>"
    html += "<div class='label-item-description'>"
    html += item["item_description"]
    html +=  "</div>"
    html += "<div class='label-item-allergen-images'>"
    if item["item_glutenfree"] == "TRUE":
        html += "<img src='images/gluten-free.png'>"
    if item["item_vegan"] == "TRUE":
        html += "<img src='images/vegan.png'>"
    html +=  "</div>"
    html +=  "</div>"
    html +=  "</div>"

    if index % 4 == 3   :
        html +=  "</div>"


html += "</body></html>"
soup = BeautifulSoup(html, "html.parser")
html = soup.prettify()

html_file = open(output_file_name, "w")
html_file.write(html)
html_file.close()

os.remove(clean_csv_file_name)
os.system("open "+ output_file_name)
