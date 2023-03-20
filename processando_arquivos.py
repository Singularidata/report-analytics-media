from io import StringIO
import csv
import re

def processando_arquivo(original_content, dados_portugues=False, debug=False):
  reader_raw = StringIO(original_content)
  reader = csv.reader(reader_raw)
  content = StringIO()
  for linha in reader:
        print("linha", list(linha))
        if len(linha) < 3 or ('Total of' in list(linha)[0]):
            # remove a linha incorreta
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

def processando_arquivo_e_tipo(original_content, debug=False):
  reader_raw = StringIO(original_content)
  reader = csv.reader(reader_raw)
  dados_portugues=False
  verificado=False
  tipo = ''
  content = StringIO()
  for linha in reader:
      if len(linha) < 3 or ('Total of' in list(linha)[0]):
          # remove a linha incorreta
          continue
      linha_string = str(linha).lower()

      #validando tipo:
      if(len(tipo) < 1):
        if (re.search('sessões', linha_string)):
          tipo = 'analytics'
        elif (re.search('tipo de campanha', linha_string)):
          tipo = 'gads'
        elif (re.search('lifecycle stage', linha_string)):
          tipo = 'hubspot'
        elif (re.search('(status de veiculação|delivery status)', linha_string)):
          tipo = 'meta_ads'
        elif (re.search('url \(ad level\)', linha_string)):
          tipo = 'tiktok_ads'

      #verifica dados portugues ou ingles
      if ( not(dados_portugues) and not(verificado) and re.search('.*([0-9]+\,[0-9]+%)', linha_string) ):
        dados_portugues = True
        verificado=True
      elif ('Record ID' in list(linha)[0]):
         verificado= True
      if(dados_portugues):
        linha = list(map(lambda val: val.replace(".",""), linha))
        linha = list(map(lambda val: val.replace(",","."), linha))
      content.write(",".join(linha) + "\n")
  # Reposiciona o ponteiro do buffer de string para o início
  content.seek(0)
  if(debug):
    print("content2 ")
    print(content.getvalue())
  #encontrando o tipo
  dict_file = {"arquivo": content, "tipo": tipo}
  return dict_file

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