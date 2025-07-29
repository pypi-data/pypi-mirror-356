def ft_load(path: str) -> array:
    """
    Load an image file and return its content.
    
    :return: The content of the image file.
    """
    import os
    from numpy import array
    from PIL import Image    
    
    if not os.path.exists(path):
        print("File not found.")
        return None
    with Image.open(path) as img:
        img_array = array(img)
    print(f"The shape of image is: {img_array.shape}")
    return img_array