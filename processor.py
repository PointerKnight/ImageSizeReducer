from PIL import Image


class ImageProcessor:
    
    def optimize_without_quality_loss(self, input_path, output_path):
        try:
            with Image.open(input_path) as img:
                img = self._convert_to_rgb(img)
                
                if input_path.lower().endswith(('.png', '.bmp')):
                    img.save(output_path, optimize=True)
                else:
                    img.save(output_path, quality=95, optimize=True, progressive=True)
                    
            return True
        except Exception as e:
            print(f"Error optimizing {input_path}: {e}")
            return False
    
    def compress_with_quality_reduction(self, input_path, output_path, quality):
        try:
            with Image.open(input_path) as img:
                img = self._convert_to_rgb(img)
                img.save(output_path, quality=quality, optimize=True, progressive=True)
                
            return True
        except Exception as e:
            print(f"Error compressing {input_path}: {e}")
            return False
    
    def _convert_to_rgb(self, img):
        if img.mode in ('RGBA', 'LA', 'P'):
            if img.mode == 'P':
                img = img.convert('RGBA')
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            return background
        elif img.mode != 'RGB':
            return img.convert('RGB')
        return img
