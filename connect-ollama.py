import os
import json
from ollama import Client

OLLAMA_HOST_FILE = "secret/server_info.json"

def create_ollama():

    OLLAMA_IP = os.environ.get("OLLAMA_IP")
    OLLAMA_PORT = os.environ.get("OLLAMA_PORT")

    # Check if credentials file exists
    if os.path.exists(OLLAMA_HOST_FILE):
        with open(OLLAMA_HOST_FILE, 'r') as file:
            creds = json.load(file)
            # print(f"Connecting to {creds['ip']}:{creds['port']}")
            return Client(host=f"{creds['ip']}:{creds['port']}")

    if OLLAMA_IP is None or OLLAMA_PORT is None:
        print(f"Could not find ollama server details in {OLLAMA_HOST_FILE} nor OLLAMA_IP and OLLAMA_PORT env variable.")

    return EOFError



client = create_ollama()
if os.path.exists("data/Archéologie short.txt"):
      with open("data/Archéologie short.txt", 'r') as file:
          defi = file.read().replace("\n", " ")

#print(f"ok{defi}")
# print (defi)
#consigne = input("Consigne>")
consigne = ""
answer = ""
# for i in ["premier", "second", "troisème", "quatrième", "cinquième", "sixième"]:
#     requete = f"Dans le texte suivant, répète sans le modifier le {i} paragraphe : " + defi
#     response = client.chat(model='llama3.2', messages=[
#     {
#         'role': 'user',
#         'content': requete,
#     },
#     ])

#     answer = answer + response['message']['content']
client.pull('llama3.1') 
requete = f"Tu es relecteur professionnel.\nVoici une définition obtenue par OCR sur un dictionnaire spécialisé.\nTu corrigeras les fautes dans les mots, et corrigera ou retirera ceux qui n'ont pas de sens sans retirer les retours à la ligne qui les précèdent. En effet, au début d'un paragraphe (mais aussi en fin de mot ou ailleurs), il arrive que des caractères aient été ajoutés par erreur. Retire ceux-là sans perdre la séparation entre paragraphes.\n Assure toi que le texte produit soit fidèle au texte originellement intentionné avant l'OCR, tout en étant cohérent car tu lui aurais retiré les erreurs.\n Ne réponds rien d'autre que le texte corrigé :\n" + defi
response = client.chat(model='llama3.2', messages=[
 {
     'role': 'user',
     'content': requete,
 },
 ])
answer = response['message']['content']


print(requete)
print(answer)
with open("output/Foucault/Archéologie.txt", 'w') as file:
          file.write(answer)

requete = f"Tu es relecteur professionnel.\nVoici une définition obtenue par OCR sur un dictionnaire spécialisé.\n Tu encadreras chaque NOM D'AUTEUR via les balises <persName>NOM D'AUTEUR</persName>.\n Tu encadreras chaque DATE via les balises <date>DATE</date>.\n  Tu encadreras chaque REFERENCE BIBLIOGRAPHIQUE via les balises <bibl>REFERENCE BIBLIOGRAPHIQUE</bibl>.\nNe réponds rien d'autre que le texte corrigé :\n" + defi
response = client.chat(model='llama3.2', messages=[
 {
     'role': 'user',
     'content': requete,
 },
 ])
answer = response['message']['content']

print("--------------------------")
print(answer)
