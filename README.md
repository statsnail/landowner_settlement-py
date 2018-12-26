# landowner_settlement-py

Program suite to read Google Sheets file over landowners, process this to a payment XML file according to the SEPA Payment Initiation Format.

Uses an API made by feeding generateDS the xml schema for pain.001.001.03.

Requires a handful of different modules, including reportlab for PDF generation.


Step 1: Read over Google Sheet document online, fix any errors

Step 2: Run Google Sheet as CSV through readsheet.py program

Step 3: Run make_xml.py on output.csv to build payment file, output is output.xml

Step 3.5: Add valid header to file according to pain.001.001.03 to output.xml

Step 4: Upload payment file to bank

Step 5: Verify and authorize payment

Step 6: Generate PDF for payments using makeallbilag.py with input output.csv

Step 7: Send all marked "letter" as physical letter, send all marked "email" as email, using another program maybe

TL;DR:

python3 readsheet.py
python3 make_xml.py
python3 makeallbilag.py