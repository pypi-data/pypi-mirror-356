import os
import torch
import numpy as np
from PIL import Image
import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from gfpgan import GFPGANer

def is_valid_image(image_path):
    if not os.path.isfile(image_path):
        return False
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except:
        return False

def is_blurry(image_path, threshold=4.0):
    img = Image.open(image_path).convert("L")
    img_np = np.array(img)
    laplacian_var = cv2.Laplacian(img_np, cv2.CV_64F).var()
    print(f"Laplacian variance: {laplacian_var:.2f}")
    return laplacian_var < threshold

def load_upsampler(upscale):
    model = RRDBNet(
        num_in_ch=3, num_out_ch=3, num_feat=64,
        num_block=23, num_grow_ch=32, scale=2
    )
    model_path = 'weights/RealESRGAN_x2plus.pth'
    use_half = torch.cuda.is_available()
    return RealESRGANer(
        scale=upscale, model_path=model_path, model=model,
        tile=400, tile_pad=10, pre_pad=0, half=use_half
    )

def load_face_enhancer(upsampler, upscale):
    gfpgan_model_path = 'weights/GFPGANv1.3.pth'
    return GFPGANer(
        model_path=gfpgan_model_path,
        upscale=upscale,
        arch='clean',
        channel_multiplier=2,
        bg_upsampler=upsampler
    )
