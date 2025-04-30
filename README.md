# Image Processing and Metadata Storage for Database
This project was inspired by Dr.Malmir, whose brilliant idea laid the foundation for its development. Thanks for the insightful concept that sparked its creation!

This is a **small student project** designed to **process images** containing both **English letters** and **numbers**, extract text from them, and retrieve **geographical metadata** stored within the image. The extracted data, including *image name*, *serial number*, and *location coordinates*, are then saved into a **database**. You can also **delete specific entries** from the database using the **same program**.

### Features:
- Extracts text from images, including both numbers and letters.
- Retrieves geographical metadata stored in the image.
- Saves extracted data into a structured database.
- Supports deleting specific entries from the database using the "name" parameter.

### Example Log Output:
```py
# Print extracted data
print(f"Name: {machine_name}")
print(f"Serial Number: {serial_number}")
print(f"Location: {location}")
```

### Testing the Database:
A sample test database has been provided in this repository, which can be viewed online using [this website for View DB](https://sqliteviewer.app/) and [this website for query](https://sqliteonline.com/) or tested locally by cloning this project.

---

## Installation

Follow these steps to install and set up the project:

1. **Install Tesseract**  
   Download and install Tesseract OCR from [this link](https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe).

2. **Add Tesseract to System PATH**  
   - Search for **"Edit the system environment variables"**  
   - Open **Environment Variables**  
   - In **System Variables**, select `PATH`, click **Edit**, and add:  
     ```
     C:\Program Files\Tesseract-OCR\
     ```

3. **Set Up Tesseract in CMD**  
   ```
   tesseract = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
   pytesseract = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
   ```

4. **Install Required Python Packages**  
   ```
   pip install pytesseract pillow opencv-python argparse piexif sqlite3
   ```

💡 **Hint:** If you encounter an error during installation, refer to this [Stack Overflow post](https://stackoverflow.com/questions/46140485/tesseract-installation-in-windows).

---

## Usage

### Read Numbers from an Image:
```
python -u ProjectDataBase.py --image "path/to/image"
```

### Read Both Numbers and Letters:
```
python -u ProjectDataBase.py --image "path/to/image" --digit 0
```

### Delete Multiple Entries from the Database:
```
python -u ProjectDataBase.py --remove Apple Banana
```
- This command will delete entries named *Apple* and *Banana*.

---

## Output Example

Once an image is processed, the program extracts relevant data and displays it in the console while also saving it to the database.
