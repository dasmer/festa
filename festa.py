import sys
import csv
import io

from bs4 import BeautifulSoup

title = sys.argv[1]
csv_file_name = sys.argv[2]
back_text_file_name = sys.argv[3]

file = open(back_text_file_name, "r")
back_text = "<br />".join(file.read().split("\n"))
file.close()

css = open('style.css').read()
csv = csv.DictReader(io.open(csv_file_name, "r", encoding = "utf-8-sig"))

html = "<html><head><style>" + css + "</style></head><body>"

items = []

for item in csv:
    i = 0
    quantity = item["quantity"]
    quantity = 0 if quantity == "" else int(quantity)
    while i < quantity:
        items.append(item)
        i += 1;

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

html_file = open("output.html", "w")
html_file.write(html)
html_file.close()
