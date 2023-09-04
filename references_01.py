import brk
import requests
import xmltodict
import time
import tkinter as tk
import tkinter.font as tkfont
import os
import random
import subprocess

# Global 1st window for selection
root = tk.Tk()
root.withdraw()
listbox = tk.Listbox(root)
selected_item = ''
font = tkfont.nametofont("TkDefaultFont")

def close_window():
    if selected_item:
        root.destroy()

close_button = tk.Button(root, text="Select", command=close_window)

def on_select(event):
    global selected_item
    selected_index = listbox.curselection()
    if selected_index:
        selected_item = listbox.get(selected_index[0])


def dbl_k_title(filename: str):
    file_r = open(filename, "r", encoding="UTF-8")
    tmp = filename + str(random.randint(10000,20000))
    file_w = open(tmp, "w", encoding="UTF-8")
    title = False
    while True:
        line = file_r.readline()
        if not line:
            break
        pos = line.find("title")
        if (pos == 2):
            line = line.replace("= {", "= {{")
            title = True
        if (title == True):
            if line[-3:] == "},\n":
                line = line.replace("},", "}},")
                title = False
        file_w.writelines(line)
    file_r.close()
    file_w.close()
    os.remove(filename)
    os.rename(tmp, filename)



# prepare information to write files
def prep_entry(entry):
    ref = str(entry).replace("\n" , " ")
    while ref.find("  ") != -1:
        ref = ref.replace("  ", " ")
    url = str(entry["id"])
    pos_cite = url.find("/abs/") + 5
    cite = url[pos_cite:]
    title = str(entry["title"]).replace("\n"," ")
    while title.find("  ") != -1:
        title = title.replace("  ", " ")
    broken = brk.breakline("{{" + title + "}},")
    published = str(entry["published"])
    pub_list = published.split("T")
    date_list = pub_list[0].split("-")
    year = date_list[0]
    month = date_list[1]
    aut = entry["author"]
    
    # Format author to bib
    if (str(type(aut)) == "<class 'list'>"): # more than one author
        band = False
        for b in aut:
            if band == False:
                aut_bib ="  author       = {" + b["name"]
                band = True
            else:
                aut_bib += " and\n                  " + b["name"]
    else:
        aut_bib ="  author       = {" + aut["name"]
    aut_bib += "},\n"
    
    # construct bib format of the document
    my_article = "@misc{arXiv:" + cite + ",\n" # Header of the reference
    my_article += aut_bib # Author of the document
    # Title
    txt = "  {id:12s} = {eq:s}\n".format( id="title"  ,eq=broken[0])
    my_article += txt
    for i in range(1,len(broken)):
        txt = "  {id:12s}    {eq:s}\n".format( id=""  ,eq=broken[i])
        my_article += txt
    my_article += "  month        = {" + month + "},\n" # year published
    my_article += "  year         = {" + year + "},\n" # year published
    my_article += "  url          = {" + url + "}\n" # url to the file or reference
    my_article += "}\n\n" # Close the document information

    # prepare the dictionary to return
    my_dict = {
        "file" : ref + "\n",
        "f2" : (title, url),
        "f3" : my_article
    }
    return my_dict


# Show the options of reference databases
def view_menu(options):
    lng = len(options)
    right = False
    while right == False:
        print("Options :")
        for i in range(lng):
            print(i+1, "-", options[i])
        try:
            choice = int(input("Enter your choice : "))
            if ((choice < 1) or (choice > lng)):
                print("Choice out of range ....")
            else:
                right = True
        except:
            print("Wrong value ...")
    return choice


# Select the right function to work on
# on success return 0 on error return -1
def choose_option(choice):
    if choice == 1:
        result = dblp_text()
    elif choice == 2:
        result = dblp_url()
    elif choice == 3:
        result = arxiv_text()
    elif choice == 4:
        result = springer_url()
    return result


