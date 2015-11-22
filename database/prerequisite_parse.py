from lxml import html, etree, cssselect
import requests, re
from lxml.html.clean import clean_html
from lxml.cssselect import CSSSelector
from cssselect import GenericTranslator, SelectorError

page = requests.get('http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#courseinventory')
##tree = html.fromstring(page.content)

##print page.content
##for field in tree.finall('strong'):
##          print field.text
##
##
new_page = clean_html(page.content)

print html.tostring(new_page).substring(1, 30)
##print str(html)[0:200]

tree = html.fromstring(new_page)
##sel = CSSSelector('head title')
##results = sel(tree)
##print results

##match = html.tostring(tree)
##print tree.get('head title')
##
##try:
##          expression = GenericTranslator().css_to_xpath('div.id')
##except SelectorError:
##          print('Invalid selector.')
##
##i = 0
##for div in tree.cssselect('div'):
##          print html.tostring(div)
##          i = i + 1
##          if i == 5:
##                    break

contentnav = tree.find(".//div[@class='courseblock']")
#print type(contentnav), contentnav
contentnav1 = tree.xpath(".//div[@class='courseblock']")

#print contentnav1
#print html.tostring(contentnav), '1'
for item in contentnav1:          
          course_html = item.getchildren()[0]
          s =  html.tostring(course_html)
          course = (re.match('(.*?)<strong>(.*?)&(.*?);(.*?);(\w+).(.*?)', s).group(2), re.match('(.*?)<strong>(.*?)&(.*?);(.*?);(\w+).(.*?)', s).group(5))
          print course

          prerequisite_html = item.getchildren()[3]
          print html.tostring(prerequisite_html)
          
                    
##          print item.cssselect('div.courseblock')[0]
##          break
