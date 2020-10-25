import pandas as pd
import database_api
import os
from shutil import copy
import cv2
from matplotlib import pyplot as plt

# dict with 20 artists and their births
famous_artists20 = {
    "Vincent van Gogh": "1853-03-30",
    "Paul Gauguin": "1848-06-07",
    "Claude Monet": "1840-11-14",
    "Edouard Manet": "1832-01-23",
    "Paul Cezanne": "1839-01-19",
    "Pierre-Auguste Renoir": "1841-02-25",
    "Pablo Picasso": "1881-10-25",
    "Edgar Degas": "1834-07-19",
    "Leonardo da Vinci": "1452-04-15",
    "Rembrandt": "1606-07-15",             #Rembrandt Harmenszoon van Rijn
    "Sandro Botticelli": "1445-03-01",
    "Peter Paul Rubens": "1577-06-28",
    "Michelangelo": "1475-03-06",          #Michelangelo Buonarroti
    "Francisco Goya": "1746-03-30",        #Francisco José de Goya y Lucientes
    "Gustave Courbet": "1819-06-10",       #Jean Désiré Gustave Courbet
    "Salvador Dali": "1904-05-11",         #Salvador Felipe Jacinto Dalí i Domènech
    "Henri de Toulouse-Lautrec": "1864-11-24",       #Henri Marie Raymond de Toulouse-Lautrec-Monfa
    "Marc Chagall": "1887-07-07",
    "Caravaggio": "1571-09-29",            #Michelangelo Merisi
    "Eugene Delacroix": "1798-04-26"}                 #Ferdinand Victor Eugène Delacroix

# dict with 10 artists and their births
famous_artists10 = {
    "Vincent van Gogh": "1853-03-30",
    "Claude Monet": "1840-11-14",
    "Edouard Manet": "1832-01-23",
    "Pierre-Auguste Renoir": "1841-02-25",
    "Pablo Picasso": "1881-10-25",
    "Leonardo da Vinci": "1452-04-15",
    "Rembrandt": "1606-07-15",             #Rembrandt Harmenszoon van Rijn
    "Sandro Botticelli": "1445-03-01",
    "Michelangelo": "1475-03-06",          #Michelangelo Buonarroti
    "Salvador Dali": "1904-05-11"}         #Salvador Felipe Jacinto Dalí i Domènech

#dict with 1 artist and his birth
test_artist = {"Sandro Botticelli": "1445-03-01"}     #lowest number of pictures

def csv_in_db(path):
    """
    Takes the all_data_info.csv and fills the database based on the famous_artists. Therefor it saves the
    information of the artist (name and birth) to the corresponding table in the database. Moreover it saves
    every picture including all the information (filename, title, genre, epoch, artist) and the picture itself
    to the corresponding table in the database.

    Parameters:
    path(string): the string to the all_data_info.csv file that contains all information

    Returns:
    None
    """
    artist_set = famous_artists20
    df = pd.read_csv(path + "/all_data_info.csv")
    part_df = df.loc[df['artist'].isin(artist_set.keys())]

    unique_artists = part_df.artist.unique()
    print(unique_artists)
    print(list(set(artist_set.keys()) - set(unique_artists)))
    print(part_df.shape)

    part_df = part_df.drop(columns=['date','pixelsx','pixelsy','size_bytes','source','artist_group','in_train'])

    titles = []
    artists = []

    for artist in artist_set:
        name = artist
        birth = artist_set[artist]
        database_api.insert_artist(name, birth)
        all_artist_rows = part_df[part_df.artist == artist]
        #selected_pictures = all_artist_rows.sample(5)
        selected_pictures = all_artist_rows.head(10)
        picture_count = 0
        for index, row in selected_pictures.iterrows():
            filename = row.new_filename
            #picture = open_and_convert_picture(filename)
            title = adjust_title(row.title)
            if convert_to_txt(title) in titles:
                continue
            epoch = row.style
            genre = row.genre
            database_api.insert_picture(filename, title, artist, epoch, genre)
            titles.append(convert_to_txt(title))
            file_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(file_dir)
            dest = os.path.join(parent_dir, "ArtBotGUI")
            dest = os.path.join(dest, "static")
            dest = os.path.join(dest, "art")
            file = os.path.join("E:/extracted/resize_500/" + filename)
            copy_picture_to_folder(file, dest)
            picture_count += 1
            if picture_count == 5:
                break
        print(artist, " finished with " + str(picture_count) + " pictures!")
        artists.append(convert_to_txt(artist))
    save_list_to_txt(titles, "titles")
    save_list_to_txt(artists, "artist")


