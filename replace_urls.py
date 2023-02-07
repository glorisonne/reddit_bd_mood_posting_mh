#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
# use "real regex engine" instead of native python re to avoid backtracking of the pattern
# see https://gist.github.com/gruber/249502#gistcomment-1349329
# installed from https://github.com/andreasvc/pyre2 (pip install pyre2)
import re2 as re
import sys

post_file = sys.argv[1] # config.data + "posts_texts.csv"

# source https://gist.github.com/gruber/249502 (copied from first comment with python code)
GRUBER_URLINTEXT_PAT = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')

def replace_urls(text, line_number):
    # urls = []
    # for mgroups in GRUBER_URLINTEXT_PAT.findall(text):
    #     urls.append(mgroups[0])
    # if urls:
    #     print("%d: %s" %(line_number, ", ".join(urls)))
    text = re.sub(GRUBER_URLINTEXT_PAT, "subURLaddress", text)
    return text

post_file_urls_replaced = ".".join(post_file.split(".")[:-1]) + "_urls_replaced.csv"
print("Writing texts with urls replaced to %s" %post_file_urls_replaced)

with open(post_file, "r", encoding="utf-8") as f, open(post_file_urls_replaced, "w", encoding="utf-8", newline='')\
        as csvfile:
    reader = csv.reader(f, delimiter = ",")
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    counter = 0
    for row in reader:
        line_number = counter + 1
        # print(row)
        id, text = row
        text = replace_urls(text, line_number)
        writer.writerow([id, text.strip()])