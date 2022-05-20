import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import fitz

dir_path = "/Users/ilyasabdulrahman/Desktop/work_docs/some_docs"
os.chdir(dir_path)
file_list = os.listdir()

count = 1
page_count = 1
for file_name in file_list:
    try:
        new_file = open("doc" + str(count) + ".txt", "w")
        with fitz.open(dir_path+'/' + file_name) as doc:
            first_pg = ""
            text = ""
            # loops through each page and removes all stop words
            for page in doc:
                if first_pg != "":
                    text = ""
                    text = page.get_text()
                    word_list = word_tokenize(text)
                    # removes stop words from word_list
                    filtered_words2 = {word.lower() for word in word_list if word not in stopwords.words('english')}
                else:
                    first_pg += page.get_text()
                    # writes to new file if first_pg contains "Change Notice"
                    if first_pg.find("Change Notice") != -1:
                        new_file.write(first_pg)
                    word_list = word_tokenize(first_pg)
                    # removes stop words from word_list
                    filtered_words1 = {word.lower() for word in word_list if word not in stopwords.words('english')}
                    #if first page is unreadable, continues to the next page
                    if first_pg == "":
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
                if cosine >= 0.41:
                    # outlier on page 9 of pdf file named "591B7700135_558491_7.pdf"
                    # contains many of the same keywords as the most updated change of notice
                    # which allows the cosine of similarity to be within the threshold
                    if cosine == 0.46561240821866673:
                        new_file.write(text)
                    else:
                        pass
                else:
                    new_file.write(text)
                page_count += 1
        # resets page counter for each pdf document
        page_count = 1
        # increments counter to write to separate file for each pdf document
        count += 1
        new_file.close()
        doc.close()
    except:
        continue