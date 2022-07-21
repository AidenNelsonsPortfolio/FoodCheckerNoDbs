import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
import pytesseract
from PIL import Image, ImageTk

# Define path to tesseract module
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

# defining main window (tkinter) and its width/height
root = Tk()
root.wm_title("Allergen Checker")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

app_height = 700
app_width = 1000

# storing variables for each checkbox(on and off-checked vals)
milk = tk.StringVar()
treeNuts = tk.StringVar()
gluten = tk.StringVar()
peanuts = tk.StringVar()
soy = tk.StringVar()
shellfish = tk.StringVar()
sesame = tk.StringVar()

root.geometry(
    f'{app_width}x{app_height}+{int(screen_width / 2 - app_width / 2)}+{int(screen_height / 2 - app_height / 2)}')

# within a given allergen, variants to look out for:

treeNutList = ['walnut', 'tree nut', 'almond', 'pecan', 'pistachio',
               'walnuts', 'tree nuts', 'almonds', 'pecans', 'pistachios']

shellfishList = ['crab', 'lobster', 'fish', 'crustacean', 'oyster']

# global variable declaration for labels and vars I want to be able to update easily upon user interaction
image = None
allergensToFind = []
imageLoaded = False
filePicked = False
chooseFile = Button()
goodFood = Label()
badFood = Label()
pickFile = Label()


# Functionality via askopenfile to open and scan for proper file tyles, update GUI accordingly

def open_file():
    # uses module method to open file on computer of the selected types below.
    path = askopenfile(mode='r', filetypes=[('Image Files', ['*jpeg', '*png', '*jpg'])])
    global pathName
    pathName = path.name
    # saves path of the file selected to global variable, then adds button to scan through image file upon user action.
    if path is not None:
        global imageLoaded, image, choose, chooseFile, filePicked
        imageLoaded = True
        if not filePicked:
            chooseFile = Button(root, text="Find Allergens From Label", command=findAllergens)
            chooseFile.pack(pady=10)
        filePicked = True
        choose['text'] = "File Selected"
        choose['background'] = "green"
        pass


# once selected, finding the allergens happens via adding all checked box allergens to array to scan through
def findAllergens():
    if imageLoaded:
        print("Value Extraction Started")

        # destroys labels (global) from last file/errors (if any occurred)
        global goodFood, badFood, pickFile
        goodFood.destroy()
        badFood.destroy()
        pickFile.destroy()

        allergensToFind.clear()

        # adds all allergens that user selected to list of ones to screen for
        if treeNuts.get() == 'find':
            for nut in treeNutList:
                allergensToFind.append(nut)
        if gluten.get() == 'find':
            allergensToFind.append('wheat')
        if peanuts.get() == 'find':
            allergensToFind.append('peanut')
            allergensToFind.append('peanuts')
        if soy.get() == 'find':
            allergensToFind.append('soy')
        if milk.get() == 'find':
            allergensToFind.append('milk')
            allergensToFind.append('dairy')
        if shellfish.get() == 'find':
            for fish in shellfishList:
                allergensToFind.append(fish)
        if sesame.get() == 'find':
            allergensToFind.append('sesame')

        global pathName
        img = Image.open(pathName)
        text = pytesseract.image_to_string(img)

        text = text.lower()
        allergensPresent = []
        temp = ""

        # goes through letter by letter, adding each to a temp var, then, if the word ends,
        # or a whitespace/punctuation character is detected,
        # the allergen will be checked for in the list allergensPresent.
        for letter in text:
            if letter == "," or letter == " " or letter == ".":
                if temp in allergensToFind or temp[:-1] in allergensToFind:
                    if temp not in allergensPresent:
                        allergensPresent.append(temp)
                        print("Contains Allergen Selected : WARNING")
                temp = ""
            else:
                temp = temp + letter

        # adds a label if allergensPresent has a length > 0
        allergenInFood(allergensPresent)

        # else, label is added stating that the food was safe by our judgement, cannot be sure, though.
        if len(allergensPresent) == 0:
            goodFood = Label(root, text="From What We Can See, There Are No Allergens "
                                        "\nYou Selected Present In The Food. "
                                        "\n\nEat With Caution, However, We Cannot Guarantee"
                                        "\n A Safe Eating Experience. "
                                        "\n\n Try to add another, clearer image label picture if you would like!",
                             font='Times 30', bg='green')
            goodFood.pack(pady=10)

        # changes color and text of file choosing button after scanning and warning is completed.
        global choose
        choose['text'] = "Pick Another File?"
        choose['background'] = "white"

        print("done")

    else:
        # Tells user to pick a file IF they have not already/an error occured.
        pickFile = Label(root, text="Must Choose A File Before Finding Its Allergy Contents")
        pickFile.pack(pady=10)


# Warning label if checked allergen is present in food label
def allergenInFood(s):
    if len(s) > 0:
        temp = ""
        # concatenates entirety of allergens detected throughout scanning process
        for word in s:
            temp = word.upper() + " " + temp

        # adds a label to root if there was a bad food detected
        global badFood
        badFood = Label(root, text=f"ALLERGEN SELECTED IS PRESENT IN FOOD "
                                   f"\\n DO NOT CONSUME "
                                   f"\n\n Allergen(s) Present is/are {temp}",
                        font='Times 30', bg='red')
        badFood.pack(pady=10)


# Basic labels and buttons to be able to add to allergens to scan for,
# as well as, for the choose button, begin the file selection process.

Label(root, text="Allergen to Scan For", font='Times 35').pack(pady=10)
ttk.Checkbutton(root, text="Tree Nuts", variable=treeNuts, onvalue='find', offvalue='not').pack(padx=5)
ttk.Checkbutton(root, text="Gluten", variable=gluten, onvalue='find', offvalue='not').pack(padx=5)
ttk.Checkbutton(root, text="Peanuts", variable=peanuts, onvalue='find', offvalue='not').pack(padx=5)
ttk.Checkbutton(root, text="Soy", variable=soy, onvalue='find', offvalue='not').pack(padx=5)
ttk.Checkbutton(root, text="Milk", variable=milk, onvalue='find', offvalue='not').pack(padx=5)
ttk.Checkbutton(root, text="Shellfish", variable=shellfish, onvalue='find', offvalue='not').pack(padx=5)
ttk.Checkbutton(root, text='Sesame', variable=sesame, onvalue='find', offvalue='not').pack(padx=5)
choose = tk.Button(root, text='Choose Ingredients Label File', font='Times 20', command=lambda: (open_file()))
choose.pack(pady=10)

# Begins main loop for the Tkinter window/GUI
root.mainloop()
