from PIL import Image

def crop_image(inf_result_vec, source_image_path):
    source_image = Image.open(source_image_path)

    cropped_image = source_image.crop((inf_result_vec[0], 
                        inf_result_vec[1], 
                        inf_result_vec[2], 
                        inf_result_vec[3]))
    return cropped_image

def save_image(image, destination_path):
    source_image = image.save(destination_path)