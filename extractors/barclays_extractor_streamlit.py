import io
import tempfile
from unittest.mock import DEFAULT
import tabula
import PyPDF2
# from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import pandas as pd
import os
from pandas import isnull

class BarclaysExtractorStreamlit():
  
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
    row_description = 'test'
    row_money_in = 'test'
    row_money_out = 'test'
    row_balance = 'test'

    final_df = pd.DataFrame()
    final_df['Date'] = pd.NaT
    final_df['Description'] = pd.NaT
    final_df['Money in'] = pd.NaT
    final_df['Money out'] = pd.NaT
    final_df['Balance'] = pd.NaT

    fill_date = None

    row_count = 0

    for index, row in dataframe.iterrows():
      if row['Description'] == 'End balance':
        break
      
      if index == 0:
        new_row = {
          'Date': row['Date'],
          'Description': row['Description'],
          'Money in': row['Money in'],
          'Money out': row['Money out'],
          'Balance': row['Balance']
          }
        final_df = final_df.append(new_row, ignore_index = True)

        fill_date = row['Date']
      
      elif row_count < 1:
        row_date += f"{str(row['Date'])} "
        row_description += f"{str(row['Description'])}"
        row_money_in += f"{str(row['Money in'])} "
        row_money_out += f"{str(row['Money out'])} "
        row_balance += f"{str(row['Balance'])} "

        if not pd.isnull(row['Date']):
          fill_date = row['Date']
      
        row_count += 1
      
        
      elif row_count == 1:
        row_count = 0

        row_date += f"{str(row['Date'])} "
        row_description += f"{str(row['Description'])}"
        row_money_in += f"{str(row['Money in'])} "
        row_money_out += f"{str(row['Money out'])} "
        row_balance += f"{str(row['Balance'])} "

        new_row = {
          # 'Data': row_date.replace('nan', '').replace('test', ''),
          'Date': fill_date,
          'Description': row_description.replace('nan', '').replace('test', ''),
          'Money in': row_money_in.replace('nan', '').replace('test', ''),
          'Money out': row_money_out.replace('nan', '').replace('test', ''),
          'Balance': row_balance.replace('nan', '').replace('test', '')
          }
        final_df = final_df.append(new_row, ignore_index = True)

        row_date = f""
        row_description = f""
        row_money_in = f""
        row_money_out = f""
        row_balance = f""
    
    return final_df

  
  def generateCSV(self) -> None:
    
    self.generateMergedPdf()

    # df = tabula.read_pdf(
    #   os.path.join(self.tempFolder, "tmp_pdf.pdf"),guess=False, lattice=False, stream=True, pages="all"
    # )

    area = [377, 56, 750, 420]

    tabula.convert_into(
      os.path.join(self.tempFolder, "tmp_pdf.pdf"),
      os.path.join(self.tempFolder, "tmp_csv.csv"),
      output_format="csv",
      area=area, pages="all"
    )

    os.system(f"rm -r {os.path.join(self.tempFolder, 'tmp_pdf.pdf')}")

    data_frame = pd.read_csv(os.path.join(self.tempFolder, "tmp_csv.csv"), on_bad_lines='skip')

    # os.system(f"rm -r {str(os.path.join(self.tempFolder, 'tmp_csv.csv'))}")

    column_name = data_frame.columns[0]

    for index, row in data_frame.iterrows():
      if row[column_name] == column_name:
        data_frame = data_frame.drop(index)

    df = self.handle_data(data_frame)
    # print(df)

    # # df.to_csv(os.path.join(self.outPath, f"{self.output_filename}.csv"), encoding='utf-8')
    df.to_csv(os.path.join(self.outPath, f"output.csv"), encoding='utf-8')
    # # df.to_excel(os.path.join(self.outPath, f"{self.output_filename}.xlsx"), index = False)
    # df.to_excel(os.path.join(self.outPath, f"output.xlsx"), index = False)

    