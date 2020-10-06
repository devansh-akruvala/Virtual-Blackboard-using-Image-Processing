#
# pdf = FPDF()
# # imagelist is the list with all image filenames
# images = cv2.imread("img/ball.jpeg")
#
name=input("Enter file name")
path="saves/"
name=name+".docx"
# pdf.add_page()
# cv2.imwrite(path+"a.jpg",images)
# pdf.image(path+"a.jpg", x=None, y=None, w=0, h=0)
# pdf.output(path+name, "F")
# os.remove(path+"a.jpg")
mydoc_read=docx.Document(path+name)

mydoc=docx.Document()

mydoc.add_picture("img/ball.jpeg", width=docx.shared.Inches(5), height=docx.shared.Inches(7))
mydoc.save(path+name)