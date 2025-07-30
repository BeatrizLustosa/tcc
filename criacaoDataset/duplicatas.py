import pandas as pd

class DuplicatasMusicais:
    def __init__(self, caminho_csv):
        self.caminho_csv = caminho_csv
        self.df = pd.read_csv(caminho_csv)

    def remover_duplicatas_por_letra(self):
        """
        Remove músicas com letras idênticas e retorna o novo DataFrame.
        """
        print("🔍 Removendo músicas com letras duplicadas...\n")
        antes = self.df.shape[0]

        # Remove duplicatas com base apenas na coluna 'letra'
        df_sem_duplicatas = self.df.drop_duplicates(subset=['letra'])

        depois = df_sem_duplicatas.shape[0]
        removidas = antes - depois

        print(f"➡️ {removidas} duplicatas removidas.")
        print(f"🎶 {depois} músicas únicas restantes.\n")

        return df_sem_duplicatas

    def salvar_dataset_limpo(self, caminho_saida='musicas_sem_duplicatas.csv'):
        df_limpo = self.remover_duplicatas_por_letra()

        # Contar quantas músicas por subgênero
        print("📊 Músicas por subgênero após remoção de duplicatas:\n")
        print(df_limpo['gênero'].value_counts())

        # Salvar o novo CSV
        df_limpo.to_csv(caminho_saida, index=False)
        print(f"\n📁 Dataset limpo salvo como: {caminho_saida}")

# Executa se rodar diretamente o script
if __name__ == "__main__":
    verificador = DuplicatasMusicais("dataset_musical_expandido.csv")
    verificador.salvar_dataset_limpo()
