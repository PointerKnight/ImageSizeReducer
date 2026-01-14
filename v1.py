import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pathlib import Path
from PIL import Image
import threading

class ImageSizeReducer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Size Reducer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.quality_var = tk.IntVar(value=85)  # Default quality
        self.compression_var = tk.BooleanVar(value=False)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Image Size Reducer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input folder selection
        ttk.Label(main_frame, text="Input Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_folder, width=50).grid(row=1, column=1, pady=5, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input_folder).grid(row=1, column=2, pady=5)
        
        # Output folder selection
        ttk.Label(main_frame, text="Output Folder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_folder, width=50).grid(row=2, column=1, pady=5, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_folder).grid(row=2, column=2, pady=5)
        
        # Quality settings frame
        quality_frame = ttk.LabelFrame(main_frame, text="Compression Settings", padding="10")
        quality_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # No compression option
        ttk.Radiobutton(quality_frame, text="No Quality Loss (Optimize only)", 
                       variable=self.compression_var, value=False).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # With compression option
        ttk.Radiobutton(quality_frame, text="Reduce Size with Quality Adjustment", 
                       variable=self.compression_var, value=True).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Quality slider
        ttk.Label(quality_frame, text="Quality Level:").grid(row=2, column=0, sticky=tk.W, pady=5)
        quality_scale = ttk.Scale(quality_frame, from_=10, to=95, variable=self.quality_var,
                                 orient=tk.HORIZONTAL, length=200)
        quality_scale.grid(row=2, column=1, pady=5, padx=10)
        
        self.quality_label = ttk.Label(quality_frame, text="85%")
        self.quality_label.grid(row=2, column=2, pady=5)
        
        # Bind quality slider update
        quality_scale.configure(command=self.update_quality_label)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Start Processing", 
                  command=self.start_processing).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=10)
        
        # Info text
        info_text = """
How it works:
• No Quality Loss: Optimizes images without quality reduction (PNG optimization, JPEG without recompression)
• Reduce Size: Adjusts JPEG quality level to reduce file size
• Original resolution is maintained for both options
• Supported formats: JPG, JPEG, PNG, WEBP
        """
        info_label = ttk.Label(main_frame, text=info_text, justify=tk.LEFT)
        info_label.grid(row=7, column=0, columnspan=3, pady=10, sticky=tk.W)
    
    def update_quality_label(self, value):
        self.quality_label.config(text=f"{int(float(value))}%")
    
    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)
            # Auto-set output folder
            if not self.output_folder.get():
                self.output_folder.set(os.path.join(folder, "reduced_images"))
    
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
    
    def clear_all(self):
        self.input_folder.set("")
        self.output_folder.set("")
        self.progress['value'] = 0
        self.status_label.config(text="Ready")
    
    def get_image_files(self, folder):
        """Get all image files from folder"""
        extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'}
        image_files = []
        
        for file_path in Path(folder).iterdir():
            if file_path.suffix.lower() in extensions and file_path.is_file():
                image_files.append(file_path)
        
        return image_files
    
    def optimize_without_quality_loss(self, input_path, output_path):
        """Optimize image without quality loss"""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    # Create white background for transparent images
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Save with optimization
                if input_path.lower().endswith(('.png', '.bmp')):
                    # For PNG, use optimize flag
                    img.save(output_path, optimize=True)
                else:
                    # For JPEG, save with high quality but progressive
                    img.save(output_path, quality=95, optimize=True, progressive=True)
                    
            return True
        except Exception as e:
            print(f"Error optimizing {input_path}: {e}")
            return False
    
    def compress_with_quality_reduction(self, input_path, output_path, quality):
        """Compress image with quality reduction"""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Save with specified quality
                img.save(output_path, quality=quality, optimize=True, progressive=True)
                
            return True
        except Exception as e:
            print(f"Error compressing {input_path}: {e}")
            return False
    
    def process_images(self):
        """Main processing function"""
        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()
        
        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Please select both input and output folders")
            return
        
        if not os.path.exists(input_folder):
            messagebox.showerror("Error", "Input folder does not exist")
            return
        
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Get image files
        image_files = self.get_image_files(input_folder)
        
        if not image_files:
            messagebox.showinfo("No Images", "No image files found in the selected folder")
            return
        
        total_files = len(image_files)
        processed = 0
        success_count = 0
        
        self.progress['maximum'] = total_files
        self.progress['value'] = 0
        
        for image_file in image_files:
            filename = image_file.name
            output_path = os.path.join(output_folder, filename)
            
            self.status_label.config(text=f"Processing: {filename}")
            
            try:
                if self.compression_var.get():
                    # With quality reduction
                    success = self.compress_with_quality_reduction(
                        str(image_file), output_path, self.quality_var.get()
                    )
                else:
                    # Without quality loss
                    success = self.optimize_without_quality_loss(str(image_file), output_path)
                
                if success:
                    success_count += 1
                    
                    # Get file sizes for comparison
                    original_size = os.path.getsize(str(image_file))
                    new_size = os.path.getsize(output_path)
                    
                    # Log the result
                    reduction = ((original_size - new_size) / original_size) * 100
                    print(f"Processed: {filename}")
                    print(f"  Original: {original_size/1024:.1f} KB")
                    print(f"  New: {new_size/1024:.1f} KB")
                    print(f"  Reduction: {reduction:.1f}%")
                    
            except Exception as e:
                print(f"Failed to process {filename}: {e}")
            
            processed += 1
            self.progress['value'] = processed
            self.root.update_idletasks()
        
        # Show completion message
        self.status_label.config(text="Processing Complete")
        
        messagebox.showinfo(
            "Complete",
            f"Processed {total_files} images\n"
            f"Successfully reduced: {success_count} images\n"
            f"Output folder: {output_folder}"
        )
    
    def start_processing(self):
        """Start processing in a separate thread"""
        thread = threading.Thread(target=self.process_images)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = ImageSizeReducer(root)
    root.mainloop()

if __name__ == "__main__":
    main()