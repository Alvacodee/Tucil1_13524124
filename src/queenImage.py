import os
import random
from PIL import Image, ImageDraw, ImageFont

# Setup folder
IMG_DIR = "test/img"
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

def get_color(char):
    # Seed random biar warna konsisten per karakter
    random.seed(ord(char))
    r = random.randint(150, 255)
    g = random.randint(150, 255)
    b = random.randint(150, 255)
    return (r, g, b)

def save_board_image(board, solution_mask=None, filename="output.png"):
    # Path handling sederhana
    if not filename.endswith(".png"):
        filename += ".png"
    
    if not os.path.dirname(filename):
        filename = os.path.join(IMG_DIR, filename)

    n = len(board)
    cell_size = 60
    padding = 20
    img_size = (n * cell_size) + (2 * padding)
    
    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)
    
    # Font default biar aman
    font = ImageFont.load_default()

    for r in range(n):
        for c in range(n):
            x1 = padding + (c * cell_size)
            y1 = padding + (r * cell_size)
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            
            # Gambar kotak
            color = get_color(board[r][c])
            draw.rectangle([x1, y1, x2, y2], fill=color, outline="black", width=2)
            
            # Tulis label wilayah
            draw.text((x1+5, y1+5), board[r][c], fill="black", font=font)
            
            # Gambar Ratu (Lingkaran Merah)
            if solution_mask and solution_mask[r][c]:
                m = 10 # margin
                draw.ellipse([x1+m, y1+m, x2-m, y2-m], fill="red", outline="darkred")
                # Tulis Q di tengah (agak manual posisinya)
                draw.text((x1+25, y1+20), "Q", fill="white", font=font)

    img.save(filename)
    print(f"Image saved: {filename}")
    return filename

# Bonus: Baca gambar jadi matriks (Simple Sampling)
def image_to_matrix(image_path, n):
    try:
        img = Image.open(image_path).convert("RGB")
        w, h = img.size
        
        cell_w = w / n
        cell_h = h / n
        
        matrix = []
        color_map = {} # Mapping (R,G,B) -> Char
        next_char = 65 # 'A'
        
        for r in range(n):
            row_data = []
            for c in range(n):
                # Sample titik tengah
                cx = int((c * cell_w) + (cell_w / 2))
                cy = int((r * cell_h) + (cell_h / 2))
                pixel = img.getpixel((cx, cy))
                
                # Cek warna mirip (toleransi 30)
                found = None
                for k_col, char in color_map.items():
                    dist = sum(abs(p - k) for p, k in zip(pixel, k_col))
                    if dist < 30:
                        found = char
                        break
                
                if not found:
                    found = chr(next_char)
                    color_map[pixel] = found
                    next_char += 1
                
                row_data.append(found)
            matrix.append(row_data)
            
        return matrix
    except Exception:
        print("Gagal baca gambar.")
        return None