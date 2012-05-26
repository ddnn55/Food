#!/usr/bin/env python

from wikitools import wiki, category

wikipedia_en = wiki.Wiki()
foods = category.Category(wikipedia_en, "Foods")

members = foods.getAllMembersGen()

for member in members:
   if member.title[0:len("Category:")] == "Category:":
      print member.title + "yea"
      sub_category = category.Category(wikipedia_en, member.title)
      sub_categories = sub_category.getAllMembersGen()
      for sub_category in sub_categories:
         print sub_category
      
