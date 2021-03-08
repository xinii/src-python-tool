import os
import sys
import argparse
from pathlib import Path
from pdf2image import convert_from_path
from shutil import copyfile

def convert(input_pdf_path, output_images_dir_path):
    print(input_pdf_path, output_images_dir_path)
    
    # poppler/binを環境変数PATHに追加する
    # poppler_dir = Path(__file__).parent.absolute() / "poppler/bin"
    # os.environ["PATH"] += os.pathsep + str(poppler_dir)
    
    # PDFファイルのパス
    pdf_path = Path("./pdf_file/pdf3009p.pdf")
    
    # PDF -> Image に変換（150dpi）
    pages = convert_from_path(input_pdf_path, 150)
    
    # 画像ファイルを１ページずつ保存
    image_dir = Path(output_images_dir_path)
    for i, page in enumerate(pages):
        file_name = pdf_path.stem + "_{:02d}".format(i + 1) + ".jpeg"
        image_path = image_dir / file_name
        # JPEGで保存
        page.save(str(image_path), "JPEG")

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('input', help='Relative or absolute path of the input PDF file')
    parser.add_argument('-o', '--out', help='Relative or absolute path of the output directory of images')
    args = parser.parse_args()

    # In case no output directory is specified, store in ./temp
    if not args.out:
        args.out = './temp'
        copyfile(args.input, args.input.replace(".pdf", "_BACKUP.pdf"))

    # Run
    convert(args.input, args.out)

if __name__ == '__main__':
    main()