#check if title contains " and delete it, replace () with - in first place
def adjust_title(title):
    """
    adjustes the title of the picture, so that it doesn´t contain " and replace () with - in first place and deletes
    the second one.

    Parameters:
    title(string): the picturetitle that has to be changed

    Returns:
    title(string): the adjusted title
    """
    title = title.strip()
    title = title.replace("\"", "")
    title = title.replace("(", "- ")
    title = title.replace(")", "")
    return title


def open_and_convert_picture(file_name):
    """
    Opens a picture from a file and returns it as binary data.

    Parameters:
    file_name(string): the name of the picture

    Returns:
    blob(bytes): the bytes representation of the picture
    """
    with open(("E:/extracted/resize_1000/" + file_name), 'rb') as file:
        blob = file.read()
        file.close()
    return blob


def display_numpy(np_arr):
    """
    Displays the numpy array as picture.

    Parameters:
    np_arr(numpy array): the picture as numpy array

    Returns:
    None
    """
    plt.imshow(cv2.cvtColor(np_arr, cv2.COLOR_BGR2RGB))
    plt.show()


def open_picture_as_numpy(blob, filename="./buffer"):
    """
    Open a BLOB out of the database as OpenCV picture.

    Parameters:
    blob(binary): Binary Picture coming from the database
    filename(string): the name for the bufferfile

    Returns:
    image(numpy array): the image as numpy array
    """
    with open(filename, 'wb') as file:
        file.write(blob)
        file.close()
    image = cv2.imread(filename)
    os.remove(filename)
    return image


def copy_picture_to_folder(source, target):
    """

    """
    try:
        copy(source, target)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unknown Error occured")


#The style has to match the following pattern: "    ~[value]"
def convert_to_txt(value):
    """
    Converts a given string to match the output format: "    ~[value]"

    Parameters:
    value(string): the input string

    Returns:
    output(string): converted string
    """
    output = "    ~[" + value + "]\n"
    return output


def save_list_to_txt(values, filename):
    """
    Saves a list of values to a txt file.

    Parameters:
    values(list): list of values that will be insterted in the file
    filename(string): name of the txt file to create

    Returns:
    None
    """
    with open("./" + filename + ".txt", "w", encoding='utf-8') as file:
        for value in values:
            file.write(value)
        file.close()


def save_all_artists_to_file():
    """
    Saves all artists from all_data_info.csv to a txt-file.

    Parameters:
    None

    Returns:
    None
    """
    artists = []
    count = 0
    df = pd.read_csv("./all_data_info.csv")
    unique_artists = df.artist.unique()
    for artist in unique_artists:
        count = count + 1
        artists.append(convert_to_txt(artist))
    print(count)
    save_list_to_txt(artists, "allartists")

if __name__ == '__main__':
    database_api.set_up_db()
    csv_in_db("E:/extracted")
    # row = database_api.get_random_picture()
    # # database_api.get_artist_birth('Vincent van Gogh')
    # # row = database_api.get_picture_by_title("A simple meal")
    # filename = row[0][0]
    # title = row[0][1]
    # epoch = row[0][2]
    # genre = row[0][3]
    # picture = row[0][4]
    # artist = row[0][5]
    # picture = open_picture_as_numpy(picture)
    # print((type(picture)))
    # print(picture.shape)
    # display_numpy(picture)
    # pictures = database_api.get_pictures_by_title("A")
    # #print(type(pictures))
    # #for picture in pictures:
    # #    print(picture[1])
    #
    # data = database_api.get_artist("p")
    # #print(type(data))
    # #print(data)
    #
    # data = database_api.get_artists_birth("Vincent van Gogh")
    # #print(type(data))
    # #print(data)
    #
    # data = database_api.get_pictures_by_title("Entrance to the Moulin de la Galette")
    # #print(type(data))
    # #for date in data:
    # #    print(date[0])
    #
    # data = database_api.get_pictures_by_artist("Pablo Picasso")
    # #print(type(data))
    # #for date in data:
    # #    print(date[1])
    #
    # data = database_api.get_random_picture()
    # #print(type(data))
    # #print(data[0][1])
    #
    # data = database_api.get_random_picture_by_artist("Leonardo da Vinci")
    # print(type(data))
    # print(data[0][1])
    #
    # data = database_api.get_all_pictures()
    # #print(type(data))
    # #for date in data:
    # #    print(date[1])
    #
    # data = database_api.get_all_artists_with_births()
    # #print(type(data))
    # #print(data)
    #
    # data = database_api.get_all_artists()
    # #print(type(data))
    # #print(data)
    #
    # data = database_api.get_picture_by_title_and_artist("Mona Lisa", "Leonardo da")
    # picture = data[0][4]
    # picture = open_picture_as_numpy(picture)
    # display_numpy(picture)
    # picture = open_and_convert_picture("1.jpg")
    # print(type(picture))
