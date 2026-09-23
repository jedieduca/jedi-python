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

    @staticmethod
    def _adicionar_rotulos(ax, formato: str, orientacao: str = 'v'):
        """Adiciona rótulos numéricos adaptando-se a barras verticais ou horizontais."""
        for p in ax.patches:
            if orientacao == 'v':
                val = p.get_height()
                if val > 0:
                    ax.annotate(
                        formato.format(val),
                        (p.get_x() + p.get_width() / 2., val),
                        ha='center', va='bottom', fontsize=10, xytext=(0, 3), textcoords='offset points'
                    )
            else:
                val = p.get_width()
                if val > 0:
                    ax.annotate(
                        formato.format(val),
                        (val, p.get_y() + p.get_height() / 2.),
                        ha='left', va='center', fontsize=10, xytext=(4, 0), textcoords='offset points'
                    )

    async def plot_barplot(self, df: pd.DataFrame, params: dict, path_save: str, formato_rotulo: str = "{:.1f}%"):
        """
        Função Mestra de Barras com suporte robusto a orientação Vertical e Horizontal.
        """
        self._limpar_memoria()
        
        # 1. Identifica a orientação baseando-se na coluna passada no eixo Y
        col_x = str(params.get('x'))
        col_y = str(params.get('y'))

        is_horizontal = params.get('orientacao') == 'h' or col_y == 'categoria' or params.get('x') == 'quantidade'

        # Ajusta a proporção da imagem (dá mais altura física se for horizontal para não encavalar)
        num_itens = df[col_y].nunique() if is_horizontal and col_y in df.columns else 8
        altura_figura = max(6, num_itens * 0.6) if is_horizontal else 8

        fig, ax = plt.subplots(figsize=(12, altura_figura))
        
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

        # Formatação condicional e exclusiva
        if is_horizontal:
            self._adicionar_rotulos(ax, formato_rotulo, orientacao='h')
            
            # Ajusta limite X (largura) com folga para os valores das barras não cortarem
            max_val = params.get('xlim', df[params.get('x')].max() if params.get('x') in df else 100)
            ax.set_xlim(0, max_val * 1.15)
            
            # Formatação dos textos do eixo Y (Categorias)
            ax.tick_params(axis='x', rotation=0, labelsize=11)
            ax.tick_params(axis='y', labelsize=11)
        else:
            self._adicionar_rotulos(ax, formato_rotulo, orientacao='v')
            
            # Ajusta limite Y (altura)
            max_val = params.get('ylim', 100)
            ax.set_ylim(0, max_val * 1.15)
            ax.tick_params(axis='x', rotation=45)
            
        # 4. Títulos e rótulos
        ax.set_title(params.get('titulo', ''), fontsize=14, pad=15)
        ax.set_xlabel(params.get('label_x', ''))
        ax.set_ylabel(params.get('label_y', ''))
       
        # 5. Salvamento
        fig.tight_layout()
        fig.savefig(path_save, dpi=100)
        
        self._limpar_memoria()

    async def plot_faceted_categorical_chart(self, df: pd.DataFrame, path_save: str, params: dict):
        """
        Gera um gráfico facetado legível para médias por categoria, turma e tipo (Acerto/Erro).
        Projetado para substituir gráficos de barras agrupados saturados.
        """
        try:
            # 1. Ajuste global do tema e fontes
            sns.set_theme(style="whitegrid", rc={
                "axes.facecolor": "#f8f9fa",
                "font.size": 24,
                "axes.labelsize": 24,
                "axes.titlesize": 24
            })
            
            df_plot = df.copy()
            
            tipo_order = ['Acerto', 'Erro']
            df_plot['Tipo'] = pd.Categorical(df_plot['Tipo'], categories=tipo_order, ordered=True)
            
            turmas_unicas = sorted(df_plot['turma'].unique())
            df_plot['turma'] = pd.Categorical(df_plot['turma'], categories=turmas_unicas, ordered=True)

            num_categorias = df_plot['categoria'].nunique()
            paleta_cores = "tab10" if num_categorias <= 10 else "tab20"

            num_turmas = len(turmas_unicas)

            # --- AJUSTE 1: ALTURA FÍSICA PROPORCIONAL DAS BARRAS ---
            # Dá o espaçamento exato da primeira imagem para não sobrepor os rótulos das 13 categorias
            altura_calculada = max(7.5, (num_turmas * 4.5) + 2.0)

            # 2. Criação da estrutura do gráfico
            g = sns.catplot(
                data=df_plot,
                kind="bar",
                x="media",
                y="turma",
                hue="categoria",
                col="Tipo",
                palette=paleta_cores,
                height=altura_calculada,
                aspect=1.0,
                sharex=True
            )

            # --- AJUSTE DE LARGURA FIXA DA FIGURA ---
            # Força a largura total da figura em polegadas (ex: 16 polegadas de largura fixa)
            g.fig.set_size_inches(16, altura_calculada)

            # 3. Formatação dos títulos e eixos
            g.set_titles(col_template="{col_name}", pad=15, size=22)
            g.set_axis_labels("Média (%)", "Turma")
            g.set(xlim=(0, 120))

            # --- AJUSTE 2: FONTE DO EIXO Y (TURMAS) ---
            g.axes[0, 0].set_yticklabels(turmas_unicas, color='#111111', fontsize=22)

            # --- AJUSTE 3: RÓTULOS DAS PORCENTAGENS NAS BARRAS ---
            for ax in g.axes.flat:
                ax.tick_params(axis='x', labelsize=14)
                for container in ax.containers:
                    for bar in container:
                        val = bar.get_width()
                        if val > 0.1:
                            ax.annotate(
                                f'{val:.1f}%',
                                (val, bar.get_y() + bar.get_height() / 2.),
                                ha='left', va='center',
                                fontsize=14,            # Fonte ajustada para o espaço da barra
                                # fontweight='bold',      # Negrito para destaque imediato
                                xytext=(5, 0),
                                textcoords='offset points',
                                color='#111111'
                            )

            # --- AJUSTE 4: LEGENDA LATERAL ---
            if g._legend:

                sns.move_legend(
                    g, 
                    loc="center left", 
                    bbox_to_anchor=(1.01, 0.5),
                    title="Categorias",
                    title_fontsize=22,      # Tamanho do título da legenda
                    fontsize=22,            # Tamanho da fonte dos ITENS da legenda (igual ao eixo Y) 
                    handletextpad=0.2,      # Reduz o espaço entre o bloco de cor e o texto (padrão é ~0.8)
                    borderaxespad=0.2,      # Ajusta o espaçamento interno das bordas
                    frameon=True,
                    facecolor='white',
                    edgecolor='#cccccc'
                )

                # 2. (Opcional) Aumenta os marcadores/quadradinhos coloridos da legenda para acompanhar o texto grande
                for handle in g._legend.legend_handles:
                    handle.set_height(15)
                    handle.set_width(15)

            # --- AJUSTE 5: TÍTULO PRINCIPAL ---
            titulo_formatado = params.get('titulo', 'Média de Acertos/Erros por Categoria e Turma')
            g.fig.subplots_adjust(top=0.88, wspace=0.30) 
            g.fig.suptitle(titulo_formatado, size=24, y=1.01)

            # --- AJUSTE 6: SALVAMENTO COM DPI BALANCEADO (90 DPI) ---
            # Evita o encolhimento excessivo no navegador mantendo as fontes legíveis no container
            # g.savefig(path_save, dpi=90, bbox_inches='tight', pad_inches=0.15)
            g.savefig(path_save, dpi=100, pad_inches=0.15)
            plt.clf()
            plt.close('all')
        except Exception as e:
            print(f"Erro ao gerar gráfico facetado: {e}")
            raise e

    async def plot_faceted_partida_chart(self, df: pd.DataFrame, path_save: str, params: dict):
        """
        Gera um gráfico horizontal/facetado limpo para a comparação Partida Inicial vs Partida Final.
        """
        try:
            # 1. Configuração de Tema e Fontes
            sns.set_theme(style="whitegrid", rc={
                "axes.facecolor": "#f8f9fa",
                "font.size": 13,
                "axes.labelsize": 15,
                "axes.titlesize": 16,
                "xtick.labelsize": 13,
                "ytick.labelsize": 13,
                "legend.fontsize": 12,
                "legend.title_fontsize": 13
            })
            
            self._limpar_memoria()
            df_plot = df.copy()
            
            # Ordenação de Turmas e Momentos
            momento_order = ['Partida Inicial', 'Partida Final']
            df_plot['momento'] = pd.Categorical(df_plot['momento'], categories=momento_order, ordered=True)
            
            eixos_y_unicos = sorted(df_plot['eixo_y'].unique())
            df_plot['eixo_y'] = pd.Categorical(df_plot['eixo_y'], categories=eixos_y_unicos, ordered=True)

            paleta_partida = ['#34495e', '#2ecc71']

            # 2. Criação do Gráfico Unificado em subplots (Sem Facetas separadas)
            fig, ax = plt.subplots(figsize=(10, max(4.5, len(eixos_y_unicos) * 1.2)))

            sns.barplot(
                data=df_plot,
                x="media",
                y="eixo_y",
                hue="momento",
                palette=paleta_partida,
                ax=ax
            )

            # 3. Formatação dos Eixos
            ax.set_xlabel("Média (%)")
            ax.set_ylabel("Turma")
            ax.set_xlim(0, 115)
            ax.set_yticklabels(eixos_y_unicos, color='#111111')

            # 4. Adição das Porcentagens nas Pontas das Barras
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

            # 5. Posicionamento da Legenda Externa (Mantendo o padrão aprovado)
            plt.legend(
                title="Momento",
                loc="center left",
                bbox_to_anchor=(1.01, 0.5),
                frameon=True,
                facecolor='white',
                edgecolor='#cccccc'
            )

            # 6. Título Principal
            titulo_formatado = params.get('titulo', 'Desempenho Médio: Partida Inicial vs Partida Final')
            ax.set_title(titulo_formatado, size=16, pad=20)

            # 7. Salvar e Limpar Memória
            fig.savefig(path_save, dpi=100, bbox_inches='tight', pad_inches=0.15)
            self._limpar_memoria()

        except Exception as e:
            print(f"Erro ao gerar gráfico de partida facetado: {e}")
            raise e

    # api/v1/endpoints/utils/ChartGenerator.py

    async def plot_ranking_horizontal_bars(self, df: pd.DataFrame, path_save: str, params: dict):
        """Gera um gráfico de barras horizontais ordenado de forma decrescente."""
        try:
            self._limpar_memoria()
            
            # Garante a ordenação decrescente no DataFrame
            df_sorted = df.sort_values(by=params.get('x'), ascending=False)
            
            num_itens = len(df_sorted)
            altura_figura = max(6, num_itens * 0.5)

            fig, ax = plt.subplots(figsize=(12, altura_figura))

            sns.barplot(
                data=df_sorted,
                x=params.get('x'),
                y=params.get('y'),
                palette=params.get('palette', 'Blues_r'),
                ax=ax,
                errorbar=None
            )

            # Adiciona os rótulos de valores no final de cada barra
            self._adicionar_rotulos(ax, formato="{:.0f}", orientacao='h')

            max_val = df_sorted[params.get('x')].max() if not df_sorted.empty else 10
            ax.set_xlim(0, max_val * 1.15)

            ax.set_title(params.get('titulo', ''), fontsize=14, pad=15)
            ax.set_xlabel(params.get('label_x', 'Número de Partidas'))
            ax.set_ylabel(params.get('label_y', 'Aluno / Turma / Escola'))

            fig.tight_layout()
            fig.savefig(path_save, dpi=100, bbox_inches='tight')
            self._limpar_memoria()
        except Exception as e:
            print(f"Erro ao gerar gráfico de ranking: {e}")
            raise e

    async def plot_perfil_escolas_chart(self, df: pd.DataFrame, path_save: str, params: dict):
        """Gera gráfico horizontal agrupado para perfil comparativo de métricas por escola."""
        try:
            self._limpar_memoria()
            
            # Define tema e dimensões proporcionais
            sns.set_theme(style="whitegrid")
            num_escolas = df['escola'].nunique()
            altura = max(6, num_escolas * 1.5)
            
            fig, ax = plt.subplots(figsize=(12, altura))
            
            # Plotagem Agrupada
            sns.barplot(
                data=df,
                x='quantidade',
                y='escola',
                hue='metrica',
                palette='Set2',
                ax=ax
            )
            
            # Rótulos nas pontas das barras
            for container in ax.containers:
                for bar in container:
                    val = bar.get_width()
                    if val > 0:
                        ax.annotate(
                            f'{int(val)}',
                            (val, bar.get_y() + bar.get_height() / 2.),
                            ha='left', va='center',
                            fontsize=10,
                            xytext=(4, 0),
                            textcoords='offset points'
                        )

            ax.set_title(params.get('titulo', 'Perfil Quantitativo por Escola'), fontsize=15, pad=20)
            ax.set_xlabel("Quantidade")
            ax.set_ylabel("Escola")
            
            # Posicionamento da Legenda Externa
            plt.legend(
                title="Métricas",
                loc="center left",
                bbox_to_anchor=(1.01, 0.5),
                frameon=True,
                facecolor='white',
                edgecolor='#cccccc'
            )

            fig.tight_layout()
            fig.savefig(path_save, dpi=100, bbox_inches='tight', pad_inches=0.15)
            self._limpar_memoria()
            
        except Exception as e:
            print(f"Erro ao gerar gráfico de perfil de escolas: {e}")
            raise e        
        
# --- Instância global para uso nos serviços ---
chart_tool = ChartGenerator()