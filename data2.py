import os
import PyPDF2

dir_path = "/Users/ilyasabdulrahman/Desktop/work_docs/some_docs"
os.chdir(dir_path)
file_list = os.listdir()



count = 1
for file_name in file_list:
    f = open(dir_path+'/' + file_name, 'rb')
    new_file = open("doc" + str(count) + ".txt", "w")
    reader = PyPDF2.PdfFileReader(f)
    number_of_pages = reader.getNumPages()
    Obj = reader.getPage(0)
    first_pg = Obj.extractText()
    # if first page is unreadble, extracts text from the next one
    if first_pg == '':
        Obj = reader.getPage(1)
        next_pg = Obj.extractText()
        new_file.write(next_pg)
        # checks each page and only writes to file if page is not a change of notice
        for i in range(2, number_of_pages):
            PageObj = reader.getPage(i)
            text = PageObj.extractText() 
            if text.find("CHANGE NOTICE") != -1 or text.find("NOTICE OF CONTRACT") != -1 or text.find("NAME & ADDRESS OF CONTRACTOR") != -1 or text.find("PRIMARY CONTACT ") != -1 or text.find("CHANG E NOT I CE") != -1:
                continue
            else:
                new_file.write(text)
    else:
        new_file.write(first_pg)
         # checks each page and only writes to file if page is not a change of notice
        for i in range(1, number_of_pages):
            PageObj = reader.getPage(i)
            text = PageObj.extractText() 
            if text.find("CHANGE NOTICE") != -1 or text.find("NOTICE OF CONTRACT") != -1 or text.find("NAME & ADDRESS OF CONTRACTOR") != -1 or text.find("PRIMARY CONTACT ") != -1 or text.find("CHANG E NOT I CE") != -1:
                continue
            else:
                new_file.write(text)
    # increments counter to write to separate file for each pdf document
    count += 1
    new_file.close()
    f.close()