#!/usr/bin/env python3

import sys
import csv
import re

import bilag

inputfile = 'output.csv'

pattern_pid = re.compile("^([0-9][0-9][0-9][0-9]-[0-9]+/[0-9]+)$") # regexp used for sanity check of property id "1000-12/3"
pattern_account = re.compile("^([0-9]{11})$") # regexp used for sanity check of account "42900604620"
pattern_email = re.compile("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$") # regexp used for sanity check of email "blabla@eoeeoe.com"

class Error(Exception):
    pass

class CustomError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

def app():
    print("Reading the sheet...")

    with open(inputfile) as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.DictReader(csvfile) # reads the header line first, so they are accessible later on
        row_count = sum(1 for row in reader)  # fileObject is your csv.reader
        print('Number of data rows is ', row_count)

        csvfile.seek(0)

        if has_header:
            next(reader)
        else:
            raise CustomError("ERROR", "No header in csv input!")

        for idx,row in enumerate(reader):
            row_index = idx+1
            pid = row['pid']
            pid_simple = pid.replace('/', '_')
            pid_simple = pid_simple.replace('-', '_')
            savetofilename = pid_simple+'.pdf'
            email = row['email']
            if not pattern_email.match(email):
                print('email not valid ', email)
                savetofilename = 'letter'+savetofilename
            else:
                print('email is valid ', email)
                savetofilename = 'email'+savetofilename

            print(row_index, pid_simple)
            bilag.generate_bilag(property_id=pid, firstname=row['firstname'], lastname=row['lastname'], sessions=row['pickings'], cost_per_session=row['cost_per_session'], total_payout=row['total_payout'], account=row['bankaccount'], saveto=savetofilename)


if __name__ == '__main__':
    app()
