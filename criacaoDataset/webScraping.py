import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Lista de artistas por subgênero
generos_artistas = {
    "Sertanejo Raiz": ["tiao-carreiro-e-pardinho", "tonico-e-tinoco", "liu-e-leu", "belmonte-e-amarai", 
                       "barrerito", "lourenco-e-lourival", "joao-mineiro-e-marciano", "sergio-reis",
                       "inezita-barroso", "cascatinha-e-inhana", "goiano-e-paranaense", "leo-canhoto-e-robertinho", 
                        "almir-sater","zilo-e-zalo", "as-galvao", "zico-e-zeca", 
                        "pedro-bento-ze-da-estrada","vieira-vieirinha", "ze-fortuna-e-pitangueira", "rolando-boldrin",
                        "renato-teixeira", "pena-branca-e-xavantinho", "cacique-paje", "joaquim-e-manuel", "dino-franco-mourai"
                        #25 artistas com 20 músicas = 500 músicas
                        ],

            
    "Pagode": ["raca-negra", "soweto", "belo", "thiaguinho", "pericles",
               "pixote", "sorriso-maroto", "ferrugem", "pique-novo", "fundo-de-quintal",
               "turma-do-pagode", "revelacao", "diogo-nogueira", "art-popular", "so-pra-contrariar",
               "mumuzinho", "jeito-moleque", "katinguele", "molejo", "os-travessos",
               "luiz-carlos-da-vila", "grupo-malicia", "reinaldo", "negritude-junior", "sensacao",
                #25 artistas com 20 músicas = 500 músicas
               ],

    "Pop Rock Nacional": ["legiao-urbana", "skank", "paralamas-do-sucesso", "ira", "frejat", 
                          "rpm","capital-inicial", "jota-quest","engenheiros-do-hawaii", "kid-abelha", 
                          "lulu-santos", "titas", "rita-lee", "cassia-eller", "roupa-nova",
                          "barao-vermelho", "lobao", "biquini-cavadao", "ultrage-a-rigor", "leo-jaime",
                          "detonautas", "nenhum-de-nos", "los-hermanos", "herva-doce", "cazuza"
                        #25 artistas com 20 músicas = 500 músicas
                          ]

            #1500 músicas no dataset
}

# Buscar músicas de um artista
def coletar_urls_musicas(artista_slug, limite=5):
    url = f"https://www.letras.mus.br/{artista_slug}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.select('ol.js-song-list li a')  

    musicas = []
    for a in links[:limite]:
        nome = a.get('title', '').strip() or a.text.strip()
        href = a['href']
        url_completa = "https://www.letras.mus.br" + href
        musicas.append((nome, url_completa))

    return musicas

# Função para pegar a letra da música
def pegar_letra(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        letra_div = soup.find('div', class_='lyric-original')
        if letra_div:
            return letra_div.get_text(separator=' ').strip()
        else:
            return None
    except Exception as e: 
        print("ocorreu um erro: ", e) 
        return None 

# Coleta principal
dados = []

for genero, artistas in generos_artistas.items():
    for artista in artistas:
        print(f"\n🎤 Coletando de: {artista} | Gênero: {genero}")
        musicas = coletar_urls_musicas(artista, limite=20)
        print(f"🎵 Músicas encontradas para {artista}: {len(musicas)}")
        
        for nome_musica, url_musica in musicas:
            letra = pegar_letra(url_musica)
            if letra:
                dados.append({
                    "gênero": genero,
                    "artista": artista.replace("-", " ").title(),
                    "música": nome_musica,
                    "letra": letra
                })
                print(f"✅ {nome_musica}")
            else:
                print(f"❌ Falha em: {nome_musica}")
            time.sleep(1.5)

print(f"\n🎯 Total coletado: {len(dados)} músicas")
df = pd.DataFrame(dados)
df.to_csv("dataset_inicial.csv", index=False, encoding="utf-8")
print("✅ Dataset salvo com sucesso!")
