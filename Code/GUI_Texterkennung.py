import tkinter as tk
from tkinter import messagebox, font
from tkinter import filedialog, ttk
from PIL import Image, ImageTk,ImageDraw

import os
import shutil
from pdf2image import convert_from_path
from classes import PlaceholderEntry
import numpy as np

import tqdm
import re
from classes import ImageAnalysis

class TextRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Recognition App")
        self.file_path = None
        self.jpg_files = []
        self.user = os.getlogin()
        self.page_number = 0
        self.setup_section()

    def setup_section(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid(padx=10, pady=10)

        self.file_type = tk.StringVar(value="pdf")

        tk.Label(self.frame, text="Book Name:").grid(row=0, column=0)
        
        self.book_name_var = tk.StringVar()
        self.book_name_entry = tk.Entry(self.frame, textvariable=self.book_name_var)
        self.book_name_entry.grid(row=0, column=1)
        
        self.search_button = tk.Button(self.frame, text="Search", command=self.search_book)
        self.search_button.grid(row=0, column=2, padx= 5)

        self.upload_button = tk.Button(self.frame, text="Upload File", command=self.upload_file)
        self.upload_button.grid(row=1, column=0, pady=5)

        self.convert_button = tk.Button(self.frame, text="Convert PDF to JPG", command=self.convert_pdf_to_jpg)
        self.convert_button.grid(row=1, column=1, pady=5)
        
        self.delete_button = tk.Button(self.frame, text="Delete Book", command=self.delete_book)
        self.delete_button.grid(row=1, column=2, pady=5)

        self.upload_check = tk.Label(self.frame, text="", fg="green")
        self.upload_check.grid(row=2, column=0, columnspan=3, pady=5)
        
        self.process_type = tk.StringVar(value="specific_page")
        tk.Radiobutton(self.frame, text="Specific Page", variable=self.process_type, value="specific_page", command=self.toggle_page_number).grid(row=4, column=1)
        tk.Radiobutton(self.frame, text="Whole Book", variable=self.process_type, value="whole_book", command=self.toggle_page_number).grid(row=4, column=2)

        tk.Label(self.frame, text="Process Book:").grid(row=4, column=0)
        
        self.max_page_label = tk.Label(self.frame, text=f"max ({self.page_number})")
        self.max_page_label.grid(row=5,column=0)
        self.page_number_entry = PlaceholderEntry(self.frame,placeholder="1 or 1,2,10 or 1-20")
        self.page_number_entry.grid(row=5, column=0, columnspan=3, pady=5)
        
        self.process_button = tk.Button(self.frame, text="Process", command=self.process_file_it)
        self.process_button.grid(row=5, column=2, columnspan=2, pady=5)
        
        self.process_check = tk.Label(self.frame, text="", fg="green")
        self.process_check.grid(row=6, column=0, columnspan=3, pady=5)
        

        tk.Label(self.frame, text="Correct Book:").grid(row=8, column=0)
        self.starting_number_entry = PlaceholderEntry(self.frame,placeholder="Starting Page Number")
        self.starting_number_entry.grid(row=8, column=1, pady=5)
        
        self.check_button = tk.Button(self.frame, text="Start", command=self.correct_file)
        self.check_button.grid(row=8, column=2, pady=5)
        
        self.correct_check = tk.Label(self.frame, text="", fg="green")
        self.correct_check.grid(row=9, column=0, columnspan=3, pady=5)
        
        
        self.image_index = 1
        self.word_index = 1
        self.current_paragraph = 0
        
    
    def delete_book(self):
        self.bookname = self.book_name_entry.get().strip()
        destination_folder = 'C:/Users/' + self.user + '/Texterkennung/PDF_Files/' + str(self.bookname)  # Replace with the desired new folder path
        if os.path.exists(destination_folder):
            #remove data from page
            x = self.delete_button.winfo_rootx()
            y = self.delete_button.winfo_rooty()
            
            confirm_window = tk.Toplevel(root)
            confirm_window.title("Confirmation")
            confirm_window.geometry(f"+{x}+{y}")
        
            msg = tk.Label(confirm_window, text="Deletion leads to total data loss. Continue?")
            msg.pack(pady=20)
        
            button_frame = tk.Frame(confirm_window)
            button_frame.pack(pady=20)
            
            def on_yes():
                confirm_window.destroy()
                
                PDF_folder = 'C:/Users/' + self.user + '/Texterkennung/PDF_Files/' + str(self.bookname)
                JPG_folder = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname)
                Text_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname)
                Text_Numpy_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Numpy_Files/' + str(self.bookname)
                Mask_folder = 'C:/Users/' + self.user + '/Texterkennung/Mask_Files/' + str(self.bookname)
                Position_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname)
                Position_Words_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Words_Files/' + str(self.bookname)
                
                    
                if(os.path.exists(PDF_folder)):
                    try:
                        shutil.rmtree(PDF_folder)
                    except:
                        pass
                        
                        
                if(os.path.exists(JPG_folder)):
                    try:
                        shutil.rmtree(JPG_folder)
                    except:
                        pass
                        
                if(os.path.exists(Text_folder)):
                    try:
                        shutil.rmtree(Text_folder)
                    except:
                        pass
                    
                if(os.path.exists(Text_Numpy_folder)):
                    try:
                        shutil.rmtree(Text_Numpy_folder)
                    except:
                        pass
                        
                if(os.path.exists(Mask_folder)):
                    try:
                        shutil.rmtree(Mask_folder)
                    except:
                        pass
                        
                if(os.path.exists(Position_folder)):
                    try:
                        shutil.rmtree(Position_folder)
                    except:
                        pass
                
                if(os.path.exists(Position_Words_folder)):
                    try:
                        shutil.rmtree(Position_Words_folder)
                    except:
                        pass
                        
                    
                    
                self.upload_check.config(text="File deleted✔", fg="green")
        
                
                
        
            def on_no():
                confirm_window.destroy()
            
            yes_button = tk.Button(button_frame, text="Yes", command=on_yes)
            yes_button.pack(side="left", padx=5)
        
            no_button = tk.Button(button_frame, text="No", command=on_no)
            no_button.pack(side="left", padx=5)
        
            confirm_window.grab_set() 
        
        else:
            self.upload_check.config(text="No book with that name❌", fg="red")
            
        
                
                
    
    def search_book(self):
        folder_selected = filedialog.askdirectory()

        if folder_selected:
            last_folder_name = os.path.basename(folder_selected)
            self.book_name_var.set(last_folder_name)
            self.bookname = last_folder_name
            self.load_image_paths()
            self.max_page_label.config(text=f"max ({self.page_number})")

    def toggle_page_number(self):
        if self.process_type.get() == "specific_page":
            self.page_number_entry.grid()
        else:
            self.page_number_entry.grid_remove()

    def upload_file(self):
        self.bookname = self.book_name_entry.get().strip()
        chars_to_check = ['/','(',')','=','?','&','%','$','§','!',':',';',',','#','+','*','~']
        if(self.bookname==""):
            self.upload_check.config(text="Give valid name❌", fg="red")
        elif(' ' in self.bookname):
            self.upload_check.config(text="Empty space detected, use _ instead❌", fg="red")
        elif('.' in self.bookname):
            self.upload_check.config(text="Dot detected, use _ instead❌", fg="red")
        elif any(char in self.bookname for char in chars_to_check):
            self.upload_check.config(text="Special case detected, use _ instead❌", fg="red")
        else:
            destination_folder = 'C:/Users/' + self.user + '/Texterkennung/PDF_Files/' + str(self.bookname)  # Replace with the desired new folder path
            if os.path.exists(destination_folder):
                
                #remove data from page
                x = self.upload_button.winfo_rootx()
                y = self.upload_button.winfo_rooty()
                
                confirm_window = tk.Toplevel(root)
                confirm_window.title("Confirmation")
                confirm_window.geometry(f"+{x}+{y}")
            
                msg = tk.Label(confirm_window, text="File already exists. Replacing it leads to data loss. Continue?")
                msg.pack(pady=20)
            
                button_frame = tk.Frame(confirm_window)
                button_frame.pack(pady=20)
                
                def on_yes():
                    confirm_window.destroy()
                    
                    file_path = filedialog.askopenfilename()
                    if file_path:
                        PDF_folder = 'C:/Users/' + self.user + '/Texterkennung/PDF_Files/' + str(self.bookname)
                        JPG_folder = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname)
                        Text_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname)
                        Text_Numpy_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Numpy_Files/' + str(self.bookname)
                        Mask_folder = 'C:/Users/' + self.user + '/Texterkennung/Mask_Files/' + str(self.bookname)
                        Position_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname)
                        Position_Words_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Words_Files/' + str(self.bookname)
                        
                        for filename in os.listdir(PDF_folder):
                            whole_path = os.path.join(PDF_folder, filename)
                            try:
                                os.remove(whole_path)
                            except:
                                pass
                            
                            
                        if(os.path.exists(JPG_folder)):
                            try:
                                shutil.rmtree(JPG_folder)
                            except:
                                pass
                            
                        if(os.path.exists(Text_folder)):
                            try:
                                shutil.rmtree(Text_folder)
                            except:
                                pass
                        
                        if(os.path.exists(Text_Numpy_folder)):
                            try:
                                shutil.rmtree(Text_Numpy_folder)
                            except:
                                pass
                            
                        if(os.path.exists(Mask_folder)):
                            try:
                                shutil.rmtree(Mask_folder)
                            except:
                                pass
                            
                        if(os.path.exists(Position_folder)):
                            try:
                                shutil.rmtree(Position_folder)
                            except:
                                pass
                        
                        if(os.path.exists(Position_Words_folder)):
                            try:
                                shutil.rmtree(Position_Words_folder)
                            except:
                                pass
                            
                        
                        
                        self.file_path = file_path
                        self.upload_check.config(text="File overwritten✔", fg="green")
            
                        
                        os.makedirs(destination_folder, exist_ok=True)
                        
                        filename = os.path.basename(self.file_path)
                        
                        # Construct the destination path with the original filename
                        destination_path = os.path.join(destination_folder, filename)
                        
                        # Copy the file to the destination folder
                        shutil.copy(self.file_path, destination_path)
                        print(f"File uploaded: {file_path}")
                        
                        
                        self.load_image_paths()
                        self.max_page_label.config(text=f"max ({self.page_number})")
                    else:
                        self.upload_check.config(text="No data overwritten✔", fg="green")
                        self.load_image_paths()
                        self.max_page_label.config(text=f"max ({self.page_number})")
                    
            
                def on_no():
                    confirm_window.destroy()
                
                yes_button = tk.Button(button_frame, text="Yes", command=on_yes)
                yes_button.pack(side="left", padx=5)
            
                no_button = tk.Button(button_frame, text="No", command=on_no)
                no_button.pack(side="left", padx=5)
            
                confirm_window.grab_set() 
                
                
            else:
                file_path = filedialog.askopenfilename()
                if file_path:
                    self.file_path = file_path
                    self.upload_check.config(text="New file uploaded✔", fg="green")
        
                    
                    os.makedirs(destination_folder, exist_ok=True)
                    
                    filename = os.path.basename(self.file_path)
                    
                    # Construct the destination path with the original filename
                    destination_path = os.path.join(destination_folder, filename)
                    
                    # Copy the file to the destination folder
                    shutil.copy(self.file_path, destination_path)
                    print(f"File uploaded: {file_path}")
                    
                    
                    self.load_image_paths()
                    self.max_page_label.config(text=f"max ({self.page_number})")
                
            
            
            

    def convert_pdf_to_jpg(self):
        self.bookname = self.book_name_entry.get().strip()
        PDF_folder = 'C:/Users/' + self.user + '/Texterkennung/PDF_Files/' + str(self.bookname)
        if(self.bookname==""):
            self.upload_check.config(text="Give valid name❌", fg="red")
        elif(' ' in self.bookname):
            self.upload_check.config(text="Empty space detected, use _ instead❌", fg="red")
        elif('.' in self.bookname):
            self.upload_check.config(text="Dot detected, use _ instead❌", fg="red")
        elif(os.path.exists(PDF_folder)==False):
            self.upload_check.config(text="No Pdf with this name detected❌", fg="red")
        else:
            jpg_folder = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname)
            if(os.path.exists(jpg_folder) and len(os.listdir(jpg_folder))!=0):
                self.upload_check.config(text="PDF already converted to JPG✔", fg="green")
                self.load_image_paths()
                self.max_page_label.config(text=f"max ({self.page_number})")
            else:
                pdf_files = []
                for root, dirs, files in os.walk(PDF_folder):
                    for file in files:
                        if file.endswith('.pdf'):
                            pdf_files.append(os.path.join(root, file))
                
                if(len(pdf_files) == 0):
                    self.upload_check.config(text="No PDF File in the direcory detected❌", fg="red")
                elif(len(pdf_files) > 1):
                    self.upload_check.config(text="More than one PDF File in the direcory detected❌", fg="red")
                else:
                    self.progress_jpg = ttk.Progressbar(self.frame, orient="horizontal", length=300, mode="determinate")
                    self.progress_jpg.grid(row=2, column=0, columnspan=3, pady=5)
                    os.makedirs(jpg_folder , exist_ok=True)
                    
                    pdfs = pdf_files[0]
                    print(pdfs)
                    
                    pages = convert_from_path(pdfs, 300,thread_count = 8)
                    i = 1
                    for page in pages:
                        image_name = jpg_folder + "/" + "Page_" + str(i) + ".jpg"
                        page.save(image_name, "JPEG")
                        i = i+1
                        self.progress_jpg["value"] = (i+1)*(100/len(pages))
                        self.progress_jpg.update()
                    
                    self.progress_jpg.grid_forget()
                    self.upload_check.config(text="PDF successfully converted to JPG✔")
                    self.load_image_paths()
                    self.max_page_label.config(text=f"max ({self.page_number})")
                    
                    #TODO: make page mask to save wheather page is processed)
            
    #---------------------------------------------------------------------------------------------------------
    # Texterkennung
    #---------------------------------------------------------------------------------------------------------
    def process_file(self):
        print("Resulting files to process " +str(self.resulting_files_to_process))
        
        #create instance of Image Analysis Class
        for i in range(len(self.resulting_files_to_process)):
            print("PAGE ANALYZED " +str(self.resulting_files_to_process[i]))
            try:
                image_path = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname) +'/' + f"Page_{self.resulting_files_to_process[i]}.jpg"
            except:
                self.process_check.config(text="Error with JPG path❌", fg="red")
            
            try:
                book_page_dir_text = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + '/' +f"Page_{self.resulting_files_to_process[i]}"
                if(os.path.exists(book_page_dir_text)):
                    self.process_check.config(text="Page already analyzed✔", fg="green")
                else:
                    Instance_Image_Analysis = ImageAnalysis(image_path)
                    #process file with text recognition
                    Instance_Image_Analysis.process()
                    #apply text correction software
                    Instance_Image_Analysis.run_correction()
                
                
                    os.makedirs(book_page_dir_text, exist_ok=True)
                    
                    book_page_dir_mask = 'C:/Users/' + self.user + '/Texterkennung/Mask_Files/' + str(self.bookname) + '/' +f"Page_{self.resulting_files_to_process[i]}"
                    book_page_dir_positions = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + '/' +f"Page_{self.resulting_files_to_process[i]}"
                    book_page_dir_text_numpy = 'C:/Users/' + self.user + '/Texterkennung/Text_Numpy_Files/' + str(self.bookname) + '/' +f"Page_{self.resulting_files_to_process[i]}"
                    book_page_dir_positions_words = 'C:/Users/' + self.user + '/Texterkennung/Position_Words_Files/' + str(self.bookname) + '/' +f"Page_{self.resulting_files_to_process[i]}"
                    os.makedirs(book_page_dir_mask, exist_ok=True)
                    os.makedirs(book_page_dir_positions, exist_ok=True)
                    os.makedirs(book_page_dir_text_numpy, exist_ok = True)
                    os.makedirs(book_page_dir_positions_words, exist_ok = True)
                    
                    
                    
                    with open(os.path.join(book_page_dir_text, 'All_Paragraphs.txt'), 'w', encoding='utf-8', errors='ignore') as big_file:
                        # Iterate over the list and save each sequence to a separate .txt file
                        for j, sequence in enumerate(Instance_Image_Analysis.sorted_text):
                            filename = os.path.join(book_page_dir_text, f'Paragraph_{j+1}.txt')
                            with open(filename, 'w', encoding='utf-8', errors='ignore') as file:
                                file.write(' '.join(sequence))
                                
                            big_file.write(' '.join(sequence))
                            # Optionally, add a separator between paragraphs if needed
                            big_file.write('\n\n')  # Adds two newlines as a separator between paragraphs
                            
                            filename_mask = os.path.join(book_page_dir_mask, f'Paragraph_{j+1}')
                            filename_pos  = os.path.join(book_page_dir_positions, f'Paragraph_{j+1}')
                            filename_text_numpy = os.path.join(book_page_dir_text_numpy, f'Paragraph_{j+1}')
                            
                            
                        
                            np.save(filename_mask, Instance_Image_Analysis.sorted_mask[j])
                            np.save(filename_pos, Instance_Image_Analysis.sorted_paragraph_positions[j])
                            np.save(filename_text_numpy, sequence)
                            
                                                        
                            book_page_dir_positions_words_paragraph = 'C:/Users/' + self.user + '/Texterkennung/Position_Words_Files/' + str(self.bookname) + '/' +f"Page_{self.resulting_files_to_process[i]}" +'/'+f'Paragraph_{j+1}'
                            os.makedirs(book_page_dir_positions_words_paragraph, exist_ok=True)
                            #sort resulting positions in different arrays to make them homogeneous
                            
                            filename_positions_words_x = os.path.join(book_page_dir_positions_words_paragraph, 'x')
                            filename_positions_words_y = os.path.join(book_page_dir_positions_words_paragraph, 'y')
                            filename_positions_words_dx = os.path.join(book_page_dir_positions_words_paragraph, 'dx')
                            filename_positions_words_dy = os.path.join(book_page_dir_positions_words_paragraph, 'dy')
                                
                            data_x = []
                            data_y = []
                            data_dx = []
                            data_dy = []
                            for k in range(len(Instance_Image_Analysis.sorted_words_positions[j])):
                                data_x.append(Instance_Image_Analysis.sorted_words_positions[j][k][0])
                                data_y.append(Instance_Image_Analysis.sorted_words_positions[j][k][1])
                                data_dx.append(Instance_Image_Analysis.sorted_words_positions[j][k][2])
                                data_dy.append(Instance_Image_Analysis.sorted_words_positions[j][k][3])
                                
                            np.save(filename_positions_words_x, np.array(data_x))
                            np.save(filename_positions_words_y, np.array(data_y))
                            np.save(filename_positions_words_dx, np.array(data_dx))
                            np.save(filename_positions_words_dy, np.array(data_dy))
                #create Text File with generated Text
            except Exception() as err:
                self.process_check.config(text=f"Error in Image Class: {err}❌", fg="red")
                
                
    def process_file_it(self):
        self.bookname = self.book_name_entry.get().strip()
        chars_to_check = ['/','(',')','=','?','&','%','$','§','!',':',';',',','#','+','*','~']
        PDF_folder = 'C:/Users/' + self.user + '/Texterkennung/PDF_Files/' + str(self.bookname)
        JPG_folder = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname)
        if(self.bookname==""):
            self.process_check.config(text="Give valid name❌", fg="red")
        elif(' ' in self.bookname):
            self.process_check.config(text="Empty space detected, use _ instead❌", fg="red")
        elif('.' in self.bookname):
            self.process_check.config(text="Dot detected, use _ instead❌", fg="red")
        elif any(char in self.bookname for char in chars_to_check):
            self.process_check.config(text="Special case detected, use _ instead❌", fg="red")
        elif(os.path.exists(PDF_folder)==False):
            self.process_check.config(text="No PDF with this name detected. Please upload PDF or check name❌", fg="red")
        elif(os.path.exists(JPG_folder)==False):
            self.process_check.config(text="No JPG with this name detected. Please convert PDF or check name❌", fg="red")
        else:
            self.load_image_paths()
            self.text_count = self.load_text_content()
            if(self.process_type.get()=="specific_page"):
                print("specific page")
                self.resulting_files_to_process, successful = self.parse_page_numbers()
                self.resulting_files_to_process = np.array(self.resulting_files_to_process)
                if(successful == True):
                    book_text_dir = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname)
                    os.makedirs(book_text_dir, exist_ok=True)
                    
                    self.pages_to_overwrite = []
                    for i in range(len(self.resulting_files_to_process)):
                        book_page_dir_text = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + '/' +f"Page_{self.resulting_files_to_process[i]}"
                        if(os.path.exists(book_page_dir_text)):
                            self.pages_to_overwrite.append(self.resulting_files_to_process[i])
                    
                    if(len(self.pages_to_overwrite)==0):
                        self.process_file()
                    else:
                        #pages already analyzed
                        x = self.process_button.winfo_rootx()
                        y = self.process_button.winfo_rooty()
                        
                        confirm_window = tk.Toplevel(root)
                        confirm_window.title("Confirmation")
                        confirm_window.geometry(f"+{x}+{y}")
                    
                        msg = tk.Label(confirm_window, text=str(len(self.pages_to_overwrite)) +" pages already processed. Overwrite?")
                        msg.pack(pady=10)
                    
                        button_frame = tk.Frame(confirm_window)
                        button_frame.pack(pady=10)
                        
                        def on_yes():
                            
                            confirm_window.destroy()
                            for i in range(len(self.pages_to_overwrite)):
                                txt_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + '/' + f"Page_{self.pages_to_overwrite[i]}"
                                mask_folder = 'C:/Users/' + self.user + '/Texterkennung/Mask_Files/' + str(self.bookname) + '/' + f"Page_{self.pages_to_overwrite[i]}"
                                positions_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + '/' + f"Page_{self.pages_to_overwrite[i]}"
                                text_numpy_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Numpy_Files/' + str(self.bookname) + '/' + f"Page_{self.pages_to_overwrite[i]}"
                                positions_words_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Words_Files/' + str(self.bookname) + '/' + f"Page_{self.pages_to_overwrite[i]}"

                                if(os.path.exists(txt_folder)):
                                    try:
                                        shutil.rmtree(txt_folder)
                                    except:
                                        pass
                                
                                if(os.path.exists(mask_folder)):
                                    try:
                                        shutil.rmtree(mask_folder)
                                    except:
                                        pass
                                
                                if(os.path.exists(positions_folder)):
                                    try:
                                        shutil.rmtree(positions_folder)
                                    except:
                                        pass
                                
                                if(os.path.exists(text_numpy_folder)):
                                    try:
                                        shutil.rmtree(text_numpy_folder)
                                    except:
                                        pass
                            
                                if(os.path.exists(positions_words_folder)):
                                    try:
                                        shutil.rmtree(positions_words_folder)
                                    except:
                                        pass
                            print("FILES REMOVED")
                            self.process_file()
                            
                    
                        def on_no():
                            new_files_to_process = []
                            self.pages_to_overwrite = np.array(self.pages_to_overwrite)
                            for i in range(len(self.resulting_files_to_process)):
                                if(np.isin(self.resulting_files_to_process[i],self.pages_to_overwrite) == False):
                                    new_files_to_process.append(self.resulting_files_to_process[i])
                            
                            self.resulting_files_to_process = new_files_to_process
                            confirm_window.destroy()
                            self.process_file()
                        
                        yes_button = tk.Button(button_frame, text="Yes", command=on_yes)
                        yes_button.pack(side="left", padx=5)
                    
                        no_button = tk.Button(button_frame, text="No", command=on_no)
                        no_button.pack(side="left", padx=5)
                    
                        confirm_window.grab_set() 
                        
                    
            else:
                print("whole book")
                book_text_dir = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname)
                os.makedirs(book_text_dir, exist_ok=True)
                
                self.load_image_paths()
                self.resulting_files_to_process = np.arange(1,self.page_number+1)
                
                self.pages_to_overwrite = []
                for i in range(len(self.resulting_files_to_process)):
                    book_page_dir_text = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + '/' +f"Page_{self.resulting_files_to_process[i]}"
                    if(os.path.exists(book_page_dir_text)):
                        self.pages_to_overwrite.append(self.resulting_files_to_process[i])
                
                
                if(len(self.pages_to_overwrite)==0):
                    self.process_file()
                if(len(self.pages_to_overwrite)!=0):
                    #pages already analyzed
                    x = self.process_button.winfo_rootx()
                    y = self.process_button.winfo_rooty()
                    
                    confirm_window = tk.Toplevel(root)
                    confirm_window.title("Confirmation")
                    confirm_window.geometry(f"+{x}+{y}")
                
                    msg = tk.Label(confirm_window, text=str(len(self.pages_to_overwrite)) +" pages already processed. Overwrite?")
                    msg.pack(pady=10)
                
                    button_frame = tk.Frame(confirm_window)
                    button_frame.pack(pady=10)
                    
                    def on_yes():
                        
                        confirm_window.destroy()
                        for i in range(len(self.pages_to_overwrite)):
                            txt_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + '/' + f"Page_{self.pages_to_overwrite[i]}"
                            mask_folder = 'C:/Users/' + self.user + '/Texterkennung/Mask_Files/' + str(self.bookname) + '/' + f"Page_{self.pages_to_overwrite[i]}"
                            positions_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + '/' + f"Page_{self.pages_to_overwrite[i]}"
                            text_numpy_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Numpy_Files/' + str(self.bookname) + '/' + f"Page_{self.pages_to_overwrite[i]}"
                            positions_words_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Words_Files/' + str(self.bookname) + '/' + f"Page_{self.pages_to_overwrite[i]}"

                            
                            if(os.path.exists(txt_folder)):
                                try:
                                    shutil.rmtree(txt_folder)
                                except:
                                    pass
                            
                            if(os.path.exists(mask_folder)):
                                try:
                                    shutil.rmtree(mask_folder)
                                except:
                                    pass
                            
                            if(os.path.exists(positions_folder)):
                                try:
                                    shutil.rmtree(positions_folder)
                                except:
                                    pass
                            
                            if(os.path.exists(text_numpy_folder)):
                                try:
                                    shutil.rmtree(text_numpy_folder)
                                except:
                                    pass
                    
                            if(os.path.exists(positions_words_folder)):
                                try:
                                    shutil.rmtree(positions_words_folder)
                                except:
                                    pass
                        
                        print("FILES REMOVED")
                        self.process_file()
                    
                    def on_no():
                        new_files_to_process = []
                        self.pages_to_overwrite = np.array(self.pages_to_overwrite)
                        for i in range(len(self.resulting_files_to_process)):
                            if(np.isin(self.resulting_files_to_process[i],self.pages_to_overwrite) == False):
                                new_files_to_process.append(self.resulting_files_to_process[i])
                        
                        self.resulting_files_to_process = new_files_to_process
                        confirm_window.destroy()
                        self.process_file()
                    
                    yes_button = tk.Button(button_frame, text="Yes", command=on_yes)
                    yes_button.pack(side="left", padx=5)
                
                    no_button = tk.Button(button_frame, text="No", command=on_no)
                    no_button.pack(side="left", padx=5)
                
                    confirm_window.grab_set() 
                
                
                
            
    def parse_page_numbers(self):
        if(self.page_number_entry.get() == "1 or 1,2,10 or 1-20" ):
           self.process_check.config(text="No page number or range inserted❌", fg="red")
           return [], False
        
        # Clean the input string by removing spaces and splitting by commas
        input_string = self.page_number_entry.get().replace(" ", "")
        parts = input_string.split(',')
        
            
        result = []
        for part in parts:
            if '-' in part:
                # Handle range like '1-20'
                start, end = part.split('-')
                try:
                    start = int(start)
                    end = int(end)
                    if start > end:
                        self.process_check.config(text="Start number cannot be greater than end number in a range❌", fg="red")
                        return [], False
                    result.extend(range(start, end + 1))
                except ValueError:
                    self.process_check.config(text=f"Invalid range format: {part}❌", fg="red")
                    return [], False
            else:
                # Handle single number or invalid input
                try:
                    number = int(part)
                    result.append(number)
                except ValueError:
                    self.process_check.config(text=f"Invalid number format: {part}❌", fg="red")
                    return [], False

        # Remove duplicates and sort the result
        result = sorted(list(set(result)))
        if(max(result)> self.page_number):
            self.process_check.config(text="Page number higher than existing book❌", fg="red")
            return [], False
        return result, True
    
        
    #---------------------------------------------------------------------------------------------------------
    # Text Korrektur 
    #---------------------------------------------------------------------------------------------------------
    
        
    def correct_file(self):
        self.bookname = self.book_name_entry.get().strip()
        PDF_folder = 'C:/Users/' + self.user + '/Texterkennung/PDF_Files/' + str(self.bookname)
        JPG_folder = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname)
        Text_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname)
        chars_to_check = ['/','(',')','=','?','&','%','$','§','!',':',';',',','#','+','*','~']
        if(self.bookname==""):
            self.correct_check.config(text="Give valid name❌", fg="red")
        elif(' ' in self.bookname):
            self.correct_check.config(text="Empty space detected, use _ instead❌", fg="red")
        elif('.' in self.bookname):
            self.correct_check.config(text="Dot detected, use _ instead❌", fg="red")
        elif any(char in self.bookname for char in chars_to_check):
            self.correct_check.config(text="Special case detected, use _ instead❌", fg="red")
        elif(os.path.exists(PDF_folder)==False):
            self.correct_check.config(text="No PDF with this name detected. Please upload PDF or check name❌", fg="red")
        elif(os.path.exists(JPG_folder)==False):
            self.correct_check.config(text="No JPG with this name detected. Please convert PDF or check name❌", fg="red")
        elif(os.path.exists(Text_folder)==False):
            self.correct_check.config(text="No Text Files with this name detected. Please Process first or check name❌", fg="red")
        else:
            starting_page = self.starting_number_entry.get().strip()
            if(starting_page=="Starting Page Number"):
                
                self.setup_text_correction_window()
            else:
                try:
                    test = int(starting_page)
                    self.setup_text_correction_window(int(starting_page))
                except:
                    self.setup_text_correction_window()
                
            
                    

    def setup_text_correction_window(self,starting_page=False):
        self.viewer = tk.Toplevel(self.root)  # Changed self.master to self.root
        self.viewer.title("Image and Text Viewer")

        # Initialize index trackers
        self.image_index = 1
        self.word_index = 1

        # Load initial paths for images and text
        self.load_image_paths()
        self.text_count = self.load_text_content()

        # Display Image
        
        self.image_label = tk.Label(self.viewer)
        self.image_label.grid(row=0, column=0, rowspan=4)
        
    
        if(starting_page == False):
            self.image_index = 1
            flag = False
            while(flag == False and self.image_index <= self.page_number):
                text_path = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}"
                if(os.path.exists(text_path)==False):
                    self.image_index += 1
                else:
                    flag = True
        else:
            self.image_index = starting_page
            text_path = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}"
            if(os.path.exists(text_path)==False):
                #load first possible image
                self.image_index = 1
                flag = False
                while(flag == False and self.image_index <= self.page_number):
                    text_path = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}"
                    if(os.path.exists(text_path)==False):
                        self.image_index += 1
                    else:
                        flag = True
        
        self.update_image()
        
        text_path = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}"
        # Filter out entries that are not files
        self.find_paragraph_count()

        # Image Navigation Buttons
        self.prev_img_btn = tk.Button(self.viewer, text="<", command=self.prev_image)
        self.prev_img_btn.grid(row=4, column=0, sticky='w')

        self.next_img_btn = tk.Button(self.viewer, text=">", command=self.next_image)
        self.next_img_btn.grid(row=4, column=0, sticky='e')

        # Display Text
        self.text_display = tk.Text(self.viewer, width=80, height=40)
        self.text_display.grid(row=0, column=1, rowspan=4)
        self.setup_text_display()

        # Text Navigation Buttons
        self.prev_paragraph_btn = tk.Button(self.viewer, text="<", command=self.prev_paragraph)
        self.prev_paragraph_btn.grid(row=4, column=1, sticky='w')

        self.next_paragraph_btn = tk.Button(self.viewer, text=">", command=self.next_paragraph)
        self.next_paragraph_btn.grid(row=4, column=1, sticky='e')

        # Text Input Field
        self.text_input = tk.Entry(self.viewer, width=50)
        self.text_input.grid(row=5, column=1)
        
        # Bind the Enter key to the on_enter method
        self.text_input.bind('<Return>', lambda event: self.on_enter())

        #button for empty page
        self.empty_page_btn = tk.Button(self.viewer, text="Page Empty", command=self.empty_page)
        self.empty_page_btn.grid(row=1, column=2)
        
        #button for empty paragraph
        self.empty_paragraph_btn = tk.Button(self.viewer, text="Paragraph Empty", command=self.empty_paragraph)
        self.empty_paragraph_btn.grid(row=2, column=2)
        
        #button for combining paragraphs
        self.combine_paragraphs_btn = tk.Button(self.viewer, text="Combine Paragraphs", command=self.combine_paragraphs)
        self.combine_paragraphs_btn.grid(row=3, column=2)
        
        self.page_deletable()
        self.paragraph_deletable()
        self.text_correction_necessary()
    
    def combine_paragraphs(self):
        pass
        
    def on_enter(self):
        print(self.current_word_index)
        book_page_dir_mask = 'C:/Users/' + self.user + '/Texterkennung/Mask_Files/' + str(self.bookname) + '/' +f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}.npy"
        book_page_dir_text = 'C:/Users/' + self.user + '/Texterkennung/Text_Numpy_Files/' + str(self.bookname) + '/' +f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}.npy"
        image_path = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}.jpg"
        
        corrected_word = self.text_input.get()
        if(corrected_word != ""):
            self.current_mask[self.current_word_index] = 0
            self.current_text[self.current_word_index] = corrected_word
            np.save(book_page_dir_mask, self.current_mask)
            np.save(book_page_dir_text, self.current_text)
        else:
            self.current_mask = np.delete(self.current_mask, self.current_word_index)
            self.current_text =np.delete(self.current_text, self.current_word_index)
            self.text_border_x = np.delete(self.text_border_x, self.current_word_index)
            self.text_border_y = np.delete(self.text_border_y, self.current_word_index)
            self.text_border_dx = np.delete(self.text_border_dx, self.current_word_index)
            self.text_border_dy = np.delete(self.text_border_dy, self.current_word_index)
            np.save(book_page_dir_mask, self.current_mask)
            np.save(book_page_dir_text, self.current_text)
        
        
        #find next word
        flag = False
        for i in range(len(self.current_mask)):
            if(self.current_mask[i] != 0 and flag == False):
                flag = True
                self.current_word_index = i
                self.text_input.delete(0, tk.END)
                self.text_input.insert(0, self.current_text[i] )
        
        if(flag == False):
            self.text_input.delete(0, tk.END)
        
        self.text_correction_necessary()
        
        #update text file of paragraph
        text_path = "C:/Users/" + self.user + "/Texterkennung/Mask_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}.txt"
        
        if(os.path.exists(text_path)):
            os.remove(text_path)
        
        
        with open(text_path, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(' '.join(self.current_text))
        
        self.text_display.delete(1.0, tk.END)
        index = 1.0
        running_index = 0
        for word, color_flag in zip(self.current_text, self.current_mask):
            end_index = f'{index}+{len(word)}c'  # Calculate end index for current word
            
            
            # Insert word with appropriate tag based on color_flag
            if(running_index == self.current_word_index):
                self.text_display.insert(index, word, 'current')
            elif color_flag == 0:
                self.text_display.insert(index, word, 'no_error')
            elif(color_flag == 1):
                self.text_display.insert(index, word, 'dictionary_corrected')
            elif(color_flag == 2):
                self.text_display.insert(index, word, 'eigenword')
            else:
                self.text_display.insert(index, word, 'general_error')
            
            self.text_display.insert(index," ")
            index = end_index + '+1c'
            running_index += 1
        
        bold_font = font.Font(self.text_display, self.text_display.cget("font"))
        bold_font.configure(weight="bold")
        
        self.text_display.tag_configure('no_error', foreground='green')
        self.text_display.tag_configure('dictionary_corrected', foreground='orange')
        self.text_display.tag_configure('eigenword', foreground='blue')
        self.text_display.tag_configure('general_error', foreground='purple')
        self.text_display.tag_configure('current', foreground ='red', font=bold_font)

        
        display_ratio = 450/630  #width/height
        image_ratio = (self.right_border_current_paragraph-self.left_border_current_paragraph)/(self.bottom_border_current_paragraph-self.top_border_current_paragraph)
        
        image = Image.open(image_path)
        image = image.crop((self.left_border_current_paragraph,self.top_border_current_paragraph, self.right_border_current_paragraph, self.bottom_border_current_paragraph))
        
        
        if(display_ratio >= image_ratio):
            #height dominates
            image = image.resize((int(np.round(image_ratio*630)),630), Image.Resampling.LANCZOS)
        else:
            #width dominates
            image = image.resize((450, int(np.round(450/image_ratio))), Image.Resampling.LANCZOS)
        
        try:
            factor_x = self.image_size_after[0]/self.image_size_previous[0]
            factor_y = self.image_size_after[1]/self.image_size_previous[1]
            draw = ImageDraw.Draw(image)
            
            rect_start_x = ( self.text_border_x[self.current_word_index] - self.left_border_current_paragraph -5) *factor_x
            rect_start_y = ( self.text_border_y[self.current_word_index] - self.top_border_current_paragraph -5) *factor_y
            rect_end_x = rect_start_x + 5 + self.text_border_dx[self.current_word_index]*factor_x
            rect_end_y = rect_start_y + 5 + self.text_border_dy[self.current_word_index]*factor_y
            
            
            draw.rectangle([(rect_start_x, rect_start_y), (rect_end_x, rect_end_y)], outline="red", width = 3)
        except:
            pass
        
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        
        
    
    def text_correction_necessary(self):
        if(self.current_paragraph == 0):
            self.text_input.grid_remove()
        else:
            sum_mask = np.sum(self.current_mask)
            if(sum_mask != 0):
                self.text_input.grid()
            else:
                self.text_input.grid_remove()
        
    def page_deletable(self):
        txt_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}"
        mask_folder = 'C:/Users/' + self.user + '/Texterkennung/Mask_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}"
        positions_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}"
        text_numpy_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Numpy_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}"
        if((len(os.listdir(txt_folder))!=1 or len(os.listdir(mask_folder))!=0 or len(os.listdir(positions_folder))!=0 or len(os.listdir(text_numpy_folder))!=0) and self.current_paragraph == 0):
            self.empty_page_btn.grid()
            print(self.current_paragraph)
        else:
            self.empty_page_btn.grid_remove()
        
    
    def paragraph_deletable(self):
        txt_path = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}" +'/' +  f"Paragraph_{self.current_paragraph}.txt"
        mask_path = 'C:/Users/' + self.user + '/Texterkennung/Mask_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}" + '/' + f"Paragraph_{self.current_paragraph}.npy"
        positions_path = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}" +'/' +  f"Paragraph_{self.current_paragraph}.npy"
        txt_numpy_path = 'C:/Users/' + self.user + '/Texterkennung/Text_Numpy_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}" +'/' +  f"Paragraph_{self.current_paragraph}.npy"
        if(os.path.exists(txt_numpy_path) or os.path.exists(txt_path) or os.path.exists(positions_path) or os.path.exists(mask_path)):
            self.empty_paragraph_btn.grid()
        else:
            self.empty_paragraph_btn.grid_remove()
    
    def find_paragraph_count(self):
        text_path = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}"
        # Initialize the highest paragraph number
        self.paragraph_number = 0

        # Regular expression to match filenames and extract the number
        pattern = re.compile(r'Paragraph_(\d+)\.txt')

        # Iterate over all files in the directory
        for filename in os.listdir(text_path):
            # Search for the pattern in the filename
            match = pattern.match(filename)
            if match:
                # Extract the number from the filename and convert to integer
                number = int(match.group(1))
                # Update the highest paragraph number if current number is higher
                if number > self.paragraph_number:
                    self.paragraph_number = number
    
    def empty_page(self):
        #remove data from page
        x = self.empty_page_btn.winfo_rootx()
        y = self.empty_page_btn.winfo_rooty()
        
        confirm_window = tk.Toplevel(root)
        confirm_window.title("Confirmation")
        confirm_window.geometry(f"+{x}+{y}")
    
        msg = tk.Label(confirm_window, text="Are you sure?")
        msg.pack(pady=10)
    
        button_frame = tk.Frame(confirm_window)
        button_frame.pack(pady=10)
        
        def on_yes():
            confirm_window.destroy()
            txt_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}"
            mask_folder = 'C:/Users/' + self.user + '/Texterkennung/Mask_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}"
            positions_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}"
            exception_file = 'All_Paragraphs.txt'
            text_numpy_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Numpy_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}"
            positions_words_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Words_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}"

            # List all files in the directory
            for filename in os.listdir(txt_folder):
                file_path = os.path.join(txt_folder, filename)
                
                
                try:
                    os.remove(file_path)
                except:
                    pass
            #save empty exception file for GUI
            with open(os.path.join(txt_folder, exception_file), 'w'):
                pass
            
            for filename in os.listdir(mask_folder):
                file_path = os.path.join(mask_folder, filename)
                try:
                    os.remove(file_path)
                except:
                    pass
                
            for filename in os.listdir(positions_folder):
                file_path = os.path.join(positions_folder, filename)
                try:
                    os.remove(file_path)
                except:
                    pass
            
            for filename in os.listdir(text_numpy_folder):
                file_path = os.path.join(text_numpy_folder, filename)
                try:
                    os.remove(file_path)
                except:
                    pass
            
            for filename in os.listdir(positions_words_folder):
                file_path = os.path.join(positions_words_folder, filename)
                try:
                    shutil.rmtree(file_path)
                except:
                    pass
            
            self.next_image()
    
        def on_no():
            confirm_window.destroy()
        
        yes_button = tk.Button(button_frame, text="Yes", command=on_yes)
        yes_button.pack(side="left", padx=5)
    
        no_button = tk.Button(button_frame, text="No", command=on_no)
        no_button.pack(side="left", padx=5)
    
        confirm_window.grab_set() 
        
        
        
        
        
    def load_image_paths(self):
        # Replace this with actual image loading logic
        jpg_folder = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname)
        self.page_number = 0
        try:
            for file in os.listdir(jpg_folder):
                if(file.endswith('.jpg')):
                    self.page_number += 1
        except:
            pass

    def load_text_content(self):
        txt_folder = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) 
        count= 0
        try:
            for file in os.listdir(txt_folder):
                if(file.endswith('.txt')):
                    count += 1
        except:
            pass
        return count

    def update_image(self): 
        image_path = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}.jpg"
        print(image_path)
        image = Image.open(image_path)
        image = image.resize((450, 630), Image.Resampling.LANCZOS)        
        
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def prev_image(self):
        if(self.image_index >1):
            self.image_index = self.image_index -1
            self.find_paragraph_count()
            self.update_image()
            self.setup_text_display()
            self.current_paragraph = 0
            self.page_deletable()
            self.paragraph_deletable()
            
            self.text_input.delete(0, tk.END)
            self.text_correction_necessary()

    def next_image(self):
        if(self.image_index < self.page_number):
            self.image_index = self.image_index +1
            self.find_paragraph_count()
            self.update_image()
            self.setup_text_display()
            self.current_paragraph = 0
            self.page_deletable()
            self.paragraph_deletable()
            
            self.text_input.delete(0, tk.END)
            self.text_correction_necessary()
         
            
    def setup_text_display(self):
        text_path = "C:/Users/" + self.user + "/Texterkennung/Text_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + "All_Paragraphs.txt"
        with open(text_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, text_content)

    def prev_paragraph(self):
        self.current_word_index = -1
        self.find_paragraph_count()
        if(self.current_paragraph == 0 and self.image_index >1):
            self.image_index = self.image_index -1
            self.find_paragraph_count()
            self.current_paragraph = self.paragraph_number
            
            image_path = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}.jpg"
            paragraph_path = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}" +'/' + f"Paragraph_{self.current_paragraph}.npy"
            
            self.left_border_current_paragraph, self.right_border_current_paragraph, self.top_border_current_paragraph, self.bottom_border_current_paragraph = np.load(paragraph_path)
            
            #determine what side dominates
            display_ratio = 450/630  #width/height
            image_ratio = (self.right_border_current_paragraph-self.left_border_current_paragraph)/(self.bottom_border_current_paragraph-self.top_border_current_paragraph)
            
            image = Image.open(image_path)
            image = image.crop((self.left_border_current_paragraph,self.top_border_current_paragraph, self.right_border_current_paragraph, self.bottom_border_current_paragraph))
            
            self.image_size_previous = image.size
            
            if(display_ratio >= image_ratio):
                #height dominates
                image = image.resize((int(np.round(image_ratio*630)),630), Image.Resampling.LANCZOS)
                self.image_size_after = image.size
            else:
                #width dominates
                image = image.resize((450, int(np.round(450/image_ratio))), Image.Resampling.LANCZOS)
                self.image_size_after = image.size
                
        
            
            mask_path = "C:/Users/" + self.user + "/Texterkennung/Mask_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}.npy"
            text_numpy_path = "C:/Users/" + self.user + "/Texterkennung/Text_Numpy_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}.npy"
            
            self.current_mask = np.load(mask_path)
            self.current_text = np.load(text_numpy_path)
            flag = False
            for i in range(len(self.current_mask)):
                if(self.current_mask[i] != 0 and flag == False):
                    flag = True
                    self.current_word_index = i
                    self.text_input.delete(0, tk.END)
                    self.text_input.insert(0, self.current_text[i] )
            
            text_border_path_x = "C:/Users/" + self.user + "/Texterkennung/Position_Words_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}" +'/' +"x.npy"
            text_border_path_y = "C:/Users/" + self.user + "/Texterkennung/Position_Words_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}" +'/' +"y.npy"
            text_border_path_dx = "C:/Users/" + self.user + "/Texterkennung/Position_Words_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}" +'/' +"dx.npy"
            text_border_path_dy = "C:/Users/" + self.user + "/Texterkennung/Position_Words_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}" +'/' +"dy.npy"
            
            self.text_border_x = np.load(text_border_path_x)
            self.text_border_y = np.load(text_border_path_y)
            self.text_border_dx = np.load(text_border_path_dx)
            self.text_border_dy = np.load(text_border_path_dy)
            
        
            
            try:
                factor_x = self.image_size_after[0]/self.image_size_previous[0]
                factor_y = self.image_size_after[1]/self.image_size_previous[1]
                draw = ImageDraw.Draw(image)
                
                rect_start_x = ( self.text_border_x[self.current_word_index] - self.left_border_current_paragraph -5) *factor_x
                rect_start_y = ( self.text_border_y[self.current_word_index] - self.top_border_current_paragraph -5) *factor_y
                rect_end_x = rect_start_x + 5 + self.text_border_dx[self.current_word_index]*factor_x
                rect_end_y = rect_start_y + 5 + self.text_border_dy[self.current_word_index]*factor_y
                
                
                draw.rectangle([(rect_start_x, rect_start_y), (rect_end_x, rect_end_y)], outline="red", width = 3)
            except:
                pass
            
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            
            self.paragraph_deletable()
            self.page_deletable()
            
            if(flag == False):
                self.text_input.delete(0, tk.END)
            
            self.text_display.delete(1.0, tk.END)
            index = 1.0
            running_index = 0
            for word, color_flag in zip(self.current_text, self.current_mask):
                end_index = f'{index}+{len(word)}c'  # Calculate end index for current word
                
                # Insert word with appropriate tag based on color_flag
                if(running_index == self.current_word_index):
                    self.text_display.insert(index, word, 'current')
                elif color_flag == 0:
                    self.text_display.insert(index, word, 'no_error')
                elif(color_flag == 1):
                    self.text_display.insert(index, word, 'dictionary_corrected')
                elif(color_flag == 2):
                    self.text_display.insert(index, word, 'eigenword')
                else:
                    self.text_display.insert(index, word, 'general_error')
                
                self.text_display.insert(index," ")
                index = end_index + '+1c'
                running_index +=1
            
            bold_font = font.Font(self.text_display, self.text_display.cget("font"))
            bold_font.configure(weight="bold")
            
            self.text_display.tag_configure('no_error', foreground='green')
            self.text_display.tag_configure('dictionary_corrected', foreground='orange')
            self.text_display.tag_configure('eigenword', foreground='blue')
            self.text_display.tag_configure('general_error', foreground='purple')
            self.text_display.tag_configure('current', foreground ='red', font=bold_font)
            
            self.text_correction_necessary()
            
            
        elif(self.current_paragraph>0):
            flag = False
            if(self.current_paragraph > 1 and self.current_paragraph <= self.paragraph_number):
                while(flag == False and self.current_paragraph > 1):
                    self.current_paragraph = self.current_paragraph - 1
                    paragraph_path = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}" +'/' + f"Paragraph_{self.current_paragraph}.npy"
                    if(os.path.exists(paragraph_path)==True):
                        flag = True
            
            if(flag == True):
                image_path = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}.jpg"
                paragraph_path = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}" +'/' + f"Paragraph_{self.current_paragraph}.npy"
                
                self.left_border_current_paragraph, self.right_border_current_paragraph, self.top_border_current_paragraph, self.bottom_border_current_paragraph = np.load(paragraph_path)
                
                #determine what side dominates
                display_ratio = 450/630  #width/height
                image_ratio = (self.right_border_current_paragraph-self.left_border_current_paragraph)/(self.bottom_border_current_paragraph-self.top_border_current_paragraph)
                
                image = Image.open(image_path)
                image = image.crop((self.left_border_current_paragraph,self.top_border_current_paragraph, self.right_border_current_paragraph, self.bottom_border_current_paragraph))
                if(display_ratio >= image_ratio):
                    #height dominates
                    image = image.resize((int(np.round(image_ratio*630)),630), Image.Resampling.LANCZOS)
                else:
                    #width dominates
                    image = image.resize((450, int(np.round(450/image_ratio))), Image.Resampling.LANCZOS)
            
            
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
                
                
                self.paragraph_deletable()
                self.page_deletable()
                
                mask_path = "C:/Users/" + self.user + "/Texterkennung/Mask_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}.npy"
                text_numpy_path = "C:/Users/" + self.user + "/Texterkennung/Text_Numpy_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}.npy"
                
                self.current_mask = np.load(mask_path)
                self.current_text = np.load(text_numpy_path)
                flag = False
                for i in range(len(self.current_mask)):
                    if(self.current_mask[i] != 0 and flag == False):
                        flag = True
                        self.current_word_index = i
                        self.text_input.delete(0, tk.END)
                        self.text_input.insert(0, self.current_text[i] )
                
                if(flag == False):
                    self.text_input.delete(0, tk.END)
                
                self.text_display.delete(1.0, tk.END)
                index = 1.0
                running_index = 0
                for word, color_flag in zip(self.current_text, self.current_mask):
                    end_index = f'{index}+{len(word)}c'  # Calculate end index for current word
                    
                    # Insert word with appropriate tag based on color_flag
                    if(running_index == self.current_word_index):
                        self.text_display.insert(index, word, 'current')
                    elif color_flag == 0:
                        self.text_display.insert(index, word, 'no_error')
                    elif(color_flag == 1):
                        self.text_display.insert(index, word, 'dictionary_corrected')
                    elif(color_flag == 2):
                        self.text_display.insert(index, word, 'eigenword')
                    else:
                        self.text_display.insert(index, word, 'general_error')
                    
                    self.text_display.insert(index," ")
                    index = end_index + '+1c'
                    running_index += 1
                
                bold_font = font.Font(self.text_display, self.text_display.cget("font"))
                bold_font.configure(weight="bold")
                
                self.text_display.tag_configure('no_error', foreground='green')
                self.text_display.tag_configure('dictionary_corrected', foreground='orange')
                self.text_display.tag_configure('eigenword', foreground='blue')
                self.text_display.tag_configure('general_error', foreground='purple')
                self.text_display.tag_configure('current', foreground ='red', font=bold_font)
                                
                self.text_correction_necessary()
                
                
            elif(self.current_paragraph == 1 ):
                self.current_paragraph = self.current_paragraph - 1
                image_path = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}.jpg"
                
                image = Image.open(image_path)
                image = image.resize((450, 630), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
                
                text_path = "C:/Users/" + self.user + "/Texterkennung/Text_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + "All_Paragraphs.txt"
                with open(text_path, 'r', encoding='utf-8') as file:
                    text_content = file.read()
                    self.text_display.delete(1.0, tk.END)
                    self.text_display.insert(tk.END, text_content)
                
                self.paragraph_deletable()
                self.page_deletable()
                
                self.text_input.delete(0, tk.END)
        self.text_correction_necessary()
        

    def next_paragraph(self):
        self.current_word_index = -1
        self.find_paragraph_count()
        if(self.current_paragraph >= self.paragraph_number):
            self.next_image()
        else:
            safe = self.current_paragraph
            flag = False
            if(self.current_paragraph < self.paragraph_number):
                while(flag == False and self.current_paragraph < self.paragraph_number):
                    self.current_paragraph +=1 
                    paragraph_path = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}" +'/' + f"Paragraph_{self.current_paragraph}.npy"
                    if(os.path.exists(paragraph_path)==True):
                        flag = True
                    
            if(flag == False):
                self.current_paragraph = safe
            else:    
                print("new paragraph = " +str(self.current_paragraph))
                image_path = 'C:/Users/' + self.user + '/Texterkennung/JPG_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}.jpg"
                paragraph_path = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + "/" + f"Page_{self.image_index}" +'/' + f"Paragraph_{self.current_paragraph}.npy"
                self.left_border_current_paragraph, self.right_border_current_paragraph, self.top_border_current_paragraph, self.bottom_border_current_paragraph = np.load(paragraph_path)
                #determine what side dominates
                display_ratio = 450/630  #width/height
                image_ratio = (self.right_border_current_paragraph-self.left_border_current_paragraph)/(self.bottom_border_current_paragraph-self.top_border_current_paragraph)
                
                image = Image.open(image_path)
                image = image.crop((self.left_border_current_paragraph,self.top_border_current_paragraph, self.right_border_current_paragraph, self.bottom_border_current_paragraph))
                
                self.image_size_previous = image.size
                
                if(display_ratio >= image_ratio):
                    #height dominates
                    image = image.resize((int(np.round(image_ratio*630)),630), Image.Resampling.LANCZOS)
                    self.image_size_after = image.size
                else:
                    #width dominates
                    image = image.resize((450, int(np.round(450/image_ratio))), Image.Resampling.LANCZOS)
                    self.image_size_after = image.size              
                
                
                #input first word with flag != 0
                mask_path = "C:/Users/" + self.user + "/Texterkennung/Mask_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}.npy"
                text_numpy_path = "C:/Users/" + self.user + "/Texterkennung/Text_Numpy_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}.npy"
                
                self.current_mask = np.load(mask_path)
                self.current_text = np.load(text_numpy_path)
                
                
                flag = False
                for i in range(len(self.current_mask)):
                    if(self.current_mask[i] != 0 and flag == False):
                        flag = True
                        self.current_word_index = i
                        self.text_input.delete(0, tk.END)
                        self.text_input.insert(0, self.current_text[i] )
                
                
                text_border_path_x = "C:/Users/" + self.user + "/Texterkennung/Position_Words_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}" +'/' +"x.npy"
                text_border_path_y = "C:/Users/" + self.user + "/Texterkennung/Position_Words_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}" +'/' +"y.npy"
                text_border_path_dx = "C:/Users/" + self.user + "/Texterkennung/Position_Words_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}" +'/' +"dx.npy"
                text_border_path_dy = "C:/Users/" + self.user + "/Texterkennung/Position_Words_Files/" + str(self.bookname) + "/" + f"Page_{self.image_index}"+"/" + f"Paragraph_{self.current_paragraph}" +'/' +"dy.npy"
                
                self.text_border_x = np.load(text_border_path_x)
                self.text_border_y = np.load(text_border_path_y)
                self.text_border_dx = np.load(text_border_path_dx)
                self.text_border_dy = np.load(text_border_path_dy)
                
            
                
                try:
                    factor_x = self.image_size_after[0]/self.image_size_previous[0]
                    factor_y = self.image_size_after[1]/self.image_size_previous[1]
                    draw = ImageDraw.Draw(image)
                    
                    rect_start_x = ( self.text_border_x[self.current_word_index] - self.left_border_current_paragraph -5) *factor_x
                    rect_start_y = ( self.text_border_y[self.current_word_index] - self.top_border_current_paragraph -5) *factor_y
                    rect_end_x = rect_start_x + 5 + self.text_border_dx[self.current_word_index]*factor_x
                    rect_end_y = rect_start_y + 5 + self.text_border_dy[self.current_word_index]*factor_y
                    
                    
                    draw.rectangle([(rect_start_x, rect_start_y), (rect_end_x, rect_end_y)], outline="red", width = 3)
                except:
                    pass
                
                
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
                
                self.paragraph_deletable()
                self.page_deletable()
                
                
                
                if(flag == False):
                    self.text_input.delete(0, tk.END)
                
                self.text_display.delete(1.0, tk.END)
                index = 1.0
                running_index = 0
                for word, color_flag in zip(self.current_text, self.current_mask):
                    end_index = f'{index}+{len(word)}c'  # Calculate end index for current word
                    
                    # Insert word with appropriate tag based on color_flag
                    if(running_index == self.current_word_index):
                        self.text_display.insert(index, word, 'current')
                    elif color_flag == 0:
                        self.text_display.insert(index, word, 'no_error')
                    elif(color_flag == 1):
                        self.text_display.insert(index, word, 'dictionary_corrected')
                    elif(color_flag == 2):
                        self.text_display.insert(index, word, 'eigenword')
                    else:
                        self.text_display.insert(index, word, 'general_error')
                    
                    self.text_display.insert(index," ")
                    index = end_index + '+1c'
                    running_index += 1
                
                bold_font = font.Font(self.text_display, self.text_display.cget("font"))
                bold_font.configure(weight="bold")
                
                self.text_display.tag_configure('no_error', foreground='green')
                self.text_display.tag_configure('dictionary_corrected', foreground='orange')
                self.text_display.tag_configure('eigenword', foreground='blue')
                self.text_display.tag_configure('general_error', foreground='purple')
                self.text_display.tag_configure('current', foreground ='red', font=bold_font)
                
        self.text_correction_necessary()
        
        
        
                        
        
    def empty_paragraph(self):
        #remove data from page
        x = self.empty_paragraph_btn.winfo_rootx()
        y = self.empty_paragraph_btn.winfo_rooty()
        
        confirm_window = tk.Toplevel(root)
        confirm_window.title("Confirmation")
        confirm_window.geometry(f"+{x}+{y}")
    
        msg = tk.Label(confirm_window, text="Are you sure?")
        msg.pack(pady=10)
    
        button_frame = tk.Frame(confirm_window)
        button_frame.pack(pady=10)
        
        def on_yes():
            confirm_window.destroy()
            txt_path = 'C:/Users/' + self.user + '/Texterkennung/Text_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}" +'/' +  f"Paragraph_{self.current_paragraph}.txt"
            mask_path = 'C:/Users/' + self.user + '/Texterkennung/Mask_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}" + '/' + f"Paragraph_{self.current_paragraph}.npy"
            positions_path = 'C:/Users/' + self.user + '/Texterkennung/Position_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}" +'/' +  f"Paragraph_{self.current_paragraph}.npy"
            txt_numpy_path = 'C:/Users/' + self.user + '/Texterkennung/Text_Numpy_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}" +'/' +  f"Paragraph_{self.current_paragraph}.npy"
            txt_positions_folder = 'C:/Users/' + self.user + '/Texterkennung/Position_Words_Files/' + str(self.bookname) + '/' + f"Page_{self.image_index}" +'/' +  f"Paragraph_{self.current_paragraph}"
            os.remove(txt_path)
            os.remove(mask_path)
            os.remove(positions_path)
            os.remove(txt_numpy_path)    
            
            if(os.path.exists(txt_positions_folder)):
                try:
                    shutil.rmtree(txt_positions_folder)
                except:
                    pass
            
            self.next_paragraph()
            
        def on_no():
            confirm_window.destroy()
        
        yes_button = tk.Button(button_frame, text="Yes", command=on_yes)
        yes_button.pack(side="left", padx=5)
    
        no_button = tk.Button(button_frame, text="No", command=on_no)
        no_button.pack(side="left", padx=5)
    
        confirm_window.grab_set()
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = TextRecognitionApp(root)
    root.mainloop()
