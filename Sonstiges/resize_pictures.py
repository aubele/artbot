import cv2
import os
import sys


def resize_images_from_folder(folder, limit):
    """
    Resizes all Pictures in a given folder based on a limit.

    Parameters:
    folder(string): the path to the folder that contains the pictures
    limit(int): the limit for the pixels to resize to

    Returns:
    None
    """
    limit = limit
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        img = cv2.imread(path)
        if img is not None:
            shape = img.shape
            if shape[0] > limit and shape[1] > limit:
                if shape[0] <= shape[1]:
                    print(shape)
                    factor = shape[1]/limit
                    print(factor)
                    new_width = shape[0] / factor
                    new_height = shape[1] / factor
                    dim = (int(new_height), int(new_width))
                    print(dim)
                    resized_img = cv2.resize(img, dim, factor, factor, cv2.INTER_CUBIC)
                    save_picture(folder, filename, resized_img)
                else:
                    print(shape)
                    factor = shape[0]/limit
                    print(factor)
                    new_width = shape[0] / factor
                    new_height = shape[1] / factor
                    dim = (int(new_height), int(new_width))
                    print(dim)
                    resized_img = cv2.resize(img, dim, factor, factor, cv2.INTER_CUBIC)
                    save_picture(folder, filename, resized_img)
            else:
                save_picture(folder, filename, img)



def save_picture(folder, filename, picture):
    """
    Saves the resized picture to a new folder.

    Parameters:
    folder(string): the string to the starting folder
    filename(string): the name of the destination file
    picture(OpenCV image): the picture

    Returns:
    None
    """
    folder = folder + "/resize"
    try:
        os.mkdir(folder)
        print("Directory " + folder + " created!")
    except FileExistsError:
        print()
    cv2.imwrite(os.path.join(folder, filename), picture)


if __name__ == '__main__':
    #resize_images_from_folder("D:/nc/Documents/Master_Informatik_Studium/4.Semester WS 1920/KI/test")
    #resize_images_from_folder("E:/extracted/pictures")
