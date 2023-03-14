import re

def translate_plataforma_from_google_ads(line):
  line = line.lower()
  if re.search('.*(search|Search).*', line) and re.search('.*(testeonline|TesteOnline|teste_online|Testeonline).*', line):
    return "Google Search (teste online)"
  elif re.search('.*(search|Search).*', line):
    return "Google Search"
  elif re.search('.*(pmax|Pmax|PMAX|PMax|performancemax|PerformanceMax|performance_max).*', line):
    return 'Google PMax'
  elif re.search('.*(display|Display).*', line):
    return 'Google Display'
  elif re.search('.*(discovery|Discovery).*', line):
    return 'Google Discovery'
  elif re.search('.*(tiktok|Tiktok|TIKTOK).*', line):
    return 'TikTok'
  elif re.search('.*(fbi|Fbi|FBI).*', line):
    return 'Meta Ads'
  elif re.search('.*(igoal|iGoal|IGoal).*', line):
    return 'iGoal'
  elif re.search('.*(dgmax|Dgmax|DGmax|DGMax).*', line):
    return 'DGMax'
  elif re.search('.*(google|Google|GOOGLE|adwords|Adwords|ADWORDS).*', line):
    return 'Google Search'
  elif re.search('.*(beeleads|Beeleads).*', line):
    return 'Beeleads'
  elif re.search('.*(not set).*', line):
    return 'Organico'
  else:
    return 'Outros'

def translate_campaign_type(campaign_name):
  if re.search('.*(testeonline|TesteOnline|teste_online|Testeonline).*', campaign_name):
    return "Teste Online"
  elif re.search('.*(wpp|WhatsApp|Whatsapp|WHATSAPP|whatsapp|whats_app).*', campaign_name):
    return "Whatsapp"
  elif re.search('.*(faculdade|Faculdade|FACULDADE).*', campaign_name):
    return "Faculdade"
  elif re.search('.*(fortnite|Fortnite|FORTNITE).*', campaign_name):
    return "Fortnite"
  else:
    return "Captação"

def translate_plataforma_to_meta_ads(line):
  if re.search('.*(whatsapp|Whatsapp|WHATSAPP|WhatsApp).*', line):
    return "Meta Ads (wpp)"
  else:
    return "Meta Ads"
