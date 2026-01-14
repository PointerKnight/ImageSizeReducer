from tkinter import ttk


class UISetup:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        
        self.progress = None
        self.status_label = None
        self.quality_label = None
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=("W", "E", "N", "S"))
        
        title_label = ttk.Label(
            main_frame, 
            text="Image Size Reducer", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        self._setup_folder_selection(main_frame)
        self._setup_compression_settings(main_frame)
        self._setup_progress_and_status(main_frame)
        self._setup_buttons(main_frame)
        self._setup_info(main_frame)
    
    def _setup_folder_selection(self, parent):
        ttk.Label(parent, text="Input Folder:").grid(row=1, column=0, sticky="W", pady=5)
        ttk.Entry(parent, textvariable=self.app.input_folder, width=50).grid(
            row=1, column=1, pady=5, padx=5
        )
        ttk.Button(
            parent, 
            text="Browse", 
            command=self.app.browse_input_folder
        ).grid(row=1, column=2, pady=5)
        
        ttk.Label(parent, text="Output Folder:").grid(row=2, column=0, sticky="W", pady=5)
        ttk.Entry(parent, textvariable=self.app.output_folder, width=50).grid(
            row=2, column=1, pady=5, padx=5
        )
        ttk.Button(
            parent, 
            text="Browse", 
            command=self.app.browse_output_folder
        ).grid(row=2, column=2, pady=5)
    
    def _setup_compression_settings(self, parent):
        quality_frame = ttk.LabelFrame(parent, text="Compression Settings", padding="10")
        quality_frame.grid(row=3, column=0, columnspan=3, sticky=("W", "E"), pady=10)
        
        ttk.Radiobutton(
            quality_frame, 
            text="No Quality Loss (Optimize only)",
            variable=self.app.compression_var, 
            value=False
        ).grid(row=0, column=0, sticky="W", pady=5)
        
        ttk.Radiobutton(
            quality_frame, 
            text="Reduce Size with Quality Adjustment",
            variable=self.app.compression_var, 
            value=True
        ).grid(row=1, column=0, sticky="W", pady=5)
        
        ttk.Label(quality_frame, text="Quality Level:").grid(row=2, column=0, sticky="W", pady=5)
        
        quality_scale = ttk.Scale(
            quality_frame, 
            from_=10, 
            to=95, 
            variable=self.app.quality_var,
            orient="horizontal", 
            length=200
        )
        quality_scale.grid(row=2, column=1, pady=5, padx=10)
        
        self.quality_label = ttk.Label(quality_frame, text="85%")
        self.quality_label.grid(row=2, column=2, pady=5)
        
        quality_scale.configure(command=self.app.update_quality_label)
    
    def _setup_progress_and_status(self, parent):
        self.progress = ttk.Progressbar(parent, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=("W", "E"), pady=10)
        
        self.status_label = ttk.Label(parent, text="Ready")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)
    
    def _setup_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        ttk.Button(
            button_frame, 
            text="Start Processing",
            command=self.app.start_processing
        ).pack(side="left", padx=10)
        
        ttk.Button(
            button_frame, 
            text="Clear",
            command=self.app.clear_all
        ).pack(side="left", padx=10)
        
        ttk.Button(
            button_frame, 
            text="Exit",
            command=self.root.quit
        ).pack(side="left", padx=10)
    
    def _setup_info(self, parent):
        info_text = """
How it works:
• No Quality Loss: Optimizes images without quality reduction (PNG optimization, JPEG without recompression)
• Reduce Size: Adjusts JPEG quality level to reduce file size
• Original resolution is maintained for both options
• Supported formats: JPG, JPEG, PNG, WEBP
        """
        info_label = ttk.Label(parent, text=info_text, justify="left")
        info_label.grid(row=7, column=0, columnspan=3, pady=10, sticky="W")
