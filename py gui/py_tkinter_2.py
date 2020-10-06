from  tkinter import *

root = Tk()  ### it is basic gui we will add more stuff on this base

## gui logic

## widthxheight
root.geometry("644x444")
root.title("virtual board")
def hello():
    for i in range(1,11):
        print("hello")

frame1=Frame(root,bg="yellow",borderwidth=8,relief=SUNKEN)
frame1.pack(side=LEFT,fill=Y)
label1=Label(frame1,text="PROJECT",bg="blue",fg="White")
label1.pack()


frame2=Frame(root,bg="grey",borderwidth=8,relief=SUNKEN)
frame2.pack(side=TOP,fill=X)

label2=Label(frame2,text="Welcome to virtual board",bg="blue",fg="White")
label2.pack()


##### buttons
mainframe=Frame(root,bg="grey")
mainframe.pack(side=TOP,fill=Y)
b1=Button(mainframe,text="press me",command=hello)
b1.pack()


root.mainloop()  #### main loop