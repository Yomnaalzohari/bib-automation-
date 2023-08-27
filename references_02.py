# http://www.paolomonella.it/pybtex/index.html
# https://docs.pybtex.org/api/parsing.html#bibliography-data-classes
from pybtex.database import parse_file
import brk
import tkinter as tk
from tkinter import scrolledtext
import os
import random
import re

# prepare information to write files to update
def prep_entry_u(entry: str):
    output = ""
    my_list = entry.split("\n")
    lng = len(my_list)
    count = 0
    for ml in my_list :
        if count == 0 :
            output += ml + "\n"
        elif ml == "}" :
            output += ml + "\n"
            break
        else:
            #a = ml.split("\"")
            a = re.sub(',$', '', ml)
            #a = a.replace("\"","").replace("{","").replace("}","").replace("\\","")
            b = a.split("=")
            id = b[0].strip()
            txt = "  {id:9s} = ".format(id=id)
            output += txt
            if id == "author" or id == "editor":
                txt = b[1].strip().replace("and", "and\n              ")
                output += txt
            else :
                broken = brk.breakline(b[1].strip())
                if len(broken) == 1 :
                    txt = broken[0]
                    output += txt
                else :
                    txt = broken[0] + "\n"
                    output += txt
                    for i in range(1,len(broken)):
                        txt = "               " + broken[i]
                        output += txt
                        if i != (len(broken) - 1) :
                            output += "\n"
            output += ",\n"
        count += 1
    output = output.replace("= \"", "= {").replace("\",", "},").replace("},\n}","}\n}")
    return output

def bib_update():
    chosen = ''
    old = ''
    if os.path.exists('myfile.bib'):
        try:
            bib_DB = parse_file('myfile.bib')
            bib_file = parse_file('reference.bib')
            nw = open("new_entries.bib", "w", encoding="UTF-8")
            for e in bib_file.entries:
                title_file = bib_file.entries[e].fields['title']
                title_file = title_file.replace("{","").replace("}","").lower()
                found = False
                for f in bib_DB.entries:
                    title_DB = bib_DB.entries[f].fields['title']
                    title_DB = title_DB.replace("{","").replace("}","").lower()
                    if title_file == title_DB :
                        found = True
                        old = str(bib_DB.entries[f].to_string('bibtex'))
                        new = str(bib_file.entries[e].to_string('bibtex'))
                        choose_entry(old, new)
                        break
                if found == False :
                    entry = str(bib_file.entries[e].to_string('bibtex'))
                    nw.write(prep_entry_u(entry))
                    nw.write("\n")
            nw.close()
        except:
            print("There's something wrong with the format of the database")
            print("The database cannot be readed...")
            print("Please replace the database with a good one...")


        inp = open("new_entries.bib", "r", encoding="UTF-8")
        app = open("myfile.bib", "a+", encoding="UTF-8")
        app.write("\n")
        app.write(inp.read())
        inp.close()
        app.close()
    else:
        print("Reference database:  myfile.bib  doesn't exist")
        print("Creating database: myfile.bib")
        inp = open("reference.bib", "r", encoding="UTF-8")
        app = open("myfile.bib", "w", encoding="UTF-8")
        app.write("\n")
        app.write(inp.read())
        inp.close()
        app.close()
    if selected_choice == 1:
        change_to(new, title_file)


def change_to(new: str, title_1: str):
    filename = 'myfile.bib'
    bib_DB = parse_file(filename)
    tmp = filename + str(random.randint(10000,20000))
    file_w = open(tmp, "w", encoding="UTF-8")
    for f in bib_DB.entries:
        title_2 = bib_DB.entries[f].fields['title']
        title_2 = title_2.replace("{","").replace("}","")
        entry = str(bib_DB.entries[f].to_string('bibtex'))
        # print(entry)
        if title_1 == title_2:
            file_w.write(prep_entry_u(new))
        else:
            file_w.write(prep_entry_u(entry))
    file_w.close()
    os.remove(filename)
    os.rename(tmp, filename)


def save_text():
    global selected_choice
    selected_choice = selected.get()
    root.destroy()

# Solved comparing the two entries side by side
def choose_entry(old : str, new: str):
    root.deiconify()
    text_widgets[0].insert(tk.INSERT, old)
    text_widgets[1].insert(tk.INSERT, new)
    root.mainloop()

selected_choice = 0
root = tk.Tk()
root.withdraw()
root.title("Reference comparison")

# Create Text Widgets
text_widgets = [scrolledtext.ScrolledText(root) for _ in range(2)]

rb_txt = ['Previous reference', 'New reference']

# Create Text Labels
labels = [tk.Label(root, text=f"{rb_txt[i]}") for i in range(2)]

# Create Save Button
save_button = tk.Button(root, text="Save Selected Reference", command=save_text)

# Create Radio Buttons for Text Selection
selected = tk.IntVar()
selected.set(0)  # Default selection

radio_buttons = [tk.Radiobutton(root, text=f"{rb_txt[i]}", variable=selected, value=i) for i in range(2)]

# Grid Layout
for i in range(2):
    labels[i].grid(row=0, column=i, sticky='nsew', padx=10, pady=5)
    text_widgets[i].grid(row=1, column=i, sticky='nsew', padx=10, pady=5)
    radio_buttons[i].grid(row=2, column=i, sticky='nsew', padx=10, pady=5)

save_button.grid(row=3, column=0, columnspan=3, pady=10)

# Configure grid weights for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
bib_update()
