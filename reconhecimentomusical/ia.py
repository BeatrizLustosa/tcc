import re
import requests
from bs4 import BeautifulSoup
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from unidecode import unidecode
import nltk
import pandas as pd

# Baixa stopwords do NLTK (se não baixou ainda)
nltk.download('stopwords')
stopwords_pt = set(nltk.corpus.stopwords.words('portuguese'))

def get_lyrics(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # No site letras.mus.br a letra está dentro da div com class "cnt-letra"
        div_letra = soup.find("div", class_="cnt-letra")
        if div_letra:
            # Pega o texto da letra (remove tags, mantém o texto)
            letra = div_letra.get_text(separator="\n").strip()
            return letra
        else:
            print(f"Letra não encontrada em {url}")
            return None
    except Exception as e:
        print(f"Erro ao buscar letra em {url}: {e}")
        return None

musicas = [
    {
        "url": "https://www.vagalume.com.br/tiao-carreiro-e-pardinho/porta-do-mundo.html",
        "genero": "Sertanejo Raiz"
    },
    
]

dados = []
for m in musicas:
    print(f"Coletando: {m['url']}")
    letra = get_lyrics(m["url"])
    if letra:
        print(f"Tamanho da letra: {len(letra)} caracteres")
        dados.append({"letra": letra, "genero": m["genero"]})
    else:
        print("Letra não coletada.")

df = pd.DataFrame(dados)
print(df.head())
