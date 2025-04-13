import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser
import numpy as np
from PIL import Image, ImageTk
import random
from script import generate_word, show_image, random_word
import json, cv2


PAGE_SIZE = (960, 675, 3)
PAGE_GT = np.ones(PAGE_SIZE)*255
PAGE_GEN = np.ones(PAGE_SIZE)*255
META = []


class Metadata:
    def __init__(self, x0, y0, x1, y1, word) -> None:
        self.x0:int = x0
        self.y0:int = y0
        self.x1:int = x1
        self.y1:int = y1

        self.word:str = word

    def __str__(self):
        return f"(x0:{self.x0} y0:{self.y0} x1:{self.x1} y1:{self.y1} word:{self.word})"
    

def replace_pixel_GT(big_image, small_image, position):
    # Get dimensions of small image
    height, width, _ = small_image.shape

    # Get dimensions of big image
    big_height, big_width, _ = big_image.shape

    # Replace pixel
    big_image[position[0]:position[0]+height, position[1]:position[1]+width] = small_image

    return big_image

def replace_pixel_GEN(big_image, small_image, position):
    # Get dimensions of small image
    height, width, _ = small_image.shape

    # Get dimensions of big image
    big_height, big_width, _ = big_image.shape

   # Get the dimensions of the image
    h, w, _ = small_image.shape

    # Traverse through the image array
    for i in range(height):
        for j in range(width):
            # print(small_image[i, j])
            if (small_image[i, j]==[0,0,0]).all():
                big_image[position[0]+i, position[1]+j] = [small_image[i,j,0] ,small_image[i,j,1], small_image[i,j,2]]                #[0,0,0]



    return big_image

def add_word(word:str, ii:int, pos:tuple):
    bgr, filled = generate_word(word, ii, [255,255,255])
    replace_pixel_GEN(PAGE_GEN, bgr, pos)
    replace_pixel_GT(PAGE_GT, filled, pos)
    return bgr.shape


class ImageApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image App")
        self.master.geometry("600x400")
        
        # Create left and right frames
        self.left_frame = tk.Frame(self.master, width=507, height=720)
        self.right_frame = tk.Frame(self.master, width=507, height=720)

        self.top_frame = tk.Frame(self.master)


        # Create picture boxes
        self.pic1 = tk.Label(self.left_frame, text="Generated Picture", padx=10, pady=10)
        self.pic2 = tk.Label(self.right_frame, text="Ground Truth", padx=10, pady=10)
        
        # Create text box
        self.text_box = tk.Text(self.master, height=10, width=50)
        
        # Create button to choose image
        self.add_background = tk.Button(self.top_frame, text="Add Background", command=self.choose_image)
        self.add_solidcolor = tk.Button(self.top_frame, text="Add Solid Color", command=self.choose_color)

      
        # Create button to add text to image
        self.add_text_button = tk.Button(self.top_frame, text="Add Text", command=self.add_word)


        self.save_button = tk.Button(self.top_frame, text="Save Images", command=self.save)
        self.add_para_button = tk.Button(self.top_frame, text="Add Paragraph", command=self.add_para)
        self.add_object_button = tk.Button(self.top_frame, text="Add Drawing Object", command=self.add_object)
        

        # Create input fields for text coordinates and word
        self.x_entry = tk.Entry(self.top_frame, width=5)
        self.y_entry = tk.Entry(self.top_frame, width=5)
        self.word_entry = tk.Entry(self.top_frame, width=20)
        self.strike_entry = tk.Entry(self.top_frame, width=5)

        self.x_label = tk.Label(self.top_frame, text="Line:")
        self.y_label = tk.Label(self.top_frame, text="Space:")
        self.word_label = tk.Label(self.top_frame, text="Word:")
        self.strike_label = tk.Label(self.top_frame, text="Strike:")
        self.psx_label = tk.Label(self.top_frame, text="Start-X:")
        self.psy_label = tk.Label(self.top_frame, text="Start-Y:")
        self.pex_label = tk.Label(self.top_frame, text="Height:")
        self.pey_label = tk.Label(self.top_frame, text="Width:")
        self.psx_entry = tk.Entry(self.top_frame, width=5)
        self.psy_entry = tk.Entry(self.top_frame, width=5)
        self.pex_entry = tk.Entry(self.top_frame, width=5)
        self.pey_entry = tk.Entry(self.top_frame, width=5)

        
        self.top_frame.pack(side="top")
        # Place widgets in the frames and on the master
        self.add_solidcolor.pack(side="left", padx=10, pady=10)
        self.add_background.pack(side="left", padx=10, pady=10)
        self.add_text_button.pack(side="left", padx=10, pady=10)
        self.x_label.pack(side="left")
        self.x_entry.pack(side="left")
        self.y_label.pack(side="left")
        self.y_entry.pack(side="left")
        self.word_label.pack(side="left")
        self.word_entry.pack(side="left")
        self.strike_label.pack(side="left")
        self.strike_entry.pack(side="left")
        self.add_object_button.pack(side="left", padx=10, pady=10)

        
        self.add_para_button.pack(side="left", padx=10, pady=10)
        self.psx_label.pack(side="left")
        self.psx_entry.pack(side="left")
        self.psy_label.pack(side="left")
        self.psy_entry.pack(side="left")
        self.pex_label.pack(side="left")
        self.pex_entry.pack(side="left")
        self.pey_label.pack(side="left")
        self.pey_entry.pack(side="left")
        self.save_button.pack(side="left", padx=10, pady=10)


        
        self.left_frame.pack(side="left", padx=10, pady=10)
        self.right_frame.pack(side="right", padx=10, pady=10)
        self.text_box.pack(side="bottom")

        self.pic1.pack(side="bottom")
        self.pic2.pack(side="bottom")



        # Initialize the PhotoImage objects for both picture boxes
        self.photo1 = None
        self.photo2 = None

    
    def choose_image(self):
        # Allow user to choose an image from their device
        filepath = filedialog.askopenfilename()
        
        # Open the image, resize it to 675x960, and convert it to a Tkinter PhotoImage
        image = Image.open(filepath)
        image = image.resize((675, 960))

        image = np.array(image)
        image = image[:, :, ::-1].copy()

        # Convert the B image to grayscale
        gray = cv2.cvtColor(cv2.convertScaleAbs(PAGE_GT), cv2.COLOR_BGR2GRAY)

        # Create a mask for the black pixels in B
        mask = np.zeros_like(gray)
        mask[gray == 0] = 255

        # Apply the mask to the A image to convert the corresponding pixels to black
        image[mask == 255] = [0, 0, 0]

        global PAGE_GEN
        PAGE_GEN = cv2.convertScaleAbs(image)

        pil_image = Image.fromarray(cv2.cvtColor(cv2.convertScaleAbs(image), cv2.COLOR_BGR2RGB)) 
        pil_image = pil_image.resize((507, 720))
        photo = ImageTk.PhotoImage(pil_image)
        self.pic1.config(image=photo)
        self.photo1 = photo


        pil_image = Image.fromarray(cv2.cvtColor(cv2.convertScaleAbs(PAGE_GT), cv2.COLOR_BGR2RGB)) 
        pil_image = pil_image.resize((507, 720))
        photo = ImageTk.PhotoImage(pil_image)
        self.pic2.config(image=photo)
        self.photo2 = photo
    
    def choose_color(self):
        color = colorchooser.askcolor(title="Choose color")

        global PAGE_GEN
        PAGE_GEN = PAGE_GT.copy()
        PAGE_GEN[np.where((PAGE_GEN==[255,255,255]).all(axis=2))] = color[0]
        
        pil_image = Image.fromarray(cv2.cvtColor(cv2.convertScaleAbs(PAGE_GEN))) 
        pil_image = pil_image.resize((507, 720))
        photo = ImageTk.PhotoImage(pil_image)
        self.pic1.config(image=photo)
        self.photo1 = photo


        pil_image = Image.fromarray(cv2.cvtColor(cv2.convertScaleAbs(PAGE_GT))) 
        pil_image = pil_image.resize((507, 720))
        photo = ImageTk.PhotoImage(pil_image)
        self.pic2.config(image=photo)
        self.photo2 = photo

        print(color)




    def update_screen(self, img_gt:Image, img_new:Image, text:str):

        image1 = img_gt.resize((507, 720))
        image2 = img_new.resize((507, 720))

        photo1 = ImageTk.PhotoImage(image1)
        photo2 = ImageTk.PhotoImage(image2)

        
        # Set the photo as the image for both picture boxes
        self.pic1.config(image=photo2)
        self.pic2.config(image=photo1)
        
        # Keep a reference to the PhotoImage object
        self.photo1 = photo1
        self.photo2 = photo2
        # Clear the current contents of the text widget
        self.text_box.delete("1.0", "end")
        self.text_box.insert("end", text)



    def add_word(self):
        # Get the input values for the text coordinates and word
        x = int(self.x_entry.get())
        y = int(self.y_entry.get())
        word = self.word_entry.get()
        strike = int(self.strike_entry.get())
        dim = add_word(word, strike, (x,y))
        obj = Metadata(x, y, x+dim[0], y+dim[1], word)
        META.append(obj)
        string_list = ""
        for metadata in META:
            string_list += str(metadata) + "\n"

        # show_image("GT",PAGE_GT)
        # show_image("GEN",PAGE_GEN)
        
        pil_image1 = Image.fromarray(cv2.cvtColor(cv2.convertScaleAbs(PAGE_GT), cv2.COLOR_BGR2RGB)) 
        pil_image2 = Image.fromarray(cv2.cvtColor(cv2.convertScaleAbs(PAGE_GEN), cv2.COLOR_BGR2RGB))  


        self.update_screen(pil_image1, pil_image2, string_list)
        
    def add_para(self):
        # Get the input values for the text coordinates and word
        sx = int(self.psx_entry.get())
        sy = int(self.psy_entry.get())
        hx = int(self.pex_entry.get())
        wy = int(self.pey_entry.get())
        ey = sy+hx
        ex = sx+wy
        assert(sx<=ex and sy<=ey)
        lcur = sy
        print('SX= %d',sx)
        print('SY= %d',sy)           
        while lcur<ey:
            wcur=sx
            while wcur<ex:                
                word = random_word()
                strike = min(max(0,random.randint(-5,2)),1)*random.randint(0,6)        
                dim = add_word(word, strike, (lcur,wcur))
                obj = Metadata(wcur, lcur, wcur+dim[1], lcur+dim[0], word)
                META.append(obj)
                string_list = ""
                for metadata in META:
                    string_list += str(metadata) + "\n"

        # show_image("GT",PAGE_GT)
        # show_image("GEN",PAGE_GEN)
        
                pil_image1 = Image.fromarray(cv2.cvtColor(cv2.convertScaleAbs(PAGE_GT), cv2.COLOR_BGR2RGB)) 
                pil_image2 = Image.fromarray(cv2.cvtColor(cv2.convertScaleAbs(PAGE_GEN), cv2.COLOR_BGR2RGB))  
                wcur = wcur + dim[1]
            lcur = lcur + 50
        self.update_screen(pil_image1, pil_image2, string_list)
        
    def add_object(self):
        # Get the input values for the text coordinates and word
        x = int(self.x_entry.get())
        y = int(self.y_entry.get())
        word = self.word_entry.get()
        strike = int(self.strike_entry.get())

        dim = add_word(word, strike, (x,y))

        obj = Metadata(x, y, x+dim[0], y+dim[1], word)
        META.append(obj)
        string_list = ""
        for metadata in META:
            string_list += str(metadata) + "\n"

        # show_image("GT",PAGE_GT)
        # show_image("GEN",PAGE_GEN)
        
        pil_image1 = Image.fromarray(cv2.cvtColor(cv2.convertScaleAbs(PAGE_GT), cv2.COLOR_BGR2RGB)) 
        pil_image2 = Image.fromarray(cv2.cvtColor(cv2.convertScaleAbs(PAGE_GEN), cv2.COLOR_BGR2RGB))  


        self.update_screen(pil_image1, pil_image2, string_list)


    def save(self):

        name = simpledialog.askstring(title="Name", prompt="name")
        cv2.imwrite(name+"_gt.jpg", PAGE_GT)
        cv2.imwrite(name+".jpg", PAGE_GEN)

        json_str = json.dumps([obj.__dict__ for obj in META])

        with open(name+'_meta.json', 'w') as f:
            f.write(json_str)



        
        

        
root = tk.Tk()
app = ImageApp(root)
root.mainloop()