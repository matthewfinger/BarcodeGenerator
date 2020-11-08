# BarcodeGenerator
A simple gui program that generates a pdf of barcodes to be printed onto label paper

This project was created for use in a retail environment to be able to print barcodes, based on a list of upcs, onto an Avery 8167/5167 label template.
As it is currently, the program will only work fully on Windows, and make sure you have an accessible way to view PDF files, and an Internet connection is also required

To use:
  1) Clone the project, and make sure you have the following dependencies installed (Sorry, venv coming soon):
    - PIL : python image library
    - requests
    - FPDF
    
  2) Run the main.py file in the root directory
