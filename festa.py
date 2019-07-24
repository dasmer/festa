import sys
import csv
import io
import os

from bs4 import BeautifulSoup

title = sys.argv[1]
csv_file_name = sys.argv[2]
back_text_file_name = sys.argv[3]
output_file_name = sys.argv[4]

show_title = title != "none"
show_global_back_text = back_text_file_name!= "none"

# Creates a temporary csv file that has no non-ascii characters
clean_csv_file_name = "festa_clean_" + csv_file_name
with io.open(csv_file_name,'r',encoding='utf-8',errors='ignore') as infile, \
     io.open(clean_csv_file_name,'w',encoding='ascii',errors='ignore') as outfile:
    for line in infile:
        print(*line.split(), file=outfile)
infile.close()
outfile.close()

if show_global_back_text:
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

    item_is_glutenfree = item["item_glutenfree"] == "TRUE"
    item_is_vegan = item["item_vegan"] == "TRUE"

    if index % 4 == 0:
        html +=  "<div class='label-page'>"

    html += "<div class='label-item'>"
    html += "<div class='label-item-back'>"
    html += "<div class='label-item-back-text'>"
    if show_global_back_text:
        html += back_text
    else:
        html += "THIS SIDE BACK<br />"
        html += "<h1>" + item["item_name"] + "<br /></h1>"
        html += item["item_description"] + "<br />"
        if item_is_glutenfree:
            html +=  "<b>Item IS GLUTEN-FREE. </b><br />"
        else:
            html +=  "<b>Item IS NOT GLUTEN-FREE. </b><br />"
        if item_is_vegan:
            html +=  "<b>Item IS VEGAN. </b><br />"
        else:
            html +=  "<b>Item IS NOT VEGAN. </b><br />"
    html +=  "</div>"
    html +=  "</div>"
    html += "<div class='label-item-front'>"
    if show_title:
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
    if item_is_glutenfree:
        html += "<img src='html-images/gluten-free.png'>"
    if item_is_vegan:
        html += "<img src='html-images/vegan.png'>"
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
