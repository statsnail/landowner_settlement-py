#!/usr/bin/env python3

import pdb
import sys, inspect
import api as api
from datetime import datetime, timedelta, date
import time
from pytz import timezone
import random
import csv

input_csv = "output.csv"

payments = []

class Payment:
    def __init__(self, pid, firstname, surname, bankaccount, pickings, cost_per_session, total_payout):
        self.pid = pid
        self.firstname = firstname
        self.surname = surname
        self.bankaccount = bankaccount
        self.pickings = pickings
        self.cost_per_session = cost_per_session
        self.total_payout = total_payout
    def __str__(self):
        return " ".join(["Payment line:", self.pid, self.firstname, self.surname, self.bankaccount, str(self.pickings), str(self.cost_per_session), str(self.total_payout)])


def make_CdtTrfTxInf(payment):

    # ISO sier 140 characters, men SMN Melding linje 1 er MAKS 40 TEGN!
    add_Ustrd = "Statsnail:" + "#" + payment.pickings + ":pid" + payment.pid
    Nm = payment.firstname + " " + payment.surname
    Id = payment.bankaccount
    valueOf_ = str(payment.total_payout)

    _CdtTrfTxInf = api.CreditTransferTransactionInformation10()
    the_random_identifier = get_random_identifier("snailb")
    _CdtTrfTxInf.set_PmtId(api.PaymentIdentification1(InstrId=the_random_identifier,EndToEndId=the_random_identifier))
    _CdtTrfTxInf.set_PmtTpInf(api.PaymentTypeInformation19(InstrPrty="NORM"))
    _CdtTrfTxInf.set_Amt(api.AmountType3Choice(InstdAmt=api.ActiveOrHistoricCurrencyAndAmount(Ccy="NOK", valueOf_=valueOf_)))
    _CdtTrfTxInf.set_Cdtr(api.PartyIdentification32(Nm=Nm, PstlAdr=api.PostalAddress6(StrtNm=" ", PstCd=" ", TwnNm=" ", Ctry="NO")))
    _CdtTrfTxInf.set_CdtrAcct(api.CashAccount16(Id=api.AccountIdentification4Choice(Othr=api.GenericAccountIdentification1(Id=Id, SchmeNm=api.PersonIdentificationSchemeName1Choice(Cd="BBAN")))))
    _RmtInf = api.RemittanceInformation5()
    _RmtInf.add_Ustrd(add_Ustrd)
    _CdtTrfTxInf.set_RmtInf(_RmtInf)
    return _CdtTrfTxInf

def make_PmtInf(payment):
    _PmtInf = api.PaymentInstructionInformation3(ReqdExctnDt=date.today().isoformat())
    _PmtInf.set_PmtInfId(get_random_identifier("pmt_snaila")) #Max35Text
    _PmtInf.set_PmtMtd("TRF") #PaymentMethod3Code
    _PmtInf.set_NbOfTxs("1") #Max15NumericText
    _PmtInf.set_CtrlSum(int(payment.total_payout)) #DecimalNumber
    _PmtInf.set_PmtTpInf(api.PaymentTypeInformation19(InstrPrty="NORM"))
    #pdb.set_trace()
    #PmtInf.set_ReqdExctnDt("1996-10-11") # Here be dragons
    #print(PmtInf.get_ReqdExctnDt())
    _PmtInf.set_Dbtr(api.PartyIdentification32(Nm="Statsnail AS", PstlAdr=api.PostalAddress6(Ctry="NO")))
    _PmtInf.set_DbtrAcct(api.CashAccount16(Id=api.AccountIdentification4Choice(Othr=api.GenericAccountIdentification1(Id="42122117590", SchmeNm=api.PersonIdentificationSchemeName1Choice(Cd="BANK"))), Ccy="NOK"))
    _PmtInf.set_DbtrAgt(api.BranchAndFinancialInstitutionIdentification4(FinInstnId=api.FinancialInstitutionIdentification7(BIC="SPTRNO22XXX")))
    
    _PmtInf.add_CdtTrfTxInf(make_CdtTrfTxInf(payment)) #CreditTransferTransactionInformation10
    
    return _PmtInf

def get_random_identifier(addit):
    """Returns a random identifier"""     
    utcdate = time.strftime('%Y%m%d', time.gmtime(time.time()))
    randint = random.randrange(1000)
    return '%s.%s.%s' % (addit, utcdate, randint)

def app(payments_to_process):
    print("Using the api...")
    print("Today: ", date.today().isoformat())

    doc = api.Document()
    ccti = api.CustomerCreditTransferInitiationV03()

    msgid = get_random_identifier("msg_snail")
    grphdr = api.GroupHeader32(MsgId=msgid,CreDtTm=datetime.utcnow().replace(microsecond=0).isoformat(), NbOfTxs=str(len(payments_to_process)))
    the_id_orgid_othr = api.GenericOrganisationIdentification1(Id="915109012")
    the_id_orgid_othr.set_SchmeNm(api.OrganisationIdentificationSchemeName1Choice(Cd="CUST"))
    the_id_orgid = api.OrganisationIdentification4()
    the_id_orgid.add_Othr(the_id_orgid_othr)
    the_id = api.Party6Choice(OrgId=the_id_orgid)
    initgpty = api.PartyIdentification32(Nm="Statsnail AS", Id=the_id)
    grphdr.set_InitgPty(initgpty)
    
    ccti.set_GrpHdr(grphdr)
    

    for payment in payments_to_process:
        ccti.add_PmtInf(make_PmtInf(payment)) # Add one payment
    
    doc.set_CstmrCdtTrfInitn(ccti)
    #pdb.set_trace()
    filetest = open("output.xml",'w')
    doc.export(outfile=filetest, level=0)
    filetest.close()
    
if __name__ == '__main__':
    #pdb.run('app()')
    #app()
    with open(input_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            payments.append(Payment(row['pid'],row['firstname'],row['lastname'], row['bankaccount'], row['pickings'], row['cost_per_session'] ,row['total_payout']))
        for payment in payments:
            print(payment)
        app(payments)