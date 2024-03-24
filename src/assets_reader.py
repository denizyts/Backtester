
class assets_reader:

#ASSETS.TXT 2023  , 
 #ASSETS2.TXT before 2021.

 def reader():
  with open('assets2.txt', 'r') as file:
     content = file.read()

  lines = content.split('\n')

  assets = []
  for line in lines:
      assets.append(line)

  return assets
 
