from tkinter import filedialog
from pathlib import Path


class FileOperations:
    
    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'}
    
    def select_folder(self, title):
        return filedialog.askdirectory(title=title)
    
    def get_image_files(self, folder):
        image_files = []
        
        for file_path in Path(folder).iterdir():
            if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS and file_path.is_file():
                image_files.append(file_path)
        
        return image_files
