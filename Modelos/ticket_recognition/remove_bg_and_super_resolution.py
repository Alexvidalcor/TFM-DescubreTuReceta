import time
from cv2 import dnn_superres
import cv2
import os
from rembg import remove

ticket_bg = "ticket_recognition/imagen_javier.jpeg"
ticket_no_bg = "ticket_recognition/imagen_javier_no_bg.png"
model = "ticket_recognition/EDSR_x4.pb"


def delete_background(image_path: str) -> str:
    """Delete image background
    
    Args:
        image_path: path of the image which its background is being removed.
    
    Returns:
        str: image with the background removed path.
    """
    aux_list = image_path.split(".")
    output_path = aux_list[0] + "_no_bg.png"
    with open(image_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)
            return output_path

def super_resolution(image_path: str, model_path: str) -> str:
    """Get an image with super resolution
    
    Args:
        image_path: path of the image which is being converted to super resolution.
        model_path: requiered model for super resolution path.

    Returns:
        str: image with super resolution path.
    """

    # extract the model name and model scale from the file path
    # extract the model name and model scale from the file path
    modelName = model_path.split("/")[-1]
    modelName = modelName.split(os.path.sep)[-1].split("_")[0].lower()
    modelScale = model_path.split("_x")[-1]
    modelScale = int(modelScale[:modelScale.find(".")])

    # initialize OpenCV's super resolution DNN object, load the super
    # resolution model from disk, and set the model name and scale
    print("[INFO] loading super resolution model: {}".format(
        model_path))
    print("[INFO] model name: {}".format(modelName))
    print("[INFO] model scale: {}".format(modelScale))
    sr = dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    # sr.setModel(modelName, modelScale)
    sr.setModel(modelName,modelScale)

    # load the input image from disk and display its spatial dimensions
    image = cv2.imread(image_path)
    print("[INFO] w: {}, h: {}".format(image.shape[1], image.shape[0]))
    # use the super resolution model to upscale the image, timing how
    # long it takes
    start = time.time()
    upscaled = sr.upsample(image)
    end = time.time()
    print("[INFO] super resolution took {:.6f} seconds".format(
        end - start))
    # show the spatial dimensions of the super resolution image
    print("[INFO] w: {}, h: {}".format(upscaled.shape[1],
        upscaled.shape[0]))

    # cv2.imshow("Original", image)
    # # cv2.imshow("Bicubic", bicubic)
    # cv2.imshow("Super Resolution", upscaled)
    # cv2.waitKey(0)

    aux_list = image_path.split(".")
    output_path = aux_list[0] + "_super_resolution.png"
    cv2.imwrite(output_path, upscaled)

    return output_path









