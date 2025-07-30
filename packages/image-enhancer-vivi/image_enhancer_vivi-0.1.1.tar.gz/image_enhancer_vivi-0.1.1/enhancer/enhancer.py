from .utils import is_valid_image, is_blurry, load_upsampler, load_face_enhancer
import os
import cv2
from basicsr.utils import imwrite

def enhance_image(input_path, output_dir='results', suffix='restored', upscale=2, use_gfpgan=True):
    os.makedirs(output_dir, exist_ok=True)

    if not is_valid_image(input_path):
        print("Invalid image. Please upload a valid image.")
        return

    if is_blurry(input_path):
        print("Image is too blurry. Please upload another one.")
        return

    print("Loading model...")
    upsampler = load_upsampler(upscale)
    face_enhancer = load_face_enhancer(upsampler, upscale) if use_gfpgan else None

    img_name = os.path.basename(input_path)
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)

    try:
        if use_gfpgan and face_enhancer:
            _, _, output = face_enhancer.enhance(
                img, has_aligned=False, only_center_face=False, paste_back=True
            )
        else:
            output, _ = upsampler.enhance(img, outscale=upscale)
    except Exception as e:
        print(f"Enhancement failed: {e}")
        output = img

    save_name = f"{os.path.splitext(img_name)[0]}_{suffix}.png"
    save_path = os.path.join(output_dir, save_name)
    imwrite(output, save_path)
    print(f"Enhanced image saved to {save_path}")
