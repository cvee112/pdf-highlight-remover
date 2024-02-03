from datetime import datetime
import glob
import imageio
import img2pdf
import numpy as np
import os
import pypdfium2 as pdfium
from sys import argv

input_pdf_path = argv[1]
output_pdf_path = argv[2]
cwd = os.getcwd()
cwd_img = os.path.join(cwd, 'pdf_images')
cwd_img_dir = os.path.join(cwd_img, os.path.basename(output_pdf_path).split(".")[0])

if not os.path.exists(cwd_img):
    os.mkdir(cwd_img)
if not os.path.exists(cwd_img_dir):
    os.mkdir(cwd_img_dir)

print("\nInput rgb value (or range in given format) to remove.\n")
r_range = input("r or [r_min, r_max]: ")
g_range = input("g or [g_min, g_max]: ")
b_range = input("b or [b_min, b_max]: ")

try:
    r_range = [int(r_range)] * 2
except ValueError:
    r_range = [int(r) for r in r_range.strip("[").strip("]").split(", ")]
try:
    g_range = [int(g_range)] * 2
except ValueError:
    g_range = [int(g) for g in g_range.strip("[").strip("]").split(", ")]
try:
    b_range = [int(b_range)] * 2
except ValueError:
    b_range = [int(b) for b in b_range.strip("[").strip("]").split(", ")]

print(f"\nProgram will remove rgb({r_range}, {g_range}, {b_range})\n")

start_time = datetime.now()

pdf = pdfium.PdfDocument(input_pdf_path)
n_pages = len(pdf)

for page_number in range(n_pages):
    page = pdf.get_page(page_number)
    bitmap = page.render(scale=4.2)
    image = bitmap.to_pil()
    image_array = np.array(image)
    criteria = np.logical_and.reduce([
        (image_array[:, :, 0] >= r_range[0]) & (image_array[:, :, 0] <= r_range[1]),
        (image_array[:, :, 1] >= g_range[0]) & (image_array[:, :, 1] <= g_range[1]),
        (image_array[:, :, 2] >= b_range[0]) & (image_array[:, :, 2] <= b_range[1]),
    ])
    image_array[criteria] = 255
    imageio.imsave(os.path.join(cwd_img_dir, f"{page_number:0>3d}" +'.png'), image_array)
    print(f"Progress: {page_number}/{n_pages} ({round(page_number/n_pages * 100)}%)")

highlight_removal_end = datetime.now()
print(f"\nConversion to images + highlight removal + image saving took {highlight_removal_end - start_time}\n")

print("Converting images back to PDF...\n")

file_list = glob.glob(os.path.join(cwd_img_dir, '*.png'))
file_list.sort()

with open(output_pdf_path, "wb") as f:
    f.write(img2pdf.convert(file_list))

print(f"PDF saved to {output_pdf_path}\n")

print(f"Images conversion to PDF took {datetime.now() - highlight_removal_end}\n")

print(f"Process took a total of {datetime.now() - start_time}\n")
