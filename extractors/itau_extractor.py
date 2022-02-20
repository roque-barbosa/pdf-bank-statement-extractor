from unittest.mock import DEFAULT
import tabula
from PyPDF2 import PdfFileMerger
import pandas as pd
import os

class ItauExtractor():
  def __init__(self, outpath: str , paths: list[str], output_filename: str = "output") -> None:
      self.paths = paths
      self.outPath = outpath
      self.tempFolder = os.path.join(".", "temp")
      self.output_filename = output_filename
    
  def generateMergedPdf(self):
    merger = PdfFileMerger()
    if len(self.paths) > 0:
      self.output_filename = os.path.basename(self.paths[0]).split('.')[0]
    for pdf in self.paths:
      merger.append(pdf)
      merger.write(os.path.join(self.tempFolder, "tmp_pdf.pdf"))

  
  def generateCSV(self) -> None:
    self.generateMergedPdf()
    
    tabula.read_pdf(
      os.path.join(self.tempFolder, "tmp_pdf.pdf"),
      pages='all', stream=True
    )

    tabula.convert_into(
      os.path.join(self.tempFolder, "tmp_pdf.pdf"),
      os.path.join(self.tempFolder, "tmp_csv.csv"),
      output_format="csv",
      pages='all'
    )

    os.system(f"rm -r {os.path.join(self.tempFolder, 'tmp_pdf.pdf')}")

    data_frame = pd.read_csv(os.path.join(self.tempFolder, "tmp_csv.csv"))

    os.system(f"rm -r {str(os.path.join(self.tempFolder, 'tmp_csv.csv'))}")

    column_name = data_frame.columns[0]

    for index, row in data_frame.iterrows():
      if row[column_name] == column_name:
        data_frame = data_frame.drop(index)
    data_frame.to_csv(os.path.join(self.outPath, f"{self.output_filename}.csv"), encoding='utf-8')
    data_frame.to_excel(os.path.join(self.outPath, f"{self.output_filename}.xlsx"), index = False)

    