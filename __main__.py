# import sys
# from extractors.itau_extractor import ItauExtractor
# import os

# def main (bank: str, paths: list):
#   print(bank)
#   for i in paths:
#     print(i)


# if __name__ == '__main__':

#   pdfs_paths = [*sys.argv[3:]]
#   outputPath = [sys.argv[2]]
#   bank_name = sys.argv[1]

#   if bank_name == 'itau':
#     ItauExtractor(outputPath, [*sys.argv[2:]]).generateCSV()
#     # ItauExtractor(os.path.join(".","output"), [*sys.argv[2:]]).generateCSV()


import click
from cli_commands import extract

@click.group()
def cli():
    pass

cli.add_command(extract)

if __name__ == "__main__":
  cli()