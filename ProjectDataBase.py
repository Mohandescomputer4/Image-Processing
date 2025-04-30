# import Packages 

# use their Engine For Proccessing An Image
import pytesseract

# parsing Characters
import argparse

# Use Features of Open-CV For Processing and Detection Of Image
import cv2

# use Pillow for work on image
from PIL import Image

# use exif property pf image -> (GPS COORDINATION)
import piexif

# use sqlite3 Database
import sqlite3

# OCR function
def ocr_image(image_path, digits_only=True):

    # load the input image, convert it from BGR to RGB channel ordering,
    # Read Image
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # initialize our Tesseract OCR options
    # check to see if *digit only* OCR should be performed, and if so,
    # update our Tesseract OCR options
    options = "outputbase digits" if digits_only else ""
    text = pytesseract.image_to_string(rgb, config=options)

    # return context of image
    return text.strip()

# Extracts latitude and longitude from an image's EXIF data
def get_lat_lon(image_path):

    # load image and Set gps dictionary
    exif_dict = piexif.load(image_path)
    gps_info = exif_dict['GPS']


    """
        Converts degrees, minutes, and seconds to decimal degrees.

        Args:
            dms (tuple): A tuple containing degrees, minutes, and seconds.
            ref (str): Reference direction ('N', 'S', 'E', or 'W').

        Returns:
            float: Decimal degrees.
    """
    def dms_to_dd(dms, ref):
        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1]
        seconds = dms[2][0] / dms[2][1] / 100
        dd = degrees + minutes / 60 + seconds / 3600
        if ref in ['S', 'W']:
            dd = -dd
        return dd

    lat = dms_to_dd(gps_info[piexif.GPSIFD.GPSLatitude], gps_info[piexif.GPSIFD.GPSLatitudeRef])
    lon = dms_to_dd(gps_info[piexif.GPSIFD.GPSLongitude], gps_info[piexif.GPSIFD.GPSLongitudeRef])

    return lat, lon

# clearing the name of Machines, Removing Extension of filename
def extract_name_without_extension(filename):

    # Remove the file extension (assuming it's always after the last dot)
    name_without_extension = filename.rsplit('.', 1)[0]
    return name_without_extension


# Database setup function
def setup_database():

    # setup and connect to Databese
    conn = sqlite3.connect('MachinesInformation.db')
    c = conn.cursor()
    
    # sqlite Query for Create/Use DataBase
    c.execute('''CREATE TABLE IF NOT EXISTS machines
                 (name TEXT, serial_number TEXT, location TEXT)''')
    conn.commit()
    return conn, c

# Function to insert data into the database
def insert_into_database(conn, c, name, serial_number, location):

    # splite Query For Add To DataBase
    c.execute("INSERT INTO machines (name, serial_number, location) VALUES (?, ?, ?)",
              (name, serial_number, location))
    conn.commit()

# Function to Remove data into the database
def remove_from_database(conn, c, name):

    # splite Query For Remove To DataBase
    c.execute("DELETE FROM machines WHERE name = ?", (name,))
    conn.commit()

# Main function
def main():

    # Set up the database connection
    conn, c = setup_database()

    # Argument parsing
    parser = argparse.ArgumentParser(description="Process machine information")
    parser.add_argument("-i", "--image", help="path to input image to be OCR'd")
    parser.add_argument("-d", "--digits", type=int, default=1, help="whether or not *digits only* OCR will be performed")
    parser.add_argument("-r", "--remove", nargs="+", help="Remove records with specified names from the database")
    args = parser.parse_args()

    # Handle removal of records
    if args.remove:
        for name in args.remove:
            remove_from_database(conn, c, name)
            print(f"{name} Removed Successfully")
    else:
        # Process image information
        if args.image:
            image_path = args.image
            digits_only = args.digits > 0
		
            # Set the name of machine without Extension of Image
            machine_name = extract_name_without_extension(image_path.split("/")[-1])

	    # Recognize the number of that locate in image
            serial_number = ocr_image(image_path, digits_only)

	    # show latitide and Longitude of Image
            try:
                lat, lon = get_lat_lon(image_path)
                location = f"Latitude: {lat}, Longitude: {lon}"
            except KeyError:
                location = "No GPS data available"

	    # insert New Data To DataBase
            insert_into_database(conn, c, machine_name, serial_number, location)

	    # print the log
            print(f"Name: {machine_name}")
            print(f"Serial Number: {serial_number}")
            print(f"Location: {location}")
        else:
            print("Please provide an --image or use the --remove option.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()