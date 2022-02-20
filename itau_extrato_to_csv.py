import tabula
import pandas as pd

# Read pdf into list of DataFrame
tabula.read_pdf("extrato.pdf", pages='all', stream=True)
# convert PDF into CSV file
tabula.convert_into("extrato.pdf", "output.csv", output_format="csv", pages='all')

data_frame = pd.read_csv('output.csv')

column_name = data_frame.columns[0]
colum_rows = data_frame[column_name]

for index, row in data_frame.iterrows():
  if row[column_name] == column_name:
    data_frame = data_frame.drop(index)

data_frame.to_csv('test.csv', encoding='utf-8')
