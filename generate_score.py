# -*- coding: utf-8 -*-
# Author: Xin Li <xinii@msn.com>

import os
import glob
from PIL import Image
from fpdf import FPDF

clear_files = True
path = os.path.expanduser('./_tmp_for_gen_score')
piano_score_id = input('pianobooks.jp/score.php?id=')
piano_score_pages = input('Pages: ')
piano_score_author = input('Score author: ')
piano_score_name = input('Score name: ')

link_first = 'aria2c -d %s http://pianobooks.jp/gd/images' % path

for i in range(int(piano_score_pages)):
    for j in range(4):
        os.system('%s/%s/p%s_0%s.png' % (link_first, str(piano_score_id), str(i + 1), str(j)))
        os.system('mv %s/p%s_0%s.png %s/p%s_0%s.png' % (path, str(i + 1), str(j), path, str(i + 1).zfill(4), str(j)))
        os.system('%s/%s/p%s_1%s.png' % (link_first, str(piano_score_id), str(i + 1), str(j)))
        os.system('mv %s/p%s_1%s.png %s/p%s_1%s.png' % (path, str(i + 1), str(j), path, str(i + 1).zfill(4), str(j)))

images = []
pdf = FPDF('P', 'mm', 'A4')

images = glob.glob('%s/p????_??.png' % path)
images.sort()

for i in range(int(len(images) / 8)):
    imagefile = []
    print('Page: %d' % (i + 1))
    for j in range(8):
        imagefile.append(Image.open(images[i * 8 + j]))

    part_width = max(imagefile[0].size)
    part_height = min(imagefile[0].size)

    target = Image.new('RGB', (part_width*2, part_height*4))

    top_one = 0
    top_two = 0
    bottom_one = part_height
    bottom_two = part_height

    for j in range(len(imagefile)):
        if(j < 4):
            target.paste(imagefile[j], (0, top_one, part_width, bottom_one))
            top_one += part_height
            bottom_one += part_height
        else:
            target.paste(imagefile[j], (part_width, top_two, part_width*2, bottom_two))
            top_two += part_height
            bottom_two += part_height
            quality_value = 100

    if (not os.path.exists('%s/output' % path)):
        os.mkdir('%s/output' % path)
    
    target.save('%s/output/page_%s.jpg' % (path, str(i + 1).zfill(4)), quality = quality_value)

    pdf.add_page()
    pdf.image('%s/output/page_%s.jpg' % (path, str(i + 1).zfill(4)), 0, 0, 210, 297)

pdf_path = './' + str(piano_score_id).zfill(4) + '.' + piano_score_author + '.' + piano_score_name + '.pdf'
pdf.output(pdf_path, 'F')
print ('Score saved to: ' + pdf_path)
if (clear_files):
    print('Clearing temp files...')
    os.system('rm -rf %s' % path)
    print('Done.')
    
