import os
import re
from PIL import Image

def resize_and_pad(img, target_size, bg_color=(255, 255, 255, 0)):
    target_w, target_h = target_size
    img_w, img_h = img.size
    ratio = min(target_w / img_w, target_h / img_h)
    new_w = int(img_w * ratio)
    new_h = int(img_h * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    new_img = Image.new('RGBA', (target_w, target_h), bg_color)
    paste_x = (target_w - new_w) // 2
    paste_y = (target_h - new_h) // 2
    new_img.paste(img, (paste_x, paste_y), mask=img if img.mode == 'RGBA' else None)
    return new_img

def process_image(img_path, out_path, target_size):
    with Image.open(img_path) as img:
        img = img.convert("RGBA")
        img = resize_and_pad(img, target_size)
        img.save(out_path, "PNG")

def is_target_folder(folder_name):
    return re.match(r'^\d{2,4}x\d{2,4}$', folder_name)

def get_size_from_folder(folder_name):
    m = re.match(r'^(\d{2,4})x(\d{2,4})$', folder_name)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None

def main():
    root = os.getcwd()
    for dirpath, dirnames, filenames in os.walk(root):
        folder = os.path.basename(dirpath)
        if is_target_folder(folder):
            size = get_size_from_folder(folder)
            print(f"处理文件夹：{folder}，目标尺寸：{size}")
            for filename in filenames:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                    img_path = os.path.join(dirpath, filename)
                    process_image(img_path, img_path, size)
                    print(f"已处理：{img_path}")

if __name__ == "__main__":
    main()
