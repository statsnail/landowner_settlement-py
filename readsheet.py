#!/usr/bin/env python3

import sys
import csv
import re

inputfile = 'landowners_master - landowners_sheet.csv'
outputfile = 'output.csv'

pattern_pid = re.compile("^([0-9][0-9][0-9][0-9]-[0-9]+/[0-9]+)$") # regexp used for sanity check of property id "1000-12/3"
pattern_account = re.compile("^([0-9]{11})$|^$") # regexp used for sanity check of account "42900604620" OR ""

class Error(Exception):
    pass

class CustomError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

def app():
    print("Reading the sheet...")

    with open(outputfile, 'w', newline='') as f:
        writer = csv.writer(f)
        csv_header = 'pid','firstname','lastname','email','bankaccount', 'pickings', 'cost_per_session', 'total_payout' 
        writer.writerow(csv_header)

        year_payout = 0
        year_sessions = 0
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

                if row['region'] == '### ENDLINE ###':
                    print(row_index, 'Found endline row, now exiting loop')
                    break

                if row['skip'] == 'x':
                    print(row_index, 'Skipping row, reason: skip column = x')
                    continue

                pid = row['pid']
                firstname1 = row['firstname1']
                lastname1 = row['lastname1']
                email1 = row['email1']
                bankaccount = row['bankaccount']

                try:
                    totalsessions = int(row['total18'])
                    cost_per_session = int(row['cost_per_session'])

                except ValueError as err:
                    print('ERROR: ValueError')
                    print(err)
                    print('row_index = ', row_index)
                    print(row)
                
                except:
                    print('ERROR: Unexpected error')
                    raise

                try:
                    # Sanity check of property id
                    if not pattern_pid.match(pid):
                        print(row_index, pid)
                        raise CustomError('ERROR', 'Property ID is not valid')

                    # Sanity check of bank account. Both Norwegian account and Empty is ok
                    if not pattern_account.match(bankaccount):
                        print(row_index, bankaccount)
                        raise CustomError('ERROR', 'Account is not valid')
                
                except:
                    print('ERROR: Unexpected error')
                    raise

                if totalsessions == 0:
                    line_new = '{:<3} {:<12} {:<20} {:<20} {:<30} {:<12} {:>2}*{:>2} # NO HARVESTS'.format(row_index, pid, firstname1, lastname1, email1, bankaccount, totalsessions, cost_per_session)
                    print(line_new)
                else:
                    if bankaccount == '':
                        line_new = '{:<3} {:<12} {:<20} {:<20} {:<30} {:<12} {:>2}*{:>2} # BANK ACCOUNT MISSING'.format(row_index, pid, firstname1, lastname1, email1, bankaccount, totalsessions, cost_per_session)
                        print(line_new)
                        #print(row_index, pid, firstname1, lastname1, bankaccount, totalsessions, cost_per_session)
                        year_sessions = year_sessions+totalsessions
                        year_payout = year_payout + (totalsessions*cost_per_session)
                    else:
                        line_new = '{:<3} {:<12} {:<20} {:<20} {:<30} {:<12} {:>2}*{:>2}'.format(row_index, pid, firstname1, lastname1, email1, bankaccount, totalsessions, cost_per_session)
                        print(line_new)
                        rowtext = pid, firstname1, lastname1, email1, bankaccount, totalsessions, cost_per_session, totalsessions*cost_per_session
                        writer.writerow(rowtext)

                        year_sessions = year_sessions+totalsessions
                        year_payout = year_payout + (totalsessions*cost_per_session)

                #if '' in pid:
                #    print(idx, 'Property does not exist, considered invalid')

                #print(pid, "pickings", totalsessions)

                #if row['bankaccount'] != '':
                #    outputrowtext = row['pid'], row['firstname1'], row['lastname1'], row['bankaccount'], totalsessions, row['cost_per_session'], cost_per_session*totalsessions
                #    writer.writerow(outputrowtext)
                #else:
                #    print('Bank account missing')

                
                #if totalsessions > 0:
                #    pricepersession = int(row['cost_per_session'])
                    #totalprice = pricepersession*int(row[week])
                #    if row['bankaccount'] != '':
                #        rowtext = row['pid'], row['firstname1'], row['lastname1'], row['bankaccount'], val, row['cost_per_session'], pricepersession*val
                #        print(rowtext)
                #        writer.writerow(rowtext)
                #        payout = payout + pricepersession*val
                #    else:
                #        print("Line skipped, bank account was null for: ", row['pid'], row['firstname1'], row['lastname1'], row['bankaccount'], val, pricepersession*val)

                #else:
                    #print("Line skipped, picked 0 times")

                #print(str.encode(pid))
        print("End of year, payout =", year_payout, ' sessions =', year_sessions)
        print()

if __name__ == '__main__':
    app()
