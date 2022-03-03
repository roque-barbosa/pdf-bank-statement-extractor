import io
import tempfile
from unittest.mock import DEFAULT
import tabula
import PyPDF2
# from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import pandas as pd
import os

class BradescoExtractorStreamlit():
  
  def __init__(self, outpath: str , files, output_filename: str = "output") -> None:
      self.files = files
      self.outPath = outpath
      self.tempFolder = os.path.join(".", "temp")
      self.output_filename = output_filename
    
  def generateMergedPdf(self):

    merger = PyPDF2.PdfFileMerger()
    for el in self.files:
      with open(os.path.join(self.tempFolder, "tmp-1.pdf"), 'wb') as f:
        f.write(el.read())
      merger.append(os.path.join(self.tempFolder, "tmp-1.pdf"))
      os.system(f"rm -r {str(os.path.join(self.tempFolder, 'tmp-1.pdf'))}")
    merger.write(os.path.join(self.tempFolder, "tmp_pdf.pdf"))
    
  
  def handle_data(self, dataframe):

    row_date = 'test'
    row_history = 'test'
    row_docto = 'test'
    row_credit = 'test'
    row_debt = 'test'
    row_balance = 'test'

    final_df = pd.DataFrame()
    final_df['Data'] = pd.NaT
    final_df['Histórico'] = pd.NaT
    final_df['Docto'] = pd.NaT
    final_df['Crédito'] = pd.NaT
    final_df['Débito'] = pd.NaT
    final_df['Saldo'] = pd.NaT

    fill_date = None

    row_count = 0

    for index, row in dataframe.iterrows():
      if index == 0:
        new_row = {
          'Data': row['Data'],
          'Histórico': row['Histórico'],
          'Docto': row['Docto.'],
          'Crédito': row['Docto.'],
          'Débito': row['Débito (R$)'],
          'Saldo': row['Saldo (R$)']
          }
        final_df = final_df.append(new_row, ignore_index = True)

        fill_date = row['Data']

      elif row_count < 2:
        row_date += f"{str(row['Data'])} "
        row_history += f"{str(row['Histórico'])}"
        row_docto += f"{str(row['Docto.'])} "
        row_credit += f"{str(row['Crédito (R$)'])} "
        row_debt += f"{str(row['Débito (R$)'])} "
        row_balance += f"{str(row['Saldo (R$)'])} "

        if not pd.isnull(row['Data']):
          fill_date = row['Data']
      
        row_count += 1
      
      elif row_count == 2:
        row_count = 0

        row_date += f"{str(row['Data'])} "
        row_history += f"{str(row['Histórico'])}"
        row_docto += f"{str(row['Docto.'])} "
        row_credit += f"{str(row['Crédito (R$)'])} "
        row_debt += f"{str(row['Débito (R$)'])} "
        row_balance += f"{str(row['Saldo (R$)'])} "

        new_row = {
          # 'Data': row_date.replace('nan', '').replace('test', ''),
          'Data': fill_date,
          'Histórico': row_history.replace('nan', '').replace('test', ''),
          'Docto': row_docto.replace('nan', '').replace('test', ''),
          'Crédito': row_credit.replace('nan', '').replace('test', ''),
          'Débito': row_debt.replace('nan', '').replace('test', ''),
          'Saldo': row_balance.replace('nan', '').replace('test', '')
          }
        final_df = final_df.append(new_row, ignore_index = True)

        row_date = f""
        row_history = f""
        row_docto = f""
        row_credit = f""
        row_debt = f""
        row_balance = f""
    
    return final_df

  
  def generateCSV(self) -> None:
    
    self.generateMergedPdf()

    area = [141, 15, 750, 612]

    tabula.convert_into(
      os.path.join(self.tempFolder, "tmp_pdf.pdf"),
      os.path.join(self.tempFolder, "tmp_csv.csv"),
      output_format="csv",
      pages='all',
      stream=True,
      area=area
    )

    os.system(f"rm -r {os.path.join(self.tempFolder, 'tmp_pdf.pdf')}")

    data_frame = pd.read_csv(os.path.join(self.tempFolder, "tmp_csv.csv"))

    os.system(f"rm -r {str(os.path.join(self.tempFolder, 'tmp_csv.csv'))}")

    column_name = data_frame.columns[0]

    for index, row in data_frame.iterrows():
      if row[column_name] == column_name:
        data_frame = data_frame.drop(index)

    df = self.handle_data(data_frame)

    # # df.to_csv(os.path.join(self.outPath, f"{self.output_filename}.csv"), encoding='utf-8')
    df.to_csv(os.path.join(self.outPath, f"output.csv"), encoding='utf-8')
    # # df.to_excel(os.path.join(self.outPath, f"{self.output_filename}.xlsx"), index = False)
    # df.to_excel(os.path.join(self.outPath, f"output.xlsx"), index = False)

    