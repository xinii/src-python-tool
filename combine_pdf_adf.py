# -*- coding: utf-8 -*-
# Author: Xin Li <xinii@msn.com>

import PyPDF2, os

def main(angle1, angle2):
    pdf_file1 = open('./1.pdf', 'rb')
    pdf_file2 = open('./2.pdf', 'rb')
    pdf_reader1 = PyPDF2.PdfFileReader(pdf_file1, strict=False)
    pdf_reader2 = PyPDF2.PdfFileReader(pdf_file2, strict=False)
    pdf_writer = PyPDF2.PdfFileWriter()

    half = pdf_reader1.numPages
    if(half == pdf_reader2.numPages):
        for i in range(half):
            page_obj = pdf_reader1.getPage(i)
            if(not angle1 == 0):
                page_obj.rotateCounterClockwise(angle1)
                
            pdf_writer.addPage(page_obj)
            
            page_obj = pdf_reader2.getPage(half - 1 - i)
            if(not angle2 == 0):
                page_obj.rotateCounterClockwise(angle2)
                
            pdf_writer.addPage(page_obj)

    else:
        print('two files don\'t have the same page numbers.')
        
    pdf_output_file = open('./combined.pdf', 'wb')
    pdf_writer.write(pdf_output_file)
    pdf_output_file.close()
    pdf_file1.close()
    pdf_file2.close()

def single(angle):
    pdf_file = open('./1.pdf', 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file, strict=False)
    pdf_writer = PyPDF2.PdfFileWriter()

    pages = pdf_reader.numPages
    for i in range(pages):
        page_obj = pdf_reader.getPage(i)
        if(not angle == 0):
            page_obj.rotateCounterClockwise(angle)
            
        pdf_writer.addPage(page_obj)

    pdf_output_file = open('./combined.pdf', 'wb')
    pdf_writer.write(pdf_output_file)
    pdf_output_file.close()
    pdf_file.close()
    
if __name__ == '__main__':
    task = input('main or single? ')
    if(task == 'main'):
        angle1 = int(input('angle1: '))
        angle2 = int(input('angle2: '))
        main(angle1, angle2)
    elif(task == 'single'):
        angle = int(input('angle: '))
        single(angle)
