import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class ChartGenerator:
    """Classe central para gestão de gráficos da aplicação."""
    
    def __init__(self):
        sns.set_theme(style="whitegrid")
        self.cores_padrao = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f']

    @staticmethod
    def _limpar_memoria():
        """Garante que o backend do Matplotlib não acumule figuras."""
        plt.clf()
        plt.close('all')

    @staticmethod
    def _adicionar_rotulos(ax, formato: str):
        """Itera sobre as barras para adicionar os valores numéricos."""
        for p in ax.patches:
            altura = p.get_height()
            if altura > 0:
                ax.annotate(
                    formato.format(altura),
                    (p.get_x() + p.get_width() / 2., altura),
                    ha='center',
                    va='bottom',
                    fontsize=9,
                    xytext=(0, 3),
                    textcoords='offset points'
                )

    async def plot_horizontal_bars(self, df: pd.DataFrame, params: dict, path_save: str):
        """Gera gráfico de barras horizontais otimizado para textos longos."""

        self._limpar_memoria()
        
        # Aumentamos a altura (figsize) para dar espaço entre as regras
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Criamos o gráfico
        sns.barplot(
            data=df,
            x=params.get('x'),
            y=params.get('y'),
            hue=params.get('y'), 
            palette="flare",
            ax=ax,
            legend=False
        )
        
        # --- MELHORIAS ESPECÍFICAS PARA LEGENDA ---
        
        # 1. Ajuste fino do tamanho da fonte do eixo Y (as regras)
        ax.tick_params(axis='y', labelsize=11) 
        
        # 2. Alinhamento horizontal do texto à direita (encostado na barra)
        plt.setp(ax.get_yticklabels(), ha='right')

        # 3. Adiciona os valores (Lift) nas pontas das barras com respiro
        for p in ax.patches:
            width = p.get_width()
            ax.annotate(f'{width:.2f}', 
                (width, p.get_y() + p.get_height() / 2.),
                ha='left', va='center', fontsize=11, xytext=(8, 0),
                textcoords='offset points', fontweight='bold')

        # --- FIM DAS MELHORIAS ---

        ax.set_title(params.get('titulo', ''), fontsize=16, pad=20)
        ax.set_xlabel(params.get('label_x', ''))
        ax.set_ylabel('')
        
        # bbox_inches='tight' é CRUCIAL aqui para não cortar o texto à esquerda
        fig.savefig(path_save, bbox_inches='tight', dpi=100)
        self._limpar_memoria()
    
    async def plot_scatter(self, df: pd.DataFrame, params: dict, path_save: str):
        """
        Gera um gráfico de dispersão, ideal para Regras de Associação (Lift/Suporte).
        """
        self._limpar_memoria()
        fig, ax = plt.subplots(figsize=(10, 6))

        # O scatter plot do Seaborn para regras
        sns.scatterplot(
            data=df,
            x=params.get('x'),
            y=params.get('y'),
            hue=params.get('hue'),      # Geralmente o 'lift'
            size=params.get('size'),    # Geralmente o 'support'
            palette=params.get('palette', 'viridis'),
            ax=ax
        )

        ax.set_title(params.get('titulo', ''), fontsize=14)
        ax.set_xlabel(params.get('label_x', ''))
        ax.set_ylabel(params.get('label_y', ''))
        
        # Ajusta a legenda para não ficar em cima dos pontos
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        fig.tight_layout()
        fig.savefig(path_save)
        self._limpar_memoria()

    async def plot_wordcloud(self, nuvem, path_save: str, titulo: str = None):
        """
        Gera e salva uma nuvem de palavras padronizada.
        """
        self._limpar_memoria()
        
        # Criamos a figura
        fig = plt.figure(figsize=(10, 5))
        
        # Exibe a nuvem de palavras
        plt.imshow(nuvem, interpolation='bilinear')
        
        # Remove os eixos (bordas com números) que não fazem sentido para nuvens
        plt.axis("off") 
        
        if titulo:
            plt.title(titulo, fontsize=16, pad=20)
            
        # Ajuste firme para não haver bordas brancas desnecessárias
        plt.tight_layout(pad=0)
        
        # Salvamento
        fig.savefig(path_save, bbox_inches='tight')
        
        # Limpa para a próxima requisição
        self._limpar_memoria()

    async def plot_barplot(self, df: pd.DataFrame, params: dict, path_save: str, formato_rotulo: str = "{:.1f}%"):
        """
        Função Mestra de Barras. 
        Substitui a lógica repetitiva de todas as funções de barra do utils.py.
        """
        self._limpar_memoria()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.barplot(
            data=df, 
            x=params.get('x'), 
            y=params.get('y'), 
            hue=params.get('hue'), 
            order=params.get('order'),
            palette=params.get('palette', self.cores_padrao),
            ax=ax,
            errorbar=None
        )    
        
        self._adicionar_rotulos(ax, formato_rotulo)
        
        ax.set_title(params.get('titulo', ''), fontsize=14)
        ax.set_xlabel(params.get('label_x', ''))
        ax.set_ylabel(params.get('label_y', ''))
        plt.ylim(0, params.get('ylim', 100) + 15)
        plt.xticks(rotation=45)
       
        fig.tight_layout()
        fig.savefig(path_save)
        
        self._limpar_memoria()

    async def plot_faceted_categorical_chart(self, df: pd.DataFrame, path_save: str, params: dict):
        """
        Gera um gráfico facetado legível para médias por categoria, turma e tipo (Acerto/Erro).
        Projetado para substituir gráficos de barras agrupados saturados.
        """
        try:
            # 1. Ajuste global de tamanho de fontes (Fontes gigantes em pixels nativos)
            sns.set_theme(style="whitegrid", rc={
                "axes.facecolor": "#f8f9fa",
                "font.size": 14,
                "axes.labelsize": 16,
                "axes.titlesize": 18,
                "xtick.labelsize": 14,
                "ytick.labelsize": 14,
                "legend.fontsize": 13,
                "legend.title_fontsize": 14
            })
            
            df_plot = df.copy()
            
            tipo_order = ['Acerto', 'Erro']
            df_plot['Tipo'] = pd.Categorical(df_plot['Tipo'], categories=tipo_order, ordered=True)
            
            turmas_unicas = sorted(df_plot['turma'].unique())
            df_plot['turma'] = pd.Categorical(df_plot['turma'], categories=turmas_unicas, ordered=True)

            num_categorias = df_plot['categoria'].nunique()
            paleta_cores = "tab10" if num_categorias <= 10 else "tab20"

            # 2. DIMENSÕES FIXAS NATIVAS DE TELA
            # Força o gráfico a nascer na dimensão ideal para telas (evita que o navegador tenha que encolher)
            g = sns.catplot(
                data=df_plot,
                kind="bar",
                x="media",
                y="turma",
                hue="categoria",
                col="Tipo",
                palette=paleta_cores,
                height=5.5,        # Altura nativa em polegadas
                aspect=1.1,        # Proporção horizontal das facetas
                sharex=True
            )

            # 3. Formatação dos títulos e eixos
            g.set_titles(col_template="{col_name}", pad=12)
            g.set_axis_labels("Média (%)", "Turma")
            g.set(xlim=(0, 120))

            # Rótulos do Eixo Y (Turmas)
            g.axes[0, 0].set_yticklabels(turmas_unicas, color='#111111')

            # 4. Valores nas pontas das barras com fonte visível
            for ax in g.axes.flat:
                for container in ax.containers:
                    for bar in container:
                        val = bar.get_width()
                        if val > 0.1:
                            ax.annotate(
                                f'{val:.1f}%',
                                (val, bar.get_y() + bar.get_height() / 2.),
                                ha='left', va='center',
                                fontsize=11,
                                xytext=(4, 0),
                                textcoords='offset points',
                                color='#111111'
                            )

            # 5. Legenda com fonte destacada e fixada à direita
            if g._legend:
                g._legend.set_title("Categoria")
                sns.move_legend(
                    g, 
                    loc="center left", 
                    bbox_to_anchor=(1.01, 0.5), 
                    frameon=True,
                    facecolor='white',
                    edgecolor='#cccccc'
                )

            # 6. Título Principal com espaçamento adequado dos subtítulos
            titulo_formatado = params.get('titulo', 'Média de Acertos/Erros por Categoria e Turma')
            
            # top=0.82 move o topo dos subgráficos para baixo
            g.fig.subplots_adjust(top=0.82, wspace=0.35) 
            
            # y=1.01 posiciona o título principal bem acima dos subtítulos "Acerto" e "Erro"
            g.fig.suptitle(titulo_formatado, size=16, y=1.01)

            # 7. Salva a imagem mantendo a margem
            g.savefig(path_save, dpi=100, bbox_inches='tight', pad_inches=0.15)            
            plt.clf()
            plt.close('all')

        except Exception as e:
            print(f"Erro ao gerar gráfico facetado: {e}")
            raise e
        
# --- Instância global para uso nos serviços ---
chart_tool = ChartGenerator()