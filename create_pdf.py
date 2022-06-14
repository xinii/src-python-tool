# -*- coding: utf-8 -*-
import os
import glob
import random
import string
import argparse
from PIL import Image, ImageEnhance
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path

pdf_width = 0
pdf_height = 0
single_pdf_input = False
src = ''
dest = ''
image_type = ''
images = ''

def core_process():
    canvas_output = BytesIO()
    c = canvas.Canvas(canvas_output, pagesize=A4)

    for target in images:
        im = 0 if single_pdf_input else Image.open(target)
        if(single_pdf_input):
            temp_image = './__temp_file_' + ''.join(random.choice(string.ascii_lowercase) for j in range(20))
            if not os.path.exists(temp_image):
                # target = ImageEnhance.Sharpness(target).enhance(+10.0)
                target.save(temp_image, 'JPEG')
                im = Image.open(temp_image)
                target = temp_image
            else:
                print("Temp image can not be created.")
                break;

        print("Processing " + str(target) + " ...")
        page_width = im.size[0]
        page_height = im.size[1]
        print(page_width, page_height)

        width = 0
        height = 0
        if(page_width / page_height > pdf_width / pdf_height):
            width = pdf_width
            height = pdf_width * page_height / page_width
            x = 0
            y = (pdf_height - height) / 2.0
        else:
            width = pdf_height * page_width / page_height
            height = pdf_height
            x = (pdf_width - width) / 2.0
            y = 0

        c.setPageSize((pdf_width, pdf_height))
        c.setTitle("")
        c.drawImage(target, x, y, width=width, height=height)
        c.showPage()
        if(single_pdf_input):
            os.remove(temp_image)

    c.save()
    return canvas_output

def generate_pdf():
    canvas_output = core_process()

    pdf_reader = PdfFileReader(canvas_output)
    pdf_writer = PdfFileWriter()
    for i in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(i))

    output_file = open(dest, "wb")
    pdf_writer.write(output_file)

    canvas_output.close()
    output_file.close()
    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A tool to generate PDF from multiple images in a directory, " +
                                     "or from pages in a single PDF file.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("src", help="Input PDF file path or directory of images")
    parser.add_argument("dest", help="Output PDF file path")
    parser.add_argument("-t", "--image-type", default="png", help=
                        "When the input is a directory, the file type of the images in the directory")
    parser.add_argument("-w", "--pdf-width", default="842", help="Horizontal width for PDF pages")
    parser.add_argument("-v", "--pdf-height", default="595", help="Vertical height for PDF pages")
    args = parser.parse_args()
    src = args.src
    dest = args.dest
    pdf_width = int(args.pdf_width)
    pdf_height = int(args.pdf_height)
    
    if os.path.isdir(src):
        print("Multiple images mode, sorting images ...")
        image_type = args.image_type
        images = glob.glob(os.path.normpath(src) + "/*." + image_type)
        images.sort()
    elif os.path.isfile(src) and os.path.splitext(src)[1] == '.pdf':
        print("Single PDF file mode, generating images ...")
        single_pdf_input = True
        images = convert_from_path(src)
    else:
        print("\nInvalid input.")

    generate_pdf()
