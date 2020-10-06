from tkinter import *

root=Tk()
def myfunc():
    print("dsadsadsad")
root.geometry("800x600")

# mymenu=Menu(root)
# mymenu.add_command(label="File",command=myfunc)
# root.config(menu=mymenu)
#

mainMenu=Menu(root)

fileMenu=Menu(mainMenu,tearoff=0)
fileMenu.add_command(label="New",command=myfunc)
fileMenu.add_command(label="open",command=myfunc)
fileMenu.add_separator()
fileMenu.add_command(label="save",command=myfunc)
fileMenu.add_command(label="save as",command=myfunc)
root.config(menu=mainMenu)
mainMenu.add_cascade(label="File",menu=fileMenu)

editmenu=Menu(mainMenu,tearoff=0)
editmenu.add_command(label="Cut",command=myfunc)
editmenu.add_command(label="Copy",command=myfunc)
editmenu.add_command(label="Paste",command=myfunc)
root.config(menu=mainMenu)
mainMenu.add_cascade(label="Edit",menu=editmenu)


root.mainloop()