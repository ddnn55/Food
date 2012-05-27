#!/usr/bin/env python

import os

import wikitools
from PIL import Image

class TaxonomyImage:

   def __init__(self, root_category_name, ignore=[]):
      self.wikipedia_en = wikitools.wiki.Wiki()
      self.root_category = wikitools.category.Category(self.wikipedia_en, root_category_name)
      self.ignore = ignore

   def getFirstImageForPage(self, page):
      params = {'action':'query', 'prop':'images', 'imlimit':'10', 'titles':page.title, 'redirects':''}
      request = wikitools.api.APIRequest(self.wikipedia_en, params)
      response = request.query()
      try:
      #if True:
         image_title = response['query']['pages'].values()[0]['images'][0]['title']
         if os.path.exists("data/"+image_title):
            print image_title + " - already downloaded"
         else:
            print image_title + " - downloading"
            image_wikifile = wikitools.wikifile.File(self.wikipedia_en, image_title)
            image_wikifile.download(location="data/"+image_title)
         #return Image.open("data/"+image_title)
         return None
      except:
         return None

   def getImageForCategory(self, category, depth=0):
      if category.title in self.ignore:
         return

      print depth * "-" + category.title
      sub_categories = category.getAllMembers()
      images = []
      for member_page in sub_categories:
	 if member_page.title[0:len("Category:")] == "Category:":
	    sub_category = wikitools.category.Category(self.wikipedia_en, member_page.title)
            images.append(self.getImageForCategory(sub_category, depth+1))
         elif depth > 0:
            page_image = self.getFirstImageForPage(member_page)
            images.append(page_image)
      # TODO compose images[] into a single image and return
      return None
      

   def saveImage(self, filename):
      image = self.getImageForCategory(self.root_category)
      image.save(filename)

foods_image = TaxonomyImage("Foods", ["Category:Appellations", "Category:Brand name food products", "Category:Food portal", "Category:Lists of foods"])
foods_image.saveImage("foods.jpg")
