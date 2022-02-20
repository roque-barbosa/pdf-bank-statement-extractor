from unittest.mock import DEFAULT
import PyPDF2
import tabula
import pandas as pd
import os

class ItauExtractorStreamlit():
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

  
  def generateCSV(self) -> None:
    self.generateMergedPdf()
    
    
    # print(tabula.read_pdf(
    #   os.path.join(self.tempFolder, "tmp_pdf.pdf"),
    #   pages='all', stream=True
    # ))

    tabula.convert_into(
      os.path.join(self.tempFolder, "tmp_pdf.pdf"),
      os.path.join(self.tempFolder, "tmp_csv.csv"),
      output_format="csv",
      pages='all',
      stream=True
    )

    # area = [90, 15, 750, 612]

    # tabula.convert_into(
    #   os.path.join(self.tempFolder, "tmp_pdf.pdf"),
    #   os.path.join(self.tempFolder, "tmp_csv.csv"),
    #   output_format="csv",
    #   area=area, pages="all"
    # )

    os.system(f"rm -r {os.path.join(self.tempFolder, 'tmp_pdf.pdf')}")

    data_frame = pd.read_csv(os.path.join(self.tempFolder, "tmp_csv.csv"))

    os.system(f"rm -r {str(os.path.join(self.tempFolder, 'tmp_csv.csv'))}")

    column_name = data_frame.columns[0]

    for index, row in data_frame.iterrows():
      if row[column_name] == column_name:
        data_frame = data_frame.drop(index)
    data_frame.to_csv(os.path.join(self.outPath, f"output.csv"), encoding='utf-8')
    data_frame.to_excel(os.path.join(self.outPath, f"output.xlsx"), index = False)

    