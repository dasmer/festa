from __future__ import print_function

import sys
import csv
import io
import os

from bs4 import BeautifulSoup

csv_file_name = sys.argv[1]
output_file_name = sys.argv[2]

# Creates a temporary csv file that has no non-ascii characters
clean_csv_file_name = "festa_clean_" + csv_file_name
with io.open(csv_file_name,'r',encoding='utf-8',errors='ignore') as infile, \
     io.open(clean_csv_file_name,'w',encoding='ascii',errors='ignore') as outfile:
    for line in infile:
        print(*line.split(), file=outfile)
infile.close()
outfile.close()

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

CARDS_PER_PAGE = 8

filled_cards_count = len(items) * 2
empty_cards_count = filled_cards_count % (2 * CARDS_PER_PAGE)
total_cards_count = filled_cards_count + empty_cards_count
print(total_cards_count)
blank_item = {
"item_name": "",
"item_description": "",
"item_vegan": "FALSE",
"item_glutenfree": "FALSE",
"item_additional_backtext": ""
}

blank_i = 0
while blank_i < empty_cards_count:
    items.append(blank_item)
    blank_i += 1

iteration = 0
while iteration < total_cards_count:
    print(iteration)
    quotient_small = iteration / CARDS_PER_PAGE
    quotient_large = iteration / (CARDS_PER_PAGE * 2)
    is_back_card = ((quotient_small % 2) == 1) # is_back_card is TRUE if quotient is odd
    adjustment = quotient_large * CARDS_PER_PAGE
    adjusted_index = iteration - adjustment if is_back_card == False else iteration - adjustment - CARDS_PER_PAGE
    item = items[adjusted_index]

    # if iteration % CARDS_PER_PAGE == 0:
    #     html +=  "<div class='label-page'>"

    if not is_back_card:
        if iteration % CARDS_PER_PAGE == 0:
            html +=  "<div class='label-page-front'>"

        print(item["item_name"])
        html += "<div class='label-item-front'>"
        html += "<div class='label-item-title'>"
        html += "<b>Tandoor Palace</b>"
        html +=  "</div>"
        html += "<div class='label-item-name'>"
        html += item["item_name"]
        html +=  "</div>"
        html += "<div class='label-item-description'>"
        html += item["item_description"]
        html +=  "</div>"
        html += "<div class='label-item-allergen-images'>"
        if item["item_glutenfree"] == "TRUE":
            html += "<img src='html-images/gluten-free.png'>"
        if item["item_vegan"] == "TRUE":
            html += "<img src='html-images/vegan.png'>"
        html +=  "</div>"
        html +=  "</div>"
    else:
        if iteration % CARDS_PER_PAGE == 0:
            html +=  "<div class='label-page-back'>"

        html += "<div class='label-item-back'>"
        html += "<div class='label-item-back-text'>"
        html += "BACKSIDE"
        html += "<h1>" + item["item_name"] + "</h1>"
        html += "<h4>" + item["item_description"] + "</h4>"
        if item["item_glutenfree"] == "TRUE":
            html += "IS GLUTEN-FREE<br />"
        else:
            html += "IS-NOT GLUTEN-FREE<br />"
        if item["item_vegan"] == "TRUE":
            html += "IS VEGAN"
        else:
            html += "IS-NOT VEGAN"
        html += "</div>"
        html += "</div>"

    if iteration % CARDS_PER_PAGE == CARDS_PER_PAGE - 1:
        html +=  "</div>"
    iteration += 1

# for index, item in enumerate(items, start=0):
#     if index % 8 == 0:
#     html +=  "<div class='label-page'>"
#
#     html += "<div class='label-item-back'>"
#     html += "<div class='label-item-back-text'>"
#     html += back_text
#     html +=  "</div>"
#     html +=  "</div>"
#     html += "<div class='label-item-front'>"
#     html += "<div class='label-item-title'>"
#     html += title
#     html +=  "</div>"
#     html += "<div class='label-item-name'>"
#     html += item["item_name"]
#     html +=  "</div>"
#     html += "<div class='label-item-description'>"
#     html += item["item_description"]
#     html +=  "</div>"
#     html += "<div class='label-item-allergen-images'>"
#     if item["item_glutenfree"] == "TRUE":
#         html += "<img src='html-images/gluten-free.png'>"
#     if item["item_vegan"] == "TRUE":
#         html += "<img src='html-images/vegan.png'>"
#     html +=  "</div>"
#     html +=  "</div>"
#
#     if index % 4 == 7   :
#         html +=  "</div>"
#
#
html += "</body></html>"
soup = BeautifulSoup(html, "html.parser")
html = soup.prettify()

html_file = open(output_file_name, "w")
html_file.write(html)
html_file.close()

os.remove(clean_csv_file_name)
os.system("open "+ output_file_name)
