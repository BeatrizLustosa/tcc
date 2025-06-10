import re
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from unidecode import unidecode
import nltk
import pandas as pd

# Baixa stopwords do NLTK
nltk.download('stopwords')

dados = [
    # Sertanejo Raiz (exemplos)
    {"letra": "Sou caipira, Pirapora, nossa senhora de Aparecida",
        "genero": "Sertanejo Raiz"},
    {"letra": "No sertão a vida é difícil, mas Deus me guia e me abençoa",
        "genero": "Sertanejo Raiz"},
    {"letra": "Minha viola chora na beira da fogueira", "genero": "Sertanejo Raiz"},
    {"letra": "Churrasco, prosa boa e a família reunida", "genero": "Sertanejo Raiz"},
    {"letra": "Estrada de chão, botina e chapéu, esse é o meu caminho",
        "genero": "Sertanejo Raiz"},
    {"letra": "Coração na estrada, saudade do meu lar", "genero": "Sertanejo Raiz"},
    {"letra": "Tocando moda raiz até o amanhecer", "genero": "Sertanejo Raiz"},
    {"letra": "Noite estrelada, violeiro a cantar", "genero": "Sertanejo Raiz"},
    {"letra": "No rancho velho, o amor nunca se acaba", "genero": "Sertanejo Raiz"},
    {"letra": "Sou homem do campo, da lida e do trabalho", "genero": "Sertanejo Raiz"},

    # Pagode (exemplos)
    {"letra": "Deixa a vida me levar, vida leva eu", "genero": "Pagode"},
    {"letra": "É tanto amor, minha nega, que não cabe no peito", "genero": "Pagode"},
    {"letra": "Samba no pé e sorriso no rosto, alegria no coração", "genero": "Pagode"},
    {"letra": "No pagode da vila a tristeza não tem vez", "genero": "Pagode"},
    {"letra": "Chama a galera, vamos brindar a amizade e o amor", "genero": "Pagode"},
    {"letra": "Vem comigo sambar até o sol raiar", "genero": "Pagode"},
    {"letra": "No balanço do tambor, a gente vai se encontrar", "genero": "Pagode"},
    {"letra": "Cerveja gelada, roda de samba animada", "genero": "Pagode"},
    {"letra": "Amor verdadeiro, no ritmo do coração", "genero": "Pagode"},
    {"letra": "Juntos na alegria, festejando a paixão", "genero": "Pagode"},

    # Pop Rock Nacional (exemplos)
    {"letra": "Você diz que seus pais não entendem, mas você não entende seus pais",
        "genero": "Pop Rock Nacional"},
    {"letra": "Eu quero ser o sol que ilumina o seu caminho",
        "genero": "Pop Rock Nacional"},
    {"letra": "O tempo não para, mas a gente pode tentar",
        "genero": "Pop Rock Nacional"},
    {"letra": "Coração aberto, vivendo a vida sem medo",
        "genero": "Pop Rock Nacional"},
    {"letra": "Vamos gritar até a cidade ouvir nossa canção",
        "genero": "Pop Rock Nacional"},
    {"letra": "No palco a energia que contagia multidão",
        "genero": "Pop Rock Nacional"},
    {"letra": "Entre guitarras e baterias, nasce uma revolução",
        "genero": "Pop Rock Nacional"},
    {"letra": "Liberdade é a voz que ecoa na canção", "genero": "Pop Rock Nacional"},
    {"letra": "A juventude vive intensamente seu ideal",
        "genero": "Pop Rock Nacional"},
    {"letra": "Em cada acorde, uma história para contar",
        "genero": "Pop Rock Nacional"},
]
df = pd.DataFrame(dados)

stopwords_pt = set(nltk.corpus.stopwords.words('portuguese'))


def preprocessar_texto(texto):
    texto = texto.lower()
    texto = unidecode(texto)
    # Remove tudo que não seja letra ou espaço
    texto = re.sub(r'[^a-z\s]', '', texto)
    # Remove stopwords
    tokens = [palavra for palavra in texto.split()
              if palavra not in stopwords_pt]
    return " ".join(tokens)


df['letra_tratada'] = df['letra'].apply(preprocessar_texto)

vetorizador = TfidfVectorizer(min_df=1, max_df=0.8)
X = vetorizador.fit_transform(df['letra_tratada'])
y = df['genero']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("Random Forest:")
print(classification_report(y_test, y_pred_rf))

svm = SVC(random_state=42)
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)

print("SVM:")
print(classification_report(y_test, y_pred_svm))

print("Matriz de Confusão - Random Forest:")
print(confusion_matrix(y_test, y_pred_rf))

print("Matriz de Confusão - SVM:")
print(confusion_matrix(y_test, y_pred_svm))

print("Acurácia RF:", accuracy_score(y_test, y_pred_rf))
print("Acurácia SVM:", accuracy_score(y_test, y_pred_svm))
