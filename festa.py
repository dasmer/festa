import sys
import csv
import io

css = open('style.css').read()
csv = csv.DictReader(io.open(sys.argv[1], "r", encoding = "utf-8-sig"))

html = "<html><head><style>" + css + "</style></head><body>"

items = []

for item in csv:
    i = 0
    while i < int(item["quantity"]):
        print item
        items.append(item)
