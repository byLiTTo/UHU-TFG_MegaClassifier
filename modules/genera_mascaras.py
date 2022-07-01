"""

"""
###################################################################################################
# IMPORTs

import os
import io
import sys
import cv2
import json
import numpy as np
import platform
import argparse
import matplotlib
import visualization.visualization_utils as v_utils

from tqdm import tqdm
from pathutils import PathUtils as p_utils



###################################################################################################
# FUNCIONES

def generate_binary_image(detections, image):
    im_height, im_width = image.shape[0], image.shape[1]

    mask = np.zeros((im_height, im_width))

    for detection in detections:
        x1, y1, w_box, h_box = detection['bbox']
        ymin,xmin,ymax,xmax = y1, x1, y1 + h_box, x1 + w_box

        # Convert to pixels so we can use the PIL crop() function
        (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                        ymin * im_height, ymax * im_height)

        left = round(left)
        right = round(right)
        top = round(top)
        bottom = round(bottom)
        
        # Representación: img[y0:y1, x0:x1]
        mask[top:bottom,left:right] = 1

    return mask



###################################################################################################
# FUNCIÓN PRINCIPAL

def run(input_file_names, output_dir):
    """
    
    """
    if platform.system() == 'Windows':
        windows = True
    else:
        windows = False
        
    if len(input_file_names) == 0:
        print("WARNING: No hay ficheros disponibles")
        return
    
    for input_path in tqdm(input_file_names):
        with open(input_path) as f:
            input_file = json.load(f)

        image_file = input_file['file']

        name, ext = os.path.splitext(os.path.basename(image_file).lower())
        if windows:
            output_file = (output_dir + '\\' + name + '_mask.png')
        else:
            output_file = (output_dir + '/' + name + '_mask.png')

        image = cv2.imread(image_file)        

        mask = generate_binary_image(input_file['detections'],image)
        
        cv2.imwrite(output_file, mask * 255)



###################################################################################################
# Command-line driver

def main():
    parser = argparse.ArgumentParser(
        description = 'Módulo para renderizar los bounding boxes de las detecciones de las imágenes '
            'indicadas')
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument(
        '--input_file',
        help = 'Fichero JSON del que se tomarán los datos para realizar el recorte'
    )
    group.add_argument(
        '--input_dir',
        help = 'Ruta al directorio donde se encuentran los ficheros JSON de los cuales se tomarán '
            'los datos para realizar los recortes a las diferentes imágenes, hace uso de la '
            'opción --recursive'
    )
    parser.add_argument(
        '--recursive',
        action = 'store_true',
        help = 'Maneja directorios de forma recursiva, solo tiene sentido usarlo con --input_file'
    )
    parser.add_argument(
        '--output_dir',
        help = 'Ruta al directorio de donde se guardaran las imágenes con los bounding boxes '
            'renderizados'
    )

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    if args.input_file:
        input_file_names = [args.input_file]
    else:
        input_file_names = p_utils.find_detections(args.input_dir, args.recursive)

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
    else:
        if args.input_dir:
            args.output_dir = args.input_dir
        else:
            args.output_dir = os.path.dirname(args.input_file)
    
    run(input_file_names=input_file_names, output_dir=args.output_dir)
    print('==========================================================================================')



if __name__ == '__main__':
    main()    



###################################################################################################