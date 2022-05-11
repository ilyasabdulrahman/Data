import os
import PyPDF2
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
dir_path = "/Users/ilyasabdulrahman/Desktop/work_docs/some_docs"
os.chdir(dir_path)
file_list = os.listdir()



count = 1
for file_name in file_list:
    # if file_name == "5500147_500499_7.pdf":
    f = open(dir_path+'/' + file_name, 'rb')
    f6 = open("docc" + str(count) + ".txt", "w")
    reader = PyPDF2.PdfFileReader(f)
    n = reader.getNumPages()
    print(n)
    #print("OK")
    file_contents = reader.getPage(0).extractText().split('\n')
    #print(file_contents)
    x = ""

    Obj = reader.getPage(0)
    t = Obj.extractText()
    #print(t)
    # print("OK")
    if t == '':
        print("OK")
        Obj = reader.getPage(1)
        t = Obj.extractText()
        sent_tokenize(t)
        #for ele in t:
            #f6.write(str(t[ele]))
        f6.write(t)
        # print(t)
        # f6.write(t)
        for i in range(3, n):
            PageObj = reader.getPage(i)
            # print("this is page " + str(i)) 
            Text = PageObj.extractText() 
            if Text.find("CHANGE NOTICE") != -1:
                continue
            else:
                sent_tokenize(Text)
                f6.write(Text)
                #for ele in Text:
                    #f6.write(str(Text[ele]))
                # f6.write(Text)
                # print(Text)
    else:
        sent_tokenize(t)
        #for ele in t:
            #f6.write(str(t[ele]))
        f6.write(t)
        # print(t)
        # f6.write(t)
        for i in range(1, n):
            PageObj = reader.getPage(i)
            # print("this is page " + str(i)) 
            Text = PageObj.extractText() 
            if Text.find("CHANGE NOTICE") != -1 or Text.find("NOTICE OF CONTRACT") != -1 or Text.find("NAME & ADDRESS OF CONTRACTOR") != -1 or Text.find("PRIMARY CONTACT ") != -1:
                continue
            else:
                sent_tokenize(Text)
                #for ele in Text:
                    #f6.write(str(Text[ele]))
                f6.write(Text)
                # print(Text)

        #print("OK") 
    count += 1
    f6.close()
    f.close()