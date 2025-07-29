from numpy import array

def ft_load(path: str) -> array:
    """
    Load an image file and return its content.
    
    :return: The content of the image file.
    """
    import os
    from PIL import Image    
    
    if not os.path.exists(path):
        print("File not found.")
        return None
    with Image.open(path) as img:
        img_array = array(img)
    return img_array