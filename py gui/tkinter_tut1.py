from  tkinter import *

tk_root = Tk()  ### it is basic gui we will add more stuff on this base

## gui logic

## widthxheight
tk_root.geometry("644x444")
tk_root.title("virtual board")
### min sizelimit
## width,height
tk_root.minsize(200,100)


### max sizelimit
## width,height
##tk_root.maxsize(1000,1000)

##### label attributes bg="red",fg="white",padx="40",pady="80",font=("comicsansms",19,"bold"),borderwidth=4,relief=SUNKEN)

lbl1=Label(text='''hiiiii asdasdlasdjash ijasdash ijviawjv wpofpsdosdo opd \n
                jadopjasdpvpsdvjpsdjvopsdjvopsadjvosdpjvpodajvp
                /nsaasdlasdlasdasdcvcmvxcnsdajfhsdainvsdlk d'''
           , bg="red",fg="white",padx="40",pady="80",font=("comicsansms",10,"bold"),borderwidth=4,relief=SUNKEN)

#### pack attributes 1. anchor=NW NE etc ,side = top bottom etc, fill=X or Y  streatch acc to size of screen padx and pad y)

lbl1.pack(side=LEFT,anchor=NE,fill=Y,padx=30,pady=40)

tk_root.mainloop()  #### main loop