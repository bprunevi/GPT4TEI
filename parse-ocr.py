# https://www.youtube.com/watch?v=9FCw1xo_s0I&list=PL2VXyKi-KpYuTAZz__9KVl1jQz74bDG7i&index=7


from lxml import etree
import re

rendu = ""
tree = etree.parse("data/hocr-big.html")
for page in tree.xpath("/html/body/div"):
    last_paragraph_lower_vpos = 0
    big_word = 0
    skipping = 0
    for paragraph in page.xpath("div/p"):
        #print(paragraph.attrib)            
        # On teste si un paragraphe est étrangement bas par rapport au précédent, auquel cas on le catégorise comme une note de bas de page et on l'ignore
        paragraph_vpos = int(re.findall(r'\d+', str(paragraph.attrib))[1])
        vdistance_since_last_paragraph = paragraph_vpos - last_paragraph_lower_vpos
        last_paragraph_lower_vpos = int(re.findall(r'\d+', str(paragraph.attrib))[3])
        if skipping == 1:
            skipped_section=""
            for word in paragraph.xpath("span/span"):
                skipped_section = skipped_section + word.text + " "
            print(skipped_section)
        elif (paragraph_vpos > 1200 and vdistance_since_last_paragraph >= 50 and last_paragraph_lower_vpos > 1800):
            print("--------------------")
            print("Skipping section...")
            skipped_section=""
            for word in paragraph.xpath("span/span"):
                skipped_section = skipped_section + word.text + " "
            print(skipped_section)
            skipping = 1
        else:
            rendu = rendu + "\n"
            for word in paragraph.xpath("span/span"):
                # if big_word == 0 and "fsize 12" in str(word.attrib):
                #     rendu = rendu + "-------------------\n"
                #     big_word = 1
                # if big_word == 0 and "fsize 11" in str(word.attrib):
                #     rendu = rendu + "-------------------\n"
                #     big_word = 1
                # elif "fsize 10" in str(word.attrib):
                #      big_word = 0
                rendu = rendu + word.text + " "

#print(rendu)
with open("output/rendu", 'w') as file:
          file.write(rendu)

