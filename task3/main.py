import PIL
import PIL.Image
import numpy as np
import argparse

#simpleSVD
#numpySVD
#advancedSVD
#.file 
#class SVDLib:
    #def
def compress_image():
    print("hi")
def decompress_image():
    print("bu")

def main():
    parser = argparse.ArgumentParser(description="compress or decompress images using the following options:")
    parser.add_argument('input_file', type=str, default="a.in", help="Input file name")
    parser.add_argument('output_file', type=str, default="a.out", help="Output file mane")
    parser.add_argument('--mode', type=str, choices=['compress','decompress'], required=True, help='Mode: compress or decompress')
    parser.add_argument('--method', type=str, choices=['numpy','simple','advanced'], help='Compression method: numpy, simple, advanced')
    parser.add_argument('--compression', type=int, help='Compression level')
    args = parser.parse_args()

    if args.mode == 'compress':
        if args.method is None or args.compression is None:
            parser.error('--method and --compression are required when --mode=compress')
        img: PIL.Image.Image = PIL.Image.open(args.input_file)
        input_size: int =os.path.getsize(args.input_file)
        output_size: int =input_size // (args.compression)
        #получить размер на входе и после компрессии bmp 24 bit
        if args.method == 'numpy':
            print('n')
        elif args.method == 'simple':
            print('s')
        elif args.method == 'advanced':
            print("g")
    elif args.mode == 'decompress':
        decompress_image()       

if __name__ == "__main__":
    main()