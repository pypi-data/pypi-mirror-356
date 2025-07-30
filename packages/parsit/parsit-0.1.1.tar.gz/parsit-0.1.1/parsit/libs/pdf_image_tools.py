from io import BytesIO 
import cv2 
import fitz 
import numpy as np 
from PIL import Image 
from parsit .data .data_reader_writer import DataWriter 
from parsit .libs .commons import join_path 
from parsit .libs .hash_utils import compute_sha256 


def cut_image (bbox :tuple ,page_num :int ,page :fitz .Page ,return_path ,imageWriter :DataWriter ):


    filename =f'{page_num }_{int (bbox [0 ])}_{int (bbox [1 ])}_{int (bbox [2 ])}_{int (bbox [3 ])}'


    img_path =join_path (return_path ,filename )if return_path is not None else None 


    img_hash256_path =f'{compute_sha256 (img_path )}.png'


    rect =fitz .Rect (*bbox )

    zoom =fitz .Matrix (5 ,5 )

    pix =page .get_pixmap (clip =rect ,matrix =zoom )

    byte_data =pix .tobytes (output ='png')

    imageWriter .write (img_hash256_path ,byte_data )

    return img_hash256_path 


def cut_image_to_pil_image (bbox :tuple ,page :fitz .Page ,mode ="pillow"):


    rect =fitz .Rect (*bbox )

    zoom =fitz .Matrix (3 ,3 )

    pix =page .get_pixmap (clip =rect ,matrix =zoom )

    if mode =="cv2":

        img_array =np .frombuffer (pix .samples ,dtype =np .uint8 ).reshape (pix .height ,pix .width ,pix .n )

        if pix .n ==3 or pix .n ==4 :
            image_result =cv2 .cvtColor (img_array ,cv2 .COLOR_RGB2BGR )
        else :
            image_result =img_array 
    elif mode =="pillow":

        image_file =BytesIO (pix .tobytes (output ='png'))

        image_result =Image .open (image_file )
    else :
        raise ValueError (f"mode: {mode } is not supported.")

    return image_result 