# Access database dblp using keyword to get the references
# on success return 0 on error return -1
def dblp_text():
    global root
    global listbox
    global close_button
    global selected_item
    
    # Define max number of references to retrieve in first atemp, cannot be higher than 1000
    MAX_HITS = 1000

    # ask for the keyword to search
    while True:
        my_key = input("Enter the keyword to search: ")
        if my_key.isnumeric():
            print("   the key cannot be numeric...")
        elif len(my_key) < 3:
            print("   the key must be >= 3 characters...")
        else:
            break

    # Ask for the kind of search
    xt_key = my_key.replace(" ", "* ") + "*"
    while True:
        print("Choose the right option:")
        print("1. Exact search:    ", my_key)
        print("2. Extended search: ", xt_key)
        opt = input("option: ")
        if opt == "1":
            my_key_s = my_key.replace(" ","$+") + "$"
            break
        elif opt == "2":
            my_key_s = my_key.replace(" ", "+")
            found = 0
            break
        else:
            print("Error wrong choice ...")
        
    myhits = MAX_HITS

    while True:
        # turn keyword into an url to query dblp.org
        myurl = 'https://dblp.org/search/publ/api?q=' + my_key_s +'&h=' + str(myhits)

        # Open a connection to the url using urllib
        resp = requests.get(myurl)
        if resp.status_code == 200: # Success
            # Info saved as xml file
            with open("my_file.xml", "wb") as bf:
                bf.write(resp.content)

            # Show statistics of the result of the search
            print("\nStatistics of the result of the search:")
            with open("my_file.xml", "r", encoding="UTF-8") as f:
                band = 0
                while True:
                    line = f.readline().replace(">"," ").replace("</"," ").replace("<","").replace("\n","").strip()
                    fields = line.split(" ")
                    if (fields[0] == "query"):
                        band = 1
                    if (band == 1):
                        l = len(fields)
                        if (l > 1):
                            if (fields[0] == fields[l-1]):
                                for i in range(l-1):
                                    print(fields[i], end=" ")
                                print("")
                            else:
                                print(line)
                    if (fields[0] == "hits"):
                        print("")
                        break    

            # convert xml to dictionary
            mydict = xmltodict.parse(resp.content)
            result = mydict["result"]
            hits = result["hits"]

            # send the references to a file references.txt
            # send the url references to a file urllib.txt
            try:
                hit = hits["hit"]
            # there aren't any references
            except:
                print("Not found any references")
                file = open("references.txt", "w", encoding="UTF-8")
                file.close()
                return -1
            else:
                file = open("references.txt", "w", encoding="UTF-8")
                f2 = open("title_url.txt", "w", encoding="UTF-8")
                f3 = open("reference.bib", "wb")
                # Check if there are more than one references
                if (str(type(hit)) == "<class 'list'>"):
                    numhits = len(hit)
                    count = 1
                    slen = 0
                    root.title("Select an Option")
                    listbox.pack(fill=tk.BOTH, expand=True)
                    dict_title ={}
                    for a in hit:
                        info = a["info"]
                        title = str(info["title"])
                        if opt == '1':
                            found = title.lower().find(my_key.lower())
                        if found != -1:
                            url = str(info["url"])
                            file.write(str(info) + "\n")
                            f2.write("\"" + title + "\"," + url + "\n")
                            listbox.insert(tk.END, f"{title}")
                            tlen = font.measure(title)
                            if tlen > slen:
                                slen = tlen
                            dict_title[title] = url
                            count += 1
                    if count > 1:
                        # show a menu to choose the right tittle
                        listbox.bind("<<ListboxSelect>>", on_select)
                        close_button.pack()
                        root.geometry(f'{slen+5}x300')
                        root.deiconify()
                        root.mainloop()
                        url = dict_title[selected_item]
                        print("Downloading:", selected_item, " wait ...", end=" ")
                    else:
                        print("No one option meet the exact criteria for:  ", my_key)
                        return -1
                # there is just one reference
                else:
                    info = hit["info"]
                    title = info["title"]
                    url = info["url"]
                    file.write(str(info) + "\n")
                    f2.write("\"" + str(title) + "\"," + str(url) + "\n")
                    print("Downloading:", title, " wait ...", end=" ")
                biburl = url + ".bib"
                time.sleep(0.25)
                bibresp = requests.get(biburl)
                if bibresp.status_code == 200: # Success
                    f3.write(bibresp.content)
                    print("success")
                else:
                    print("Error :", bibresp.status_code)            
                file.close()
                f2.close()
                f3.close()
                dbl_k_title("reference.bib")
                return 0
            break
        else: # Error code from the server
            print("Error :", resp.status_code)
            if resp.status_code == 500:
                if myhits == 1:
                    print("There's a temporary problem in the server, please try again later")
                    break
                    return -1
                time.sleep(1)
                print("Changing hits from", myhits, end=" ")
                # Reduce to half the hits objective to reduce the load of the server
                myhits = myhits // 2
                print("to",myhits)
            else:
                break
                return -1

# on success return 0 on error return -1
def dblp_url():
    # ask for the url to search
    url = input("Enter the bib url to search: ")

    a = url.split(".") # https://test.bib --> a[0]  = test , a[1] = bib

    if (len(a) == 1) or (url[0:16] != "https://dblp.org"):
        print("That is not a valid url")
        return -1
    elif (len(a) <= 3):
        biburl = a[0] + "." + a[1] + ".bib"
        print(biburl)

        # Open a connection to the url using urllib
        resp = requests.get(biburl)
        if resp.status_code == 200: # Success
            # Info saved as bib file
            with open("reference.bib", "wb") as bf:
                bf.write(resp.content)
            dbl_k_title("reference.bib")
            return 0
        else: # Error code from the server
            print("Error :", resp.status_code)
            return -1
    else:
        print("That is not a valid url")
        return -1

# on success return 0 on error return -1
def arxiv_text():
    global root
    global listbox
    global close_button
    global selected_item
    
    # Define max number of references to retrieve, cannot be higher than 1000
    MAX_HITS = 100

    # ask for the keyword to search
    while True:
        my_key = input("Enter the keyword to search in the Title: ")
        if my_key.isnumeric():
            print("   the key cannot be numeric...")
        elif len(my_key) < 3:
            print("   the key must be >= 3 characters...")
        else:
            break

    # Ask for the kind of search
    # Test: "A GPU-based Kalman Filter for Track Fitting"
    xt_key = my_key.replace(" ", "* ") + "*"
    while True:
        print("Choose the right option:")
        print("1. Exact search:    ", my_key)
        print("2. Extended search: ", xt_key)
        opt = input("option: ")
        if opt == "1":
            my_key = my_key.replace("-", "%22+AND+ti:%22")
            my_key = "%22" + my_key.replace(" ", "+") + "%22"
            break
        elif opt == "2":
            my_new_key = ""
            my_list = my_key.split(" ")
            for my_word in my_list :
                if len(my_word) > 3 : # Exclude words smaller than 4 characters
                    if my_new_key == "" :
                        my_new_key = my_word
                    else :
                        my_new_key = my_new_key + "+OR+ti:" + my_word
            my_key = my_new_key
            break
        else:
            print("Error wrong choice ...")

    # Information: https://info.arxiv.org/help/api/user-manual.html#_opensearch_extension_elements
    # https://info.arxiv.org/help/api/user-manual.html#detailed_examples
    myurl = 'https://export.arxiv.org/api/query?search_query=ti:' + my_key +'&searchtype=title&source=header&start=0&max_results=' + str(MAX_HITS)

    print("url:", myurl)

    # Open a connection to the url using urllib
    resp = requests.get(myurl)
    if resp.status_code == 200: # Success
        # Info saved as xml file
        with open("my_file_arxiv.xml", "wb") as bf:
            bf.write(resp.content)

        # Show statistics of the result of the search
        print("\nStatistics of the result of the search:")
        with open("my_file_arxiv.xml", "r", encoding="UTF-8") as f:
            band = 0
            while True:
                line = f.readline()
                if line == "":
                    break
                else:
                    line = line.replace(">"," ").replace("</"," ").replace("<","").replace("\n","").strip()
                fields = line.split(" ")
                if (fields[0] == "entry"):
                    print("")
                    break   
                if (fields[0] == "title"):
                    band = 1
                if (band == 1):
                    l = len(fields)
                    if (l > 1):
                        if (fields[0] == fields[l-1]):
                            for i in range(l-1):
                                print(fields[i], end=" ")
                            print("")
                        else:
                            print(line)

        # convert xml to dictionary
        mydict = xmltodict.parse(resp.content)
        feed = mydict["feed"]
        
        # send the references to a file references.txt
        # send the url references to a file urllib.txt
        try:
            entry = feed["entry"]
        # there aren't any references
        except:
            print("Not found any references")
            file = open("references_arxiv.txt", "w", encoding="UTF-8")
            file.close()
            return -1
        else:
            file = open("references_arxiv.txt", "w", encoding="UTF-8")
            f2 = open("title_url_arxiv.txt", "w", encoding="UTF-8")
            f3 = open("reference.bib", "w", encoding="UTF-8")
            # Check if there are more than one references
            if (str(type(entry)) == "<class 'list'>"):
                slen = 0
                root.title("Select an Option")
                listbox.pack(fill=tk.BOTH, expand=True)
                dict_title ={}
                for a in entry:
                    my_dict = prep_entry(a)
                    file.write(my_dict["file"])
                    title = my_dict["f2"][0]
                    url = my_dict["f2"][1]
                    f2.write("\"" + title + "\"," + url + "\n")
                    listbox.insert(tk.END, f"{title}")
                    tlen = font.measure(title)
                    if tlen > slen:
                        slen = tlen
                    dict_title[title] = my_dict["f3"]
                # show a menu to choose the right tittle
                listbox.bind("<<ListboxSelect>>", on_select)
                close_button.pack()
                root.geometry(f'{slen+5}x300')
                root.deiconify()
                root.mainloop()
                f3.write(dict_title[selected_item])
            # there is just one reference
            else:
                my_dict = prep_entry(entry)
                file.write(my_dict["file"])
                title = my_dict["f2"][0]
                url = my_dict["f2"][1]
                f2.write("\"" + title + "\"," + url + "\n")
                f3.write(my_dict["f3"])            
            file.close()
            f2.close()
            f3.close()
            return 0
    else: # Error code from the server
        print("Error :", resp.status_code)
        return -1


