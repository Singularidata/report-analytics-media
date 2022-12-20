from datetime import datetime
import streamlit as st
import base64
import openpyxl

import pandas as pd
from processando_arquivos import processando_arquivo, dataframe_to_rows
from translators import translate_plataforma_from_google_ads, translate_plataforma_to_meta_ads

st.title("ACOMP Report! Cultura Inglesa (CISP/CIISA)")

st.header("Google Analytics")
analytics_file = st.file_uploader(
    "Selecione o arquivo CSV do Google Analytics", type="csv")
st.header("Google Ads")
gads_file = st.file_uploader(
    "Selecione o arquivo CSV do Google Ads", type="csv")
st.header("Hubspot")
hubspot_file = st.file_uploader(
    "Selecione o arquivo CSV do Hubpost", type="csv")
st.header("Meta Ads")
meta_ads_file = st.file_uploader(
    "Selecione o arquivo CSV do Meta Ads", type="csv")
st.header("TikTok Ads")
tiktok_ads_file = st.file_uploader(
    "Selecione o arquivo CSV do TikTok Ads", type="csv")

parsing_date = lambda date_string: pd.to_datetime(date_string).strftime("%Y%m%d")
if (analytics_file is not None and gads_file is not None and hubspot_file is not None and meta_ads_file is not None and tiktok_ads_file is not None):
  analytics_content = analytics_file.read().decode("utf-8")
  gads_content = gads_file.read().decode("utf-8")
  hubspot_content = hubspot_file.read().decode("utf-8")
  meta_ads_content = meta_ads_file.read().decode("utf-8")
  tiktok_ads_content = tiktok_ads_file.read().decode("utf-8")

  analytics_content_corrected = processando_arquivo(analytics_content, dados_portugues=True)
  gads_content_corrected = processando_arquivo(gads_content, dados_portugues=True)
  hubspot_content_corrected = processando_arquivo(hubspot_content)
  meta_ads_content_corrected = processando_arquivo(meta_ads_content)
  tiktok_ads_content_corrected = processando_arquivo(tiktok_ads_content)

  analytics = pd.read_csv(analytics_content_corrected,  error_bad_lines=False, parse_dates=['Data'])
  gads = pd.read_csv(gads_content_corrected,  error_bad_lines=False, parse_dates=['Dia'])
  hubspot = pd.read_csv(hubspot_content_corrected,  error_bad_lines=False, parse_dates=['Create Date'])
  meta_ads = pd.read_csv(meta_ads_content_corrected,  error_bad_lines=False, parse_dates=['Dia'])
  tiktok_ads = pd.read_csv(tiktok_ads_content_corrected,  error_bad_lines=False, parse_dates=['Date'])
  
  st.button("Processar novamente!")


  hubspot_por_dia = hubspot.groupby([hubspot['Create Date'].dt.date, 'Original Source Drill-Down 1', 'Lifecycle Stage']).agg({'Email': 'count'}).reset_index()
  hubspot_por_dia = hubspot_por_dia.rename(columns={'Create Date': 'Dia', 'Original Source Drill-Down 1': 'Campanha', 'Lifecycle Stage': 'Tipo', 'Email': 'Leads'})
  hubspot_por_dia['Plataforma'] = hubspot_por_dia['Campanha'].apply(translate_plataforma_from_google_ads)
  hubspot_por_dia["Source"] = "Hubspot"

  #analytics
  analytics['Data'] = analytics['Data'].dt.date
  analytics['Plataforma'] = analytics['Campanha'].apply(translate_plataforma_from_google_ads)
  analytics = analytics.rename(columns={'Data': 'Dia', 'ABlab - Submissão de formulário (Conclusões da meta 10)': 'Leads', 'ABlab - Submissão de formulário (Taxa de conversão da meta 10)': 'Taxa de conv.'})
  analytics_por_dia = analytics[['Dia', 'Plataforma', 'Campanha', 'Usuários', 'Sessões', 'Leads', 'Taxa de conv.']]
  analytics_por_dia["Source"] = "Google Analytics"

  #Gads
  gads['Dia'] = gads['Dia'].dt.date
  gads['Plataforma'] = gads['Campanha'].apply(translate_plataforma_from_google_ads)
  gads = gads.rename(columns={'Custo': 'Investimento', 'Impr.': 'Impressões', 'Impr': 'Impressões', 'Conversões': 'Leads', 'Custo / conv.': 'CPL', 'Custo / conv': 'CPL'})
  gads_por_dia = gads[['Dia', 'Plataforma', 'Investimento','Leads', 'CPL', 'Impressões', 'Cliques', 'CTR', 'CPC médio', 'Taxa de conv']]
  gads_por_dia = gads_por_dia.astype({'Cliques': 'int', 'Leads': 'int', 'Impressões': 'int', 'Impressões': 'int','Investimento': 'int'})
  gads_por_dia["Source"] = "Google Ads"

  meta_ads = meta_ads.rename(columns={
  'Leads Qualificados CIRJ': 'Cadastros no site',
  'Valor gasto (BRL)': 'Investimento', 
  'Custo por cadastro': 'CPL', 
  'CTR (taxa de cliques no link)': 'CTR', 
  'CPC (custo por clique no link)': 'CPC médio', 
  'Cliques no link': 'Cliques', 
  'Nome da campanha': 'Campanha', 
  'Conversas por mensagem iniciadas': 'Leads (wpp)'
    })
  meta_ads['Plataforma'] = meta_ads["Campanha"].apply(translate_plataforma_to_meta_ads)
  meta_ads = meta_ads.fillna(0)
  if not "Leads (wpp)" in meta_ads.columns:
     meta_ads['Leads (wpp)'] = 0
  if not "Cadastros na Meta" in meta_ads.columns:
     meta_ads['Cadastros na Meta'] = 0
  meta_ads['Leads'] = meta_ads['Cadastros no site'] + meta_ads['Leads (wpp)'] + meta_ads['Cadastros na Meta']
  meta_ads['CPL'] = meta_ads['Investimento'].div(meta_ads['Leads']).round(2)
  meta_ads_por_dia = meta_ads.groupby([meta_ads['Dia'].dt.date, 'Plataforma', 'Campanha']).agg({'Investimento': 'sum', 'Leads': 'sum', 'CPL': 'mean', 'Impressões': 'sum', 'Cliques': 'sum', 'CTR': 'mean', 'CPC médio': 'mean', 'Leads (wpp)': 'sum'}).reset_index()
  meta_ads_por_dia = meta_ads_por_dia.fillna(0)
  meta_ads_por_dia = meta_ads_por_dia.astype({'Cliques': 'int', 'Leads': 'int', 'Impressões': 'int'})
  meta_ads_por_dia['Taxa de conv.'] = meta_ads_por_dia['Leads'].div(meta_ads_por_dia['Cliques']).round(4)*100
  meta_ads_por_dia['CPL'] = meta_ads_por_dia['Investimento'].div(meta_ads_por_dia['Leads']).round(2)
  meta_ads_por_dia['CTR'] = meta_ads_por_dia[meta_ads_por_dia['Plataforma'] == 'Meta Ads']['Cliques'].div(meta_ads_por_dia[meta_ads_por_dia['Plataforma'] == 'Meta Ads']['Impressões']).round(4)*100
  meta_ads_por_dia = meta_ads_por_dia.fillna(0)
  meta_ads_por_dia['Taxa de conv.'] = meta_ads_por_dia['Taxa de conv.'].round(2).map(str) +'%'
  meta_ads_por_dia['CTR'] = meta_ads_por_dia['CTR'].round(2).map(str) +'%'
  meta_ads_por_dia["Source"] = "Meta Ads"

  #tiktok ads
  tiktok_ads['Plataforma'] = "TikTok"
  tiktok_ads = tiktok_ads.rename(columns={'Date': 'Dia', 'Campaign name': 'Campanha', 'Cost': 'Investimento', 'Total Submit Form': 'Leads', 'Impression': 'Impressões', 'Click': 'Cliques', 'CPC': 'CPC médio'})
  tiktok_ads = tiktok_ads.fillna(0)
  tiktok_ads['CPL'] = tiktok_ads['Investimento'].div(tiktok_ads['Leads']).round(2)
  tiktok_ads_por_dia = tiktok_ads.groupby([tiktok_ads['Dia'].dt.date, 'Plataforma', 'Campanha']).agg({'Investimento': 'sum', 'Leads': 'sum', 'CPL': 'mean', 'Impressões': 'sum', 'Cliques': 'sum', 'CTR': 'mean', 'CPC médio': 'mean'}).reset_index()
  tiktok_ads_por_dia['Taxa de conv.'] = tiktok_ads_por_dia['Leads'].div(tiktok_ads_por_dia['Cliques']).round(4)*100
  tiktok_ads_por_dia = tiktok_ads_por_dia.fillna(0)
  tiktok_ads_por_dia['Taxa de conv.'] = tiktok_ads_por_dia['Taxa de conv.'].round(2).map(str) +'%'
  tiktok_ads_por_dia["Source"] = "TikTok Ads"

  st.header('Analytics')
  st.dataframe(analytics_por_dia)

  st.header('GAds')
  st.dataframe(gads_por_dia)

  st.header('Hubspot')
  st.dataframe(hubspot_por_dia)

  st.header('Meta Ads')
  st.dataframe(meta_ads_por_dia)

  st.header('TikTok Ads')
  st.dataframe(tiktok_ads_por_dia)

  acumulado = pd.concat([analytics_por_dia, gads_por_dia, hubspot_por_dia, meta_ads_por_dia, tiktok_ads_por_dia], ignore_index=True)
  acumulado = acumulado.fillna(0)
  st.header('Acumulado')
  st.dataframe(acumulado)


  workbook =  openpyxl.load_workbook('./src/acomp_data_report.xlsx')
  original_dash = workbook['dashboard']
  original_data = workbook['data']
  original_dia = workbook['dia-a-dia']

  workbook.remove(workbook.get_sheet_by_name('acumulado'))
  acumulado_worksheet = workbook.create_sheet('acumulado')
  for r in dataframe_to_rows(acumulado, index=False, header=True):
    acumulado_worksheet.append(r)
  
  workbook.remove(workbook.get_sheet_by_name('hubspot'))
  hubspot_worksheet = workbook.create_sheet('hubspot')
  for r in dataframe_to_rows(hubspot_por_dia, index=False, header=True):
    hubspot_worksheet.append(r)

  workbook.remove(workbook.get_sheet_by_name('ga'))
  ga_worksheet = workbook.create_sheet('ga')
  for r in dataframe_to_rows(analytics_por_dia, index=False, header=True):
    ga_worksheet.append(r)
  
  workbook.remove(workbook.get_sheet_by_name('gads'))
  gads_worksheet = workbook.create_sheet('gads')
  for r in dataframe_to_rows(gads_por_dia, index=False, header=True):
    gads_worksheet.append(r)
  
  workbook.remove(workbook.get_sheet_by_name('meta ads'))
  meta_ads_worksheet = workbook.create_sheet('meta ads')
  for r in dataframe_to_rows(meta_ads_por_dia, index=False, header=True):
    meta_ads_worksheet.append(r)

  workbook.remove(workbook.get_sheet_by_name('tiktok ads'))
  tiktok_ads_worksheet = workbook.create_sheet('tiktok ads')
  for r in dataframe_to_rows(tiktok_ads_por_dia, index=False, header=True):
    tiktok_ads_worksheet.append(r)
  
  workbook.save('./acomp_data_report.xlsx')

  with open('./acomp_data_report.xlsx', 'rb') as f:
    excel_b64 = base64.b64encode(f.read())

  st.markdown(
      "Clique no botão abaixo para fazer o download do arquivo Excel com as sugestões")
  st.markdown(
      f'<a href="data:application/octet-stream;base64,{excel_b64.decode()}" download="acomp_data_report.xlsx">Baixar</a>', unsafe_allow_html=True)
