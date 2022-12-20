import re

def translate_plataforma_from_google_ads(line):
  if re.search('.*(search|Search).*', line):
    return "Google Search"
  elif re.search('.*(pmax|Pmax|PMAX|PMax).*', line):
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

def translate_plataforma_to_meta_ads(line):
  if re.search('.*(whatsapp|Whatsapp|WHATSAPP|WhatsApp).*', line):
    return "Meta Ads (wpp)"
  else:
    return "Meta Ads"