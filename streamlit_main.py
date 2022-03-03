import os
import streamlit as st
from extractors.barclays_extractor_streamlit import BarclaysExtractorStreamlit


from extractors.bb_extractor_streamlit import BBExtractorStreamlit
from extractors.bradesco_extractor_streamlit import BradescoExtractorStreamlit
from extractors.itau_extractor_streamlit import ItauExtractorStreamlit

st.title('extratos -> csv')
option = st.selectbox(
  'Selecione o Banco:',
  ('Banco do Brasil', 'Itau', 'Bradesco', 'Barcleys'))
extratos = st.file_uploader('Extratos', accept_multiple_files=True)

if extratos is not None and len(extratos) > 0:

  if option == 'Banco do Brasil':

    BBExtractorStreamlit(
      outpath=os.path.join(".", "output"),
      files=extratos
    ).generateCSV()

  elif option == 'Itau':
    ItauExtractorStreamlit(
      outpath=os.path.join(".", "output"),
      files=extratos
    ).generateCSV()
  
  elif option == 'Bradesco':
    BradescoExtractorStreamlit(
      outpath=os.path.join(".", "output"),
      files=extratos
    ).generateCSV()
  
  elif option == 'Barcleys':
    BarclaysExtractorStreamlit(
      outpath=os.path.join(".", "output"),
      files=extratos
    ).generateCSV()
  
  with open(os.path.join(".", "output", "output.csv")) as result:

    st.download_button(
      label="Download data as XLSX",
      data=result,
      file_name=f"output.xlsx",
      mime='text/csv',
      key='button'
      
    )

