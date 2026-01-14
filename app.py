import tkinter as tk
from tkinter import messagebox
import threading
import os

from ui import UISetup
from processor import ImageProcessor
from utils import FileOperations


class ImageSizeReducer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Size Reducer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.quality_var = tk.IntVar(value=85)
        self.compression_var = tk.BooleanVar(value=False)
        
        self.ui = UISetup(root, self)
        self.processor = ImageProcessor()
        self.file_ops = FileOperations()
    
    def browse_input_folder(self):
        folder = self.file_ops.select_folder("Select Input Folder")
        if folder:
            self.input_folder.set(folder)
            if not self.output_folder.get():
                self.output_folder.set(os.path.join(folder, "reduced_images"))
    
    def browse_output_folder(self):
        folder = self.file_ops.select_folder("Select Output Folder")
        if folder:
            self.output_folder.set(folder)
    
    def clear_all(self):
        self.input_folder.set("")
        self.output_folder.set("")
        self.ui.progress['value'] = 0
        self.ui.status_label.config(text="Ready")
    
    def update_quality_label(self, value):
        self.ui.quality_label.config(text=f"{int(float(value))}%")
    
    def start_processing(self):
        thread = threading.Thread(target=self.process_images)
        thread.daemon = True
        thread.start()
    
    def process_images(self):
        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()
        
        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Please select both input and output folders")
            return
        
        if not os.path.exists(input_folder):
            messagebox.showerror("Error", "Input folder does not exist")
            return
        
        os.makedirs(output_folder, exist_ok=True)
        
        image_files = self.file_ops.get_image_files(input_folder)
        
        if not image_files:
            messagebox.showinfo("No Images", "No image files found in the selected folder")
            return
        
        total_files = len(image_files)
        success_count = 0
        
        self.ui.progress['maximum'] = total_files
        self.ui.progress['value'] = 0
        
        for idx, image_file in enumerate(image_files):
            filename = image_file.name
            output_path = os.path.join(output_folder, filename)
            
            self.ui.status_label.config(text=f"Processing: {filename}")
            
            try:
                if self.compression_var.get():
                    success = self.processor.compress_with_quality_reduction(
                        str(image_file), output_path, self.quality_var.get()
                    )
                else:
                    success = self.processor.optimize_without_quality_loss(
                        str(image_file), output_path
                    )
                
                if success:
                    success_count += 1
                    self._log_result(filename, image_file, output_path)
                    
            except Exception as e:
                print(f"Failed to process {filename}: {e}")
            
            self.ui.progress['value'] = idx + 1
            self.root.update_idletasks()
        
        self.ui.status_label.config(text="Processing Complete")
        messagebox.showinfo(
            "Complete",
            f"Processed {total_files} images\n"
            f"Successfully reduced: {success_count} images\n"
            f"Output folder: {output_folder}"
        )
    
    def _log_result(self, filename, input_path, output_path):
        original_size = os.path.getsize(str(input_path))
        new_size = os.path.getsize(output_path)
        reduction = ((original_size - new_size) / original_size) * 100
        
        print(f"Processed: {filename}")
        print(f"  Original: {original_size/1024:.1f} KB")
        print(f"  New: {new_size/1024:.1f} KB")
        print(f"  Reduction: {reduction:.1f}%")
