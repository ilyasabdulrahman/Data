import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import fitz
import re

dir_path = "/Users/ilyasabdulrahman/Desktop/work_docs/some_docs"
os.chdir(dir_path)
file_list = os.listdir()

count = 1
for file_name in file_list:
    try:
        new_file = open("doc" + str(count) + ".txt", "w")
        with fitz.open(dir_path+'/' + file_name) as doc:
            first_pg = ""
            text = ""
            # loops through each page and removes all stop words
            for page in doc:
                date_pattern='(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4}'
                if first_pg != "":
                    text = ""
                    text = page.get_text()
                    # removes all patterns of dates
                    new_text = re.sub(date_pattern, "", text)
                    # removes all names
                    nt = re.sub(r"[A-Z][a-z]+,?\s+(?:[A-Z][a-z]*\.?\s*)?[A-Z][a-z]+", "", new_text)
                    word_list = word_tokenize(nt)
                    # removes stop words from word_list
                    filtered_words2 = {word.lower() for word in word_list if word not in stopwords.words('english')}
                else:
                    first_pg += page.get_text()
                    # removes all patterns of dates
                    new_first = re.sub(date_pattern, "", first_pg)
                    # writes to new file if first_pg contains "Change Notice"
                    if first_pg.find("Change Notice") != -1:
                        new_file.write(first_pg)
                    # removes all names
                    nf = re.sub(r"[A-Z][a-z]+,?\s+(?:[A-Z][a-z]*\.?\s*)?[A-Z][a-z]+", "", new_first)
                    word_list = word_tokenize(nf)
                    # removes stop words from word_list
                    filtered_words1 = {word.lower() for word in word_list if word not in stopwords.words('english')}
                    continue
                l1 = []
                l2 = []
                # forms a set containing keywords of both strings 
                rvector = filtered_words1.union(filtered_words2)
                for w in rvector:
                    if w in filtered_words1: l1.append(1) # creates a vector/matrix
                    else: l1.append(0)
                    if w in filtered_words2: l2.append(1)
                    else: l2.append(0)
                c = 0
                # cosine formula 
                for i in range(len(rvector)):
                        c+= l1[i]*l2[i]
                cosine = c / float((sum(l1)*sum(l2))**0.5)
                # only writes to new file if not within the threshold
                if cosine >= 0.40:
                    pass
                else:
                    new_file.write(text)
        # increments counter to write to separate file for each pdf document
        count += 1
        new_file.close()
        doc.close()
    except:
        continue