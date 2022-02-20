import os
import aspose.words as aw
import tempfile

with tempfile.NamedTemporaryFile() as f:
  f = aw.Document("extrato.pdf")
  f.save(f)
  # print(f)
os.system('rm -r htmloutput/*.png')