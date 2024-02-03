from datetime import datetime
import glob
import imageio
import img2pdf
import numpy as np
import os
from pdf2image import convert_from_path
from sys import argv

input_pdf_path = argv[1]
output_pdf_path = argv[2]
cwd = os.getcwd()
cwd_img = os.path.join(cwd, 'pdf_images')
cwd_img_dir = os.path.join(cwd_img, os.path.basename(output_pdf_path).split(".")[0])

if not os.path.exists(cwd_img_dir):
    os.mkdir(cwd_img)
    os.mkdir(cwd_img_dir)

start_time = datetime.now()

print(f"\nConverting PDF to images...\n")
images = convert_from_path(input_pdf_path, dpi=300)

pdf2img_end = datetime.now()
print(f"PDF conversion to images took {pdf2img_end - start_time}\n")

print("Input rgb value (or range in given format) to remove.\n")
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

print(f"\nProgram will remove r={r_range}, g={g_range}, b={b_range}\n")

total = len(images)
i = 0

for image in images:
    image_array = np.array(image)
    print(image_array.shape)
    criteria = np.logical_and.reduce([
        (image_array[:, :, 0] >= r_range[0]) & (image_array[:, :, 0] <= r_range[1]),
        (image_array[:, :, 1] >= g_range[0]) & (image_array[:, :, 0] <= g_range[1]),
        (image_array[:, :, 2] >= b_range[0]) & (image_array[:, :, 0] <= b_range[1]),
    ])
    image_array[criteria] = 255
    imageio.imsave(os.path.join(cwd_img_dir, 'page'+ str(i) +'.png'), image_array)
    i += 1
    print(f"Highlight removal progress: {i}/{total} ({round(i/total * 100)}%)")

highlight_removal_end = datetime.now()
print(f"\nHighlight removal took {highlight_removal_end - pdf2img_end}\n")

print(f"Saving images...\n")

save_img_end = datetime.now()
print(f"Saving images took {save_img_end - highlight_removal_end}\n")

print("Converting images back to PDF...\n")

file_list = glob.glob(os.path.join(cwd_img_dir, '*.png'))
file_list.sort()

with open(output_pdf_path, "wb") as f:
    f.write(img2pdf.convert(file_list))

print(f"PDF saved to {output_pdf_path}\n")

print(f"Images conversion to PDF took {datetime.now() - save_img_end}\n")

print(f"Process took a total of {datetime.now() - start_time}\n")