def breakl_spr(line: str):
    lines = []
    right = line
    while True:
        pos = right.find(" ",70)
        if pos != -1:
            left = right[:pos]
            right = right[pos+1:]
            lines.append(left +"\n")
        else:
            left = right
            lines.append(left)
        if left == right:
            break
    return lines

# on success return 0 on error return -1
def springer_url():
    # ask for the url to search
    # example html page:
    # https://link.springer.com/chapter/10.1007/978-3-030-90539-2_13
    # bib equivalent:
    # https://citation-needed.springer.com/v2/references/10.1007/978-3-030-90539-2_13?format=bibtex&flavour=citation
    url = input("Enter the url to search: ")

    # validates springer: https://link.springer.com/chapter/
    if ( url[0:34] == "https://link.springer.com/chapter/" ): # Success html
        biburl = "https://citation-needed.springer.com/v2/references/" + url[34:] + "?format=bibtex&flavour=citation"

        # Open a connection to the url using urllib
        resp = requests.get(biburl)
        if resp.status_code == 200: # Success
            # Info saved as bib file
            with open("springer.bib", "wb") as bf:
                bf.write(resp.content)
            
            f1 = open("springer.bib", "r", encoding="UTF-8")
            f2 = open("reference.bib", "w", encoding="UTF-8")

            for line in f1:
                verif = line.split("=")
                if verif[0] == "title":
                    nl = line.replace( "=\"" , "={{" ).replace( "\"," , "}},").replace( "\"" , "}}" )
                else:
                    nl = line.replace( "=\"" , "={" ).replace( "\"," , "},").replace( "\"" , "}" )
                if nl.find("@") != -1:
                    f2.write(nl)
                else:
                    a = nl.split("=")
                    if len(a) == 2: # appears = in the line
                        broken = breakl_spr(a[1])
                        txt = "  {id:13s} = {eq:s}".format( id=a[0]  ,eq=broken[0])
                        f2.write(txt)
                        for i in range(1,len(broken)):
                            txt = "  {id:13s}   {eq:s}".format( id=""  ,eq=broken[i])
                            f2.write(txt)
                    elif len(nl) > 2 :
                        txt = "  {id:13s}   {eq:s}".format( id=""  ,eq=a[0])
                        f2.write(txt)
                    else:
                        txt = nl
                        f2.write(txt)
                    
            f1.close()
            f2.close()
            return 0
        else: # Error code from the server
            print("Error :", resp.status_code)
            return -1
    else:
        print("That is not a valid url")
        return -1


def main():
    # Offers a menu to the user
    options = [
        'dblp text entry',
        'dblp url entry',
        'arxiv text entry',
        'springer url entry'
    ]
    my_choice = view_menu(options)
    my_success = choose_option(my_choice)
    if my_success == 0 :
        try: 
            result = subprocess.run(["python", "references_02.py"], shell=True, check=True)
        except FileNotFoundError as exc:
            print(f"Process failed because the executable could not be found.\n{exc}")
        except subprocess.CalledProcessError as exc:
            print(
                f"Process failed because did not return a successful return code. "
                f"Returned {exc.returncode}\n{exc}"
            )
        except subprocess.TimeoutExpired as exc:
            print(f"Process timed out.\n{exc}")
main()
