import io
import tempfile
from unittest.mock import DEFAULT
import tabula
import PyPDF2
# from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import pandas as pd
import os
from pandas import isnull

class BBExtractorStreamlit():
  
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
    row_value = 'test'

    final_df = pd.DataFrame()
    final_df['Dia'] = pd.NaT
    final_df['Histórico'] = pd.NaT
    final_df['Valor'] = pd.NaT

    for index, row in dataframe.iterrows():
      if not isnull(row['Dia']):
        new_row = {'Dia': row_date, 'Histórico': row_history, 'Valor': row_value.replace('nan', ' ')}
        final_df = final_df.append(new_row, ignore_index = True)

        row_date = row['Dia']
        row_history = str(row['Histórico'])
        row_value = str(row['Valor'])
      
      if not isnull(row['Histórico']):
        row_history += f"{str(row['Histórico'])} "
      
      if not isnull(row['Valor']):
        row_value += f"{str(row['Valor'])} "
    
    return final_df

  
  def generateCSV(self) -> None:
    
    self.generateMergedPdf()

    # df = tabula.read_pdf(
    #   os.path.join(self.tempFolder, "tmp_pdf.pdf"),guess=False, lattice=False, stream=True, pages="all"
    # )

    area = [100, 15, 750, 612]

    tabula.convert_into(
      os.path.join(self.tempFolder, "tmp_pdf.pdf"),
      os.path.join(self.tempFolder, "tmp_csv.csv"),
      output_format="csv",
      area=area, pages="all"
    )

    os.system(f"rm -r {os.path.join(self.tempFolder, 'tmp_pdf.pdf')}")

    data_frame = pd.read_csv(os.path.join(self.tempFolder, "tmp_csv.csv"), on_bad_lines='skip')

    os.system(f"rm -r {str(os.path.join(self.tempFolder, 'tmp_csv.csv'))}")

    column_name = data_frame.columns[0]

    for index, row in data_frame.iterrows():
      if row[column_name] == column_name:
        data_frame = data_frame.drop(index)

    df = self.handle_data(data_frame)
    print(df)

    # df.to_csv(os.path.join(self.outPath, f"{self.output_filename}.csv"), encoding='utf-8')
    df.to_csv(os.path.join(self.outPath, f"output.csv"), encoding='utf-8')
    # df.to_excel(os.path.join(self.outPath, f"{self.output_filename}.xlsx"), index = False)
    df.to_excel(os.path.join(self.outPath, f"output.xlsx"), index = False)

    