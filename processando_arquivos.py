from io import StringIO
import csv
def processando_arquivo(original_content, dados_portugues=False, debug=False):
 
  reader_raw = StringIO(original_content)
  reader = csv.reader(reader_raw)
  content = StringIO()
  for linha in reader:
        print("linha", list(linha))
        if len(linha) < 3 or ('Total of' in list(linha)[0]):
            # remove a linha incorreta
            print('removendo...')
            continue
        if(dados_portugues):
          linha = list(map(lambda val: val.replace(".",""), linha))
          linha = list(map(lambda val: val.replace(",","."), linha))
        content.write(",".join(linha) + "\n")

  # Reposiciona o ponteiro do buffer de string para o início
  content.seek(0)
  if(debug):
    print("content2 ")
    print(content.getvalue())
  return content

def reprocessando(file):
  with open(file, "r") as f:
    lines = f.readlines()
  filtered_lines = []
  for line in lines:
    if len(line.split(',')) >= 3:
      filtered_lines.append(line)
  
  csv_string = "".join(filtered_lines)
  csv_string_io = StringIO(csv_string)
  return csv_string_io

def dataframe_to_rows(df, index=True, header=True):
    """Iterate over a dataframe and yield rows as lists of values."""
    # Yield the header row
    if header:
        yield list(df.columns)

    # Yield the index values and data rows
    for row in df.itertuples(index=index, name='Pandas'):
        yield row