from tkinter import *



def getvals():
    print(uservalue.get())
    print(passval.get())
root=Tk()
# root.geometry("500x600")
#
# user = Label(root,text="User name")
# password = Label(root,text="Password")
# user.grid()
# password.grid(row=1)
#
# uservalue = StringVar()
# passval = StringVar()
#
# userentry=Entry(root,textvariable=uservalue)
# passentry=Entry(root,textvariable=passval)
#
# userentry.grid(row=0,column=1)
# passentry.grid(row=1,column=1)
#
# Button(text="Submit",command=getvals).grid()

canvas_height=400
canvas_width=800
root.geometry(f"{canvas_width}x{canvas_height}")

can_widget=Canvas(root,width=canvas_width,height=canvas_height)
can_widget.pack()

can_widget.create_line(0,0,800,400)
can_widget.create_text(200,200,text="python")
root.mainloop()