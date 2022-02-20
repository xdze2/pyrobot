import cv2


def load_image(img_path):
    image = cv2.imread(str(img_path))
    return image


def save_image(ouput_path, image):
    cv2.imwrite(str(ouput_path), image)
    print(f"Image saved to {ouput_path}")
