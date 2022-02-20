import click
import os
from extractors.barclays_extractor import BarclaysExtrctor
from extractors.bb_extractor import BBExtractor
from extractors.itau_extractor import ItauExtractor

@click.command()
@click.argument("bank")
@click.option("--out_dir", "-o", type=str, default=os.path.join(".","output"))
@click.option("--pdf_dir", "=p", type=str, default=None, multiple=True)
def extract(bank, out_dir, pdf_dir):

  if pdf_dir == None:
    print('You need to inform the path to at least 1 pdf file')
  elif bank == 'itau':
    ItauExtractor(out_dir, pdf_dir).generateCSV()
  elif bank == 'banco_do_brasil':
    BBExtractor(out_dir, pdf_dir).generateCSV()
  else:
    print('wtf')
