import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
import pkg_resources
import tempfile
import webbrowser
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
from PIL import Image

# Check for required packages
required_packages = ['pycryptodomex', 'pillow']
for package in required_packages:
    try:
        pkg_resources.get_distribution(package)
    except pkg_resources.DistributionNotFound:
        print(f"{package} is not installed. Installing...")
        subprocess.check_call(['pip', 'install', package])

def project_info():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Project Information</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f2f2f2;
            }
            h1 {
                font-size: 36px;
                margin-bottom: 30px;
                color: "red";
                text-align: center;
            }
            p {
                font-size: 18px;
                line-height: 1.5;
                margin-bottom: 20px;
                color: #333;
                text-align: center;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                background-color: #fff;
                text-align: center;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
            }
        </style>
    </head>
    <body>
        <p>This Project was developed by <b>Anonymous</b> as part of a <b>Cyber Security Internship.</b> This project is designed to <b>Secure Organizations in the Real World from Cyber Frauds performed by Hackers.</b></p>
        <br>
        <h1 style="color:green">Project Details</h1>
        <br><br>
        <table>
            <tr>
                <td>Project Name</td>
                <td>Implementing secured Encryption Standards for images which contain secured data</td>
            </tr>
            <tr>
                <td>Project Start Date</td>
                <td>22-SEP-2024</td>
            </tr>
            <tr>
                <td>Project End Date</td>
                <td>02-NOV-2024</td>
            </tr>
            <tr>
                <td>Project Status</td>
                <td>Completed</td>
            </tr>
        </table>
        <h1 style="color:red">Developer Details</h1>
        <br><br>
        <table>
            <tr>
                <th>Name</th>
                <th>Employee ID</th>
                <th>Email</th>
            </tr>
            <tr>
                <td>K.Naga Susmitha</td>
                <td>ST#IS#6453</td>
                <td>kancharlanagasusmitha@gmail.com</td>
            </tr>
            <tr>
                <td>S.Nandini</td>
                <td>ST#IS#6460</td>
                <td>sunkaranandini22@gmail.com</td>
            </tr>
            <tr>
                <td>P.Swarna</td>
                <td>ST#IS#6481</td>
                <td>swarnapuligadda1015@gmail.com</td>
            </tr>
            <tr>
                <td>SK.Aarshiya Begum</td>
                <td>ST#IS#6480</td>
                <td>shaikarshiyabegam18@gmail.com</td>
            </tr>
            <tr>
                <td>SK.Saafiya</td>
                <td>ST#IS#6430</td>
                <td>saafiyad@gmail.com</td>
            </tr>
            <tr>
                <td>N.Kalyani</td>
                <td>ST#IS#6478</td>
                <td>nuthikattu2002@gmail.com</td>
            </tr>
            <tr>
                <td>P.Sailaja</td>
                <td>ST#IS#6473</td>
                <td>sailajareddypondugula@gmail.com</td>
            </tr>
        </table>
        <br><br><br>
        <h1 style="color:green">Company Details</h1>
        <br><br>
        <table>
            <tr>
            <th>Company</th>
            <th>Email</th>
            </tr>
            <tr>
                <td>Supraja Technologies</td>
                <td>contact@suprajatechnologies.com</td>
            </tr>
        </table>
    </body>
    </html>"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as temp_file:
        temp_file.write(html_code)
        temp_file_path = temp_file.name
    webbrowser.open('file://' + os.path.realpath(temp_file_path))

def encrypt_image():
    file_path = filepath_entry.get()
    password = password_entry.get()

    if not file_path:
        messagebox.showerror("Error", "Please select a file to encrypt.")
        return

    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Invalid file path.")
        return

    try:
        img = Image.open(file_path)
        if img.format not in ["PNG", "JPEG"]:
            messagebox.showerror("Error", "Please select a PNG or JPEG image to encrypt.")
            return
    except IOError:
        messagebox.showerror("Error", "The file may be already encrypted or is not a valid image file.")
        return

    valid_lengths = [16, 24, 32]
    if (len(password) not in valid_lengths or
        not any(char.isdigit() for char in password) or
        not any(char.isupper() for char in password) or
        not any(char in "!@#$%^&*()_+-=[]{};':\"\\,.<>/?~" for char in password)):
        messagebox.showerror("Error", 
                              "Password should be at least 16, 24, or 32 characters long and should contain at least one capital letter, one digit, and one special character.")
        return

    key = password.encode()
    iv = get_random_bytes(16)

    with open(file_path, 'rb') as f:
        image_data = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(image_data, AES.block_size))

    with open(file_path, 'wb') as f:
        f.write(iv + encrypted_data)

    messagebox.showinfo("Info", "Image encrypted successfully.")

def decrypt_image():
    file_path = filepath_entry.get()
    password = password_entry.get()

    if not file_path:
        messagebox.showerror("Error", "Please select a file to decrypt.")
        return

    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Invalid file path.")
        return

    valid_lengths = [16, 24, 32]
    if (len(password) not in valid_lengths or
        not any(char.isdigit() for char in password) or
        not any(char.isupper() for char in password) or
        not any(char in "!@#$%^&*()_+-=[]{};':\"\\,.<>/?~" for char in password)):
        messagebox.showerror("Error", 
                              "Password should be at least 16, 24, or 32 characters long and should contain at least one capital letter, one digit, and one special character.")
        return

    key = password.encode()

    with open(file_path, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()

    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        with open(file_path, 'wb') as f:
            f.write(decrypted_data)

        messagebox.showinfo("Info", "Image decrypted successfully.")
    except (ValueError, KeyError) as e:
        messagebox.showerror("Error", "Decryption failed. Invalid password or corrupted file.")

# Setting up the GUI
root = tk.Tk()
root.title("Image Encryption and Decryption")

# File Path
title_label = tk.Label(root, text="Image Encryption Project",bg="red", font=("Helvetica", 16))
title_label.pack(pady=10)
filepath_entry = tk.Entry(root, width=50)
filepath_entry.pack(pady=5)

tk.Button(root, text="Browse", command=lambda: filepath_entry.insert(0, filedialog.askopenfilename())).pack(pady=5)

# Password
tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show='*', width=50)
password_entry.pack(pady=5)

# Buttons
tk.Button(root, text="Project Info", bg="blue", command=project_info).pack(pady=10)
tk.Button(root, text="Encrypt Image", bg="skyblue", command=encrypt_image).pack(pady=10)
tk.Button(root, text="Decrypt Image", bg="green", command=decrypt_image).pack(pady=10)

root.mainloop()
