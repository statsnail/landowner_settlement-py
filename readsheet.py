#!/usr/bin/env python3

import sys
import csv

month = "november17"

def app():
    print("Reading the sheet...")

    with open(month+".csv", 'w', newline='') as f:
        writer = csv.writer(f)
        csv_header = 'pid','firstname','lastname','bankaccount', 'pickings', 'cost_per_session', 'total_payout' 
        writer.writerow(csv_header)
        print("Month", month)
        payout = 0
        with open('landowners_master.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    val = int(row[month])
                    if val > 0:
                        pricepersession = int(row['cost_per_session'])
                        #totalprice = pricepersession*int(row[week])
                        if row['bankaccount'] != '':
                            rowtext = row['pid'], row['firstname1'], row['lastname1'], row['bankaccount'], val, row['cost_per_session'], pricepersession*val
                            print(rowtext)
                            writer.writerow(rowtext)
                            payout = payout + pricepersession*val
                        else:
                            print("Line skipped, bank account was null for: ", row['pid'], row['firstname1'], row['lastname1'], row['bankaccount'], val, pricepersession*val)

                    #else:
                        #print("Line skipped, picked 0 times")
                except ValueError:
                    print("Line skipped, picked N/A times")
        print("End of month, payout =", payout)
        print()

if __name__ == '__main__':
    app()
