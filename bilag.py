#!/usr/bin/python3

import os

from reportlab.lib import colors
from reportlab.graphics.barcode.code128 import *
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.paragraph import Paragraph
from reportlab.graphics.barcode import getCodes, getCodeNames, createBarcodeDrawing, createBarcodeImageInMemory

logo = ImageReader('logo_505x448.png')
sign = ImageReader('sign_200x41.png')

def generate_bilag(property_id, firstname, lastname, sessions, cost_per_session, total_payout, account, saveto):
  styles = getSampleStyleSheet()
  styleN = styles['Normal']

  print('Creating PDF for property_id', property_id)

  leftMargin = 25*mm
  topMargin = 270*mm

  c = Canvas(saveto,pagesize=A4) # See constructor for more
  c.setAuthor('Statsnail AS')
  c.setTitle('Bilag 2018')
  c.setSubject('Bilag for utbetaling av høstekompensasjon utført i 2018')

  # X, Y is bottom left when 0, 0, but we translated it to top left.
  c.translate(leftMargin, topMargin)

  c.drawImage(logo, 0, -80*mm, width=80, preserveAspectRatio=True, mask='auto')

  c.setFont('Helvetica-Bold', 12)
  c.drawString(0,-20*mm, 'Bilag høsting på eiendom sesong 2018')
  c.setFont('Helvetica', 10)
  c.drawString(0,-(20*mm+(2*7*mm)), 'Gjelder høsting på Deres eiendom sesongen 2018.')

  c.drawString(0,-(20*mm+(4*7*mm)), 'Eier: '+firstname+' '+lastname)
  
  session_string = '%s økter a %s NOK per økt' % (sessions, cost_per_session)
  c.drawString(0,-(20*mm+(5*7*mm)), 'Antall plukkeøkter: '+session_string)

  c.drawString(0,-(20*mm+(6*7*mm)), 'Gjelder eiendom: '+property_id)

  sum_string = '%s NOK eks MVA' % (total_payout)
  c.drawString(0,-(20*mm+(7*7*mm)), 'Total sum: '+sum_string)

  account_string = '%s' % (account)
  c.drawString(0,-(20*mm+(8*7*mm)), 'Deres konto: '+account_string)

  c.drawString(0,-(20*mm+(10*7*mm)), 'Overført fra Statsnail AS konto 4212 21 17590 til Deres konto, takk for samarbeidet.')
  
  c.drawString(0,-(20*mm+(12*7*mm)), 'På vegne av Statsnail AS og alle ansatte,')

  c.drawImage(sign, 0, -(20*mm+(13*7*mm)), width=200, preserveAspectRatio=True, mask='auto')

  c.line(0,-(20*mm+(13*7*mm)), 200,-(20*mm+(13*7*mm)))

  c.drawString(0,-(20*mm+(14*7*mm)), 'Joakim Skjefstad')
  c.drawString(0,-(20*mm+(15*7*mm)), 'Daglig leder, Statsnail AS')
  c.drawString(0,-(20*mm+(16*7*mm)), 'Telefon: 0047 91752214   Epost: joakim@statsnail.com')

  c.showPage()

  try:
    c.save()
  except FileNotFoundError as err:
    print('ERROR, FileNotFoundError', err)
    #os.makedirs(saveto)
    raise
  except:
    print('Unknown error during save')
    raise

  options = {}
  options['width'] = 300
  options['height'] = 150
  options['isoScale'] = 1



if __name__ == '__main__':
  print('This is a module, call generate_bilag() from somewhere else')
  exit()