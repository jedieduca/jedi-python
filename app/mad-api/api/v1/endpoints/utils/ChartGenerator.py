import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import textwrap
import numpy as np

from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch

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

        # Restaura o tema padrão (outros gráficos alteram o rc global do Seaborn)
        sns.set_theme(style="whitegrid")

        # Figura desenhada para 1200 px de largura; altura dá espaço para as regras em várias linhas
        fig, ax = plt.subplots(figsize=(12, 10))
        
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

        ax.set_xlabel(params.get('label_x', ''))
        ax.set_ylabel('')

        # Encaixa as regras (texto à esquerda) dentro dos 12 pol., em vez de alargar a imagem
        fig.tight_layout()

        # Quebra o título para não ultrapassar a largura da figura (senão a imagem inteira é reduzida no navegador)
        fig.suptitle(textwrap.fill(params.get('titulo', ''), width=90), fontsize=16, y=1.0, va='bottom')

        # dpi=200 para nitidez; o CSS exibe a imagem em 1200 px (metade dos pixels)
        fig.savefig(path_save, bbox_inches='tight', dpi=200)
        self._limpar_memoria()
    
    async def plot_scatter(self, df: pd.DataFrame, params: dict, path_save: str):
        """
        Gera um gráfico de dispersão, ideal para Regras de Associação (Lift/Suporte).
        """
        self._limpar_memoria()

        # Restaura o tema padrão (outros gráficos alteram o rc global do Seaborn)
        sns.set_theme(style="whitegrid")

        # Figura desenhada para 1200 px de largura
        fig, ax = plt.subplots(figsize=(12, 7))

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

        ax.set_xlabel(params.get('label_x', ''))
        ax.set_ylabel(params.get('label_y', ''))

        # Ajusta a legenda para não ficar em cima dos pontos
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        fig.tight_layout()

        # Quebra o título para não ultrapassar a largura da figura (senão a imagem inteira é reduzida no navegador)
        fig.suptitle(textwrap.fill(params.get('titulo', ''), width=90), fontsize=16, y=1.0, va='bottom')

        # dpi=200 para nitidez; o CSS exibe a imagem em 1200 px (metade dos pixels)
        fig.savefig(path_save, dpi=200, bbox_inches='tight')
        self._limpar_memoria()

    async def plot_wordcloud(self, nuvem, path_save: str, titulo: str = None):
        """
        Gera e salva uma nuvem de palavras padronizada.
        """
        self._limpar_memoria()
        
        # Figura desenhada para 1200 px de largura (mesma proporção 2:1 da nuvem)
        fig = plt.figure(figsize=(12, 6))
        
        # Exibe a nuvem de palavras
        plt.imshow(nuvem, interpolation='bilinear')
        
        # Remove os eixos (bordas com números) que não fazem sentido para nuvens
        plt.axis("off") 
        
        if titulo:
            # Quebra o título para não ultrapassar a largura da figura
            plt.title(textwrap.fill(titulo, width=90), fontsize=16, pad=20)
            
        # Ajuste firme para não haver bordas brancas desnecessárias
        plt.tight_layout(pad=0)
        
        # dpi=200: a nuvem (2400 px) é gravada sem reamostragem; o CSS a exibe em 1200 px
        fig.savefig(path_save, bbox_inches='tight', dpi=200)
        
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

        # Restaura o tema padrão (outros gráficos alteram o rc global do Seaborn)
        sns.set_theme(style="whitegrid")

        # 1. Identifica a orientação baseando-se na coluna passada no eixo Y
        col_x = str(params.get('x'))
        col_y = str(params.get('y'))

        is_horizontal = params.get('orientacao') == 'h' or col_y == 'categoria' or params.get('x') == 'quantidade'

        # Ajusta a proporção da imagem (dá mais altura física se for horizontal para não encavalar)
        num_itens = df[col_y].nunique() if is_horizontal and col_y in df.columns else 8
        altura_figura = max(6, num_itens * 0.6) if is_horizontal else 8

        # Figura desenhada para 1200 px de largura
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
            
        ax.set_xlabel(params.get('label_x', ''))
        ax.set_ylabel(params.get('label_y', ''))

        # 4. Remove a legenda automática do Seaborn (será recriada acima do gráfico, se houver)
        handles, labels = ax.get_legend_handles_labels()
        if ax.get_legend():
            ax.get_legend().remove()

        fig.tight_layout()

        # 5. Legenda e título acima do gráfico (não aumentam a largura da imagem)
        if handles:
            fig.legend(
                handles, labels,
                loc='lower center',
                ncol=len(labels),
                bbox_to_anchor=(0.5, 1 + 0.15 / altura_figura),
                frameon=False
            )

        # Quebra o título para não ultrapassar a largura da figura (senão a imagem inteira é reduzida no navegador)
        fig.suptitle(textwrap.fill(params.get('titulo', ''), width=90), fontsize=16, y=1 + 0.7 / altura_figura, va='bottom')

        # 6. dpi=200 para nitidez; o CSS exibe a imagem em 1200 px (metade dos pixels)
        fig.savefig(path_save, dpi=200, bbox_inches='tight')

        self._limpar_memoria()

    async def plot_faceted_categorical_chart(self, df: pd.DataFrame, path_save: str, params: dict):
        """
        Gera um gráfico facetado legível para médias por categoria, turma e tipo (Acerto/Erro).
        Projetado para substituir gráficos de barras agrupados saturados.
        """
        try:
            # 1. Tema com fontes no tamanho real de exibição (figura desenhada para 1200 px de largura)
            sns.set_theme(style="whitegrid", rc={
                "axes.facecolor": "#f8f9fa",
                "font.size": 12,
                "axes.labelsize": 12,
                "axes.titlesize": 14,
                "xtick.labelsize": 11,
                "ytick.labelsize": 12
            })
            
            df_plot = df.copy()
            
            tipo_order = ['Acerto', 'Erro']
            df_plot['Tipo'] = pd.Categorical(df_plot['Tipo'], categories=tipo_order, ordered=True)
            
            turmas_unicas = sorted(df_plot['turma'].unique())
            df_plot['turma'] = pd.Categorical(df_plot['turma'], categories=turmas_unicas, ordered=True)

            num_categorias = df_plot['categoria'].nunique()
            paleta_cores = "tab10" if num_categorias <= 10 else "tab20"

            num_turmas = len(turmas_unicas)

            # 2. Altura proporcional ao número de barras (0,3 pol. por categoria + respiro entre turmas)
            largura_fig = 12
            altura_fig = max(4.0, num_turmas * (num_categorias * 0.3 + 0.8))

            g = sns.catplot(
                data=df_plot,
                kind="bar",
                x="media",
                y="turma",
                hue="categoria",
                col="Tipo",
                palette=paleta_cores,
                height=altura_fig,
                aspect=1.0,
                sharex=True
            )

            g.fig.set_size_inches(largura_fig, altura_fig)

            # 3. Títulos e eixos
            g.set_titles(col_template="{col_name}", pad=10)
            g.set_axis_labels("Média (%)", "Turma")
            g.set(xlim=(0, 120))

            g.axes[0, 0].set_yticklabels(turmas_unicas, color='#111111')

            # 4. Percentuais na ponta das barras
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

            # 5. Ajusta os painéis à figura (rect explícito ignora o espaço da legenda lateral original)
            g.tight_layout(rect=[0, 0, 1, 1])

            # 6. Legenda abaixo do gráfico (não aumenta a largura da imagem)
            if g._legend:
                sns.move_legend(
                    g,
                    loc="upper center",
                    bbox_to_anchor=(0.5, 0),
                    ncol=min(4, num_categorias),
                    title="Categorias",
                    title_fontsize=12,
                    fontsize=12,
                    frameon=False
                )

            # 7. Título principal acima dos painéis
            titulo_formatado = params.get('titulo', 'Média de Acertos/Erros por Categoria e Turma')
            # Quebra o título para não ultrapassar a largura da figura (senão a imagem inteira é reduzida no navegador)
            g.fig.suptitle(textwrap.fill(titulo_formatado, width=90), fontsize=16, y=1.0, va='bottom')

            # 8. dpi=200 para nitidez; o CSS exibe a imagem em 1200 px (metade dos pixels)
            g.savefig(path_save, dpi=200, bbox_inches='tight', pad_inches=0.15)
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

            # 2. Figura desenhada para 1200 px de largura
            altura_fig = max(4.5, len(eixos_y_unicos) * 1.2)
            fig, ax = plt.subplots(figsize=(12, altura_fig))

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
            ax.set_ylabel("Escola | Turma")
            ax.set_xlim(0, 115)
            # Quebra os rótulos longos (Escola | Turma) para não espremer a área das barras
            ax.set_yticks(range(len(eixos_y_unicos)))
            ax.set_yticklabels([textwrap.fill(e, width=40) for e in eixos_y_unicos], color='#111111')

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

            # 5. Remove a legenda automática do Seaborn (será recriada acima do gráfico)
            handles, labels = ax.get_legend_handles_labels()
            if ax.get_legend():
                ax.get_legend().remove()

            fig.tight_layout()

            # 6. Legenda e título acima do gráfico (não aumentam a largura da imagem)
            fig.legend(
                handles, labels,
                title="Momento",
                loc='lower center',
                ncol=len(labels),
                bbox_to_anchor=(0.5, 1 + 0.15 / altura_fig),
                frameon=False
            )

            # Quebra o título para não ultrapassar a largura da figura (senão a imagem inteira é reduzida no navegador)
            titulo_formatado = params.get('titulo', 'Desempenho Médio: Partida Inicial vs Partida Final')
            fig.suptitle(textwrap.fill(titulo_formatado, width=90), fontsize=16, y=1 + 0.9 / altura_fig, va='bottom')

            # 7. dpi=200 para nitidez; o CSS exibe a imagem em 1200 px (metade dos pixels)
            fig.savefig(path_save, dpi=200, bbox_inches='tight', pad_inches=0.15)
            self._limpar_memoria()

        except Exception as e:
            print(f"Erro ao gerar gráfico de partida facetado: {e}")
            raise e

    # api/v1/endpoints/utils/ChartGenerator.py

    async def plot_ranking_horizontal_bars(self, df: pd.DataFrame, path_save: str, params: dict):
        """Gera um gráfico de barras horizontais ordenado de forma decrescente."""
        try:
            self._limpar_memoria()

            # Restaura o tema padrão (outros gráficos alteram o rc global do Seaborn)
            sns.set_theme(style="whitegrid")

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

            # Quebra os rótulos longos (Escola | Turma | Aluno) para não espremer a área das barras
            ax.set_yticks(ax.get_yticks())
            ax.set_yticklabels([textwrap.fill(t.get_text(), width=45) for t in ax.get_yticklabels()])

            ax.set_xlabel(params.get('label_x', 'Número de Partidas'))
            ax.set_ylabel(params.get('label_y', 'Aluno / Turma / Escola'))

            fig.tight_layout()

            # Quebra o título para não ultrapassar a largura da figura (senão a imagem inteira é reduzida no navegador)
            fig.suptitle(textwrap.fill(params.get('titulo', ''), width=90), fontsize=16, y=1.0, va='bottom')

            # dpi=200 para nitidez; o CSS exibe a imagem em 1200 px (metade dos pixels)
            fig.savefig(path_save, dpi=200, bbox_inches='tight')
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
            altura_fig = max(6, num_escolas * 1.5)

            # Figura desenhada para 1200 px de largura
            fig, ax = plt.subplots(figsize=(12, altura_fig))
            
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
                            fontsize=11,
                            xytext=(4, 0),
                            textcoords='offset points'
                        )

            # Folga no eixo X para o rótulo da maior barra não ser cortado
            ax.set_xlim(0, df['quantidade'].max() * 1.15)

            # Quebra os nomes longos das escolas para não espremer a área das barras
            ax.set_yticks(ax.get_yticks())
            ax.set_yticklabels([textwrap.fill(t.get_text(), width=30) for t in ax.get_yticklabels()])

            ax.set_xlabel("Quantidade")
            ax.set_ylabel("Escola")

            # Remove a legenda automática do Seaborn (será recriada acima do gráfico)
            handles, labels = ax.get_legend_handles_labels()
            if ax.get_legend():
                ax.get_legend().remove()

            fig.tight_layout()

            # Legenda e título acima do gráfico (não aumentam a largura da imagem)
            fig.legend(
                handles, labels,
                title="Métricas",
                loc='lower center',
                ncol=len(labels),
                bbox_to_anchor=(0.5, 1 + 0.15 / altura_fig),
                frameon=False
            )

            # Quebra o título para não ultrapassar a largura da figura (senão a imagem inteira é reduzida no navegador)
            titulo = params.get('titulo', 'Perfil Quantitativo por Escola')
            fig.suptitle(textwrap.fill(titulo, width=90), fontsize=16, y=1 + 0.9 / altura_fig, va='bottom')

            # dpi=200 para nitidez; o CSS exibe a imagem em 1200 px (metade dos pixels)
            fig.savefig(path_save, dpi=200, bbox_inches='tight', pad_inches=0.15)
            self._limpar_memoria()
            
        except Exception as e:
            print(f"Erro ao gerar gráfico de perfil de escolas: {e}")
            raise e

    async def plot_capacidade_critica_chart(self, df: pd.DataFrame, path_save: str, params: dict):
        """Gera uma rosca por linha (uma por escola/turma), com a identificação à esquerda e cores fixas por categoria."""
        try:
            self._limpar_memoria()

            # Restaura o tema padrão (outros gráficos alteram o rc global do Seaborn)
            sns.set_theme(style="white")

            turmas_unicas = df[['escola', 'turma']].drop_duplicates().sort_values(['escola', 'turma'])
            num_turmas = len(turmas_unicas)

            if num_turmas == 0:
                return

            # 1. Cor e ordem fixas por categoria: a mesma cor significa a mesma coisa em todas as turmas
            cores_fixas = {'AUMENTOU': '#66bb6a', 'MANTEVE': '#ffca28', 'DIMINUIU': '#ef5350'}
            cor_neutra = '#90a4ae'
            presentes = set(df['capacidade_critica'])
            categorias = [c for c in cores_fixas if c in presentes]
            categorias += sorted(c for c in presentes if c not in cores_fixas)
            cores = {c: cores_fixas.get(c, cor_neutra) for c in categorias}
            ordem = {c: i for i, c in enumerate(categorias)}
            handles = [Patch(facecolor=cores[c], edgecolor='white', label=str(c)) for c in categorias]

            # 2. Uma rosca por linha, desenhada para 750 px de largura (3 pol. para a identificação + 4,5 pol. para a rosca)
            altura_fig = 4.2 * num_turmas

            fig, axes = plt.subplots(nrows=num_turmas, ncols=1, figsize=(7.5, altura_fig), squeeze=False)
            axes = axes.flatten()

            for idx, (_, row) in enumerate(turmas_unicas.iterrows()):
                escola_atual, turma_atual = row['escola'], row['turma']
                ax = axes[idx]

                df_sub = df[(df['escola'] == escola_atual) & (df['turma'] == turma_atual)]
                df_sub = df_sub.sort_values('capacidade_critica', key=lambda s: s.map(ordem))
                total = int(df_sub['quantidade'].sum())

                # Identificação da escola/turma à esquerda da rosca
                rotulo = textwrap.fill(str(escola_atual), width=25) + f"\nTurma: {turma_atual}\n(n = {total})"
                ax.annotate(
                    rotulo,
                    xy=(-0.12, 0.62),
                    xycoords='axes fraction',
                    ha='right',
                    va='bottom',
                    fontsize=12,
                    weight='bold',
                    color='#333333'
                )

                # Legenda repetida em cada linha, logo abaixo da identificação
                ax.legend(
                    handles=handles,
                    title='Capacidade crítica',
                    loc='upper right',
                    bbox_to_anchor=(-0.12, 0.58),
                    fontsize=11,
                    title_fontsize=11,
                    frameon=False
                )

                if total == 0:
                    ax.axis('off')
                    continue

                wedges, _ = ax.pie(
                    df_sub['quantidade'],
                    colors=[cores[c] for c in df_sub['capacidade_critica']],
                    startangle=90,
                    counterclock=False,
                    wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
                )

                # 3. Valores: dentro do anel se a fatia for grande, fora (com linha guia) se for pequena
                for wedge, valor in zip(wedges, df_sub['quantidade']):
                    pct = valor / total * 100
                    texto = f"{int(valor)}\n({pct:.1f}%)"
                    angulo = np.deg2rad((wedge.theta1 + wedge.theta2) / 2)
                    x, y = np.cos(angulo), np.sin(angulo)

                    if pct >= 10:
                        ax.text(
                            0.8 * x, 0.8 * y, texto,
                            ha='center', va='center',
                            fontsize=11, weight='bold', color='#222222'
                        )
                    else:
                        ax.annotate(
                            texto,
                            xy=(x, y),
                            xytext=(1.3 * x, 1.3 * y),
                            ha='left' if x >= 0 else 'right',
                            va='center',
                            fontsize=11,
                            weight='bold',
                            color='#222222',
                            arrowprops=dict(arrowstyle='-', color='#888888', lw=0.8)
                        )

                # Reserva espaço para os rótulos externos sem alcançar o título
                ax.set_xlim(-1.5, 1.5)
                ax.set_ylim(-1.5, 1.5)
                ax.set_aspect('equal', adjustable='box')

            fig.tight_layout()

            # 5. Título acima da grade (a legenda agora se repete em cada linha)
            fig.suptitle(
                # Quebra o título para não ultrapassar a largura da figura (senão a imagem inteira é reduzida no navegador)
                textwrap.fill(params.get('titulo', 'Distribuição de Capacidade Crítica por Escola e Turma'), width=55),
                fontsize=16,
                y=1 + 0.3 / altura_fig,
                va='bottom'
            )

            # dpi=200 para nitidez; o CSS exibe a imagem em 750 px (metade dos pixels)
            fig.savefig(path_save, dpi=200, bbox_inches='tight')
            self._limpar_memoria()

        except Exception as e:
            print(f"Erro ao gerar gráfico de capacidade crítica: {e}")
            raise e

    async def plot_pizzas_comparativas(self, df: pd.DataFrame, path_save: str, params: dict):
        """Gera uma linha por escola/turma, com um gráfico de pizza por grupo (colunas) lado a lado."""
        try:
            self._limpar_memoria()

            # Restaura o tema padrão (outros gráficos alteram o rc global do Seaborn)
            sns.set_theme(style="white")

            col_grupo = params.get('col_grupo')
            col_categoria = params.get('col_categoria')
            col_valor = params.get('col_valor')
            grupos = params.get('ordem_grupos') or sorted(df[col_grupo].unique())

            linhas = df[['escola', 'turma']].drop_duplicates().sort_values(['escola', 'turma'])
            nrows, ncols = len(linhas), len(grupos)

            if nrows == 0:
                return

            # Mesma cor para a mesma nota em todas as pizzas, para permitir a comparação
            categorias = sorted(df[col_categoria].unique())
            paleta = sns.color_palette(params.get('palette', 'RdYlGn'), len(categorias))
            cores = dict(zip(categorias, paleta))
            handles = [Patch(facecolor=cores[c], edgecolor='white', label=str(c)) for c in categorias]

            # Figura desenhada para 1200 px de largura: 3 pol. para o rótulo da escola/turma + 4,5 pol. por pizza
            altura_fig = 4.5 * nrows
            fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols + 3, altura_fig), squeeze=False)

            for i, (_, linha) in enumerate(linhas.iterrows()):
                df_linha = df[(df['escola'] == linha['escola']) & (df['turma'] == linha['turma'])]

                for j, grupo in enumerate(grupos):
                    ax = axes[i, j]
                    df_sub = df_linha[df_linha[col_grupo] == grupo].sort_values(col_categoria)
                    total = int(df_sub[col_valor].sum())

                    if total == 0:
                        ax.set_title(f"{grupo}\n(sem respostas)", fontsize=13)
                        ax.axis('off')
                        continue
                    wedges, _ = ax.pie(
                        df_sub[col_valor],
                        colors=[cores[c] for c in df_sub[col_categoria]],
                        startangle=90,
                        counterclock=False,
                        wedgeprops=dict(edgecolor='white', linewidth=2)
                    )

                    # Rótulo de cada fatia: dentro se for grande, fora (com linha guia) se for pequena
                    for wedge, valor in zip(wedges, df_sub[col_valor]):
                        pct = valor / total * 100
                        texto = f"{int(valor)}\n({pct:.1f}%)"
                        angulo = np.deg2rad((wedge.theta1 + wedge.theta2) / 2)
                        x, y = np.cos(angulo), np.sin(angulo)

                        if pct >= 8:
                            ax.text(
                                0.7 * x, 0.7 * y, texto,
                                ha='center', va='center',
                                fontsize=11, weight='bold', color='#222222'
                            )
                        else:
                            ax.annotate(
                                texto,
                                xy=(x, y),
                                xytext=(1.3 * x, 1.3 * y),
                                ha='left' if x >= 0 else 'right',
                                va='center',
                                fontsize=11,
                                weight='bold',
                                color='#222222',
                                arrowprops=dict(arrowstyle='-', color='#888888', lw=0.8)
                            )

                    # Reserva espaço para os rótulos externos dentro da área do gráfico,
                    # assim eles nunca alcançam o título (que fica acima dessa área)
                    ax.set_xlim(-1.7, 1.7)
                    ax.set_ylim(-1.7, 1.7)
                    ax.set_aspect('equal', adjustable='box')

                    ax.set_title(f"{grupo} (n = {total})", fontsize=13, pad=10)

                # Identificação da escola/turma à esquerda da linha
                rotulo = textwrap.fill(str(linha['escola']), width=25) + f"\nTurma: {linha['turma']}"
                axes[i, 0].annotate(
                    rotulo,
                    xy=(-0.12, 0.62),
                    xycoords='axes fraction',
                    ha='right',
                    va='bottom',
                    fontsize=12,
                    weight='bold',
                    color='#333333'
                )

                # Legenda repetida em cada linha, logo abaixo da identificação
                axes[i, 0].legend(
                    handles=handles,
                    title=params.get('titulo_legenda', ''),
                    loc='upper right',
                    bbox_to_anchor=(-0.12, 0.58),
                    fontsize=11,
                    title_fontsize=11,
                    frameon=False
                )

            fig.tight_layout()

            # Quebra o título para não ultrapassar a largura da figura (senão a imagem inteira é reduzida no navegador)
            fig.suptitle(textwrap.fill(params.get('titulo', ''), width=90), fontsize=16, y=1 + 0.3 / altura_fig, va='bottom')

            # dpi=200 para nitidez; o CSS exibe a imagem em 1200 px (metade dos pixels)
            fig.savefig(path_save, dpi=200, bbox_inches='tight')
            self._limpar_memoria()

        except Exception as e:
            print(f"Erro ao gerar gráfico de pizzas comparativas: {e}")
            raise e

    async def plot_boxplot_idade_chart(self, df: pd.DataFrame, path_save: str, params: dict):
        """Gera boxplot horizontal da distribuição de idades por grupo, com o id dos outliers rotulado."""
        try:
            self._limpar_memoria()

            # Restaura o tema padrão (outros gráficos alteram o rc global do Seaborn)
            sns.set_theme(style="whitegrid")

            col_x = params.get('x', 'idade')
            col_y = params.get('y', 'rotulo')
            col_outlier = params.get('col_outlier')
            col_id = params.get('col_id')
            ordem = params.get('order', sorted(df[col_y].unique()))

            # Separa pontos normais e outliers (se o service não informar a coluna, todos são normais)
            if col_outlier and col_outlier in df.columns:
                df_normais = df[~df[col_outlier]]
                df_outliers = df[df[col_outlier]]
            else:
                df_normais = df
                df_outliers = df.iloc[0:0]

            # Altura proporcional ao número de caixas
            altura = max(5, len(ordem) * 0.6)
            fig, ax = plt.subplots(figsize=(12, altura))

            # Caixas: quartis, mediana e bigodes (calculados com TODOS os pontos)
            sns.boxplot(
                data=df,
                x=col_x,
                y=col_y,
                order=ordem,
                color=params.get('cor', '#3498db'),
                width=0.6,
                showfliers=False,
                boxprops=dict(alpha=0.35),
                medianprops=dict(color='#1f3a5f', linewidth=2),
                ax=ax
            )

            # Pontos normais com espalhamento vertical
            sns.stripplot(
                data=df_normais,
                x=col_x,
                y=col_y,
                order=ordem,
                color='#2c3e50',
                size=4,
                alpha=0.5,
                jitter=0.2,
                ax=ax
            )

            # Outliers: sem espalhamento, agrupados por (grupo, idade) e rotulados com os ids
            if not df_outliers.empty and col_id:
                posicoes = {rotulo: i for i, rotulo in enumerate(ordem)}

                def juntar_ids(ids, limite=5):
                    ids = sorted(int(i) for i in ids)
                    texto = ', '.join(str(i) for i in ids[:limite])
                    if len(ids) > limite:
                        texto += f' +{len(ids) - limite}'
                    return texto

                agrupado = (
                    df_outliers.groupby([col_y, col_x])[col_id]
                    .apply(juntar_ids)
                    .reset_index()
                )

                for idx, row in agrupado.iterrows():
                    y = posicoes[row[col_y]]
                    ax.scatter(
                        row[col_x], y,
                        s=60,
                        color='#e74c3c',
                        edgecolor='white',
                        linewidth=1.5,
                        zorder=3,
                        label='Outlier (id do jogador)' if idx == 0 else None
                    )
                    ax.annotate(
                        f"id: {row[col_id]}",
                        (row[col_x], y),
                        xytext=(0, 9),
                        textcoords='offset points',
                        ha='center',
                        va='bottom',
                        fontsize=10,
                        color='#333333'
                    )

                ax.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='#cccccc')

            # Idade é inteira: evita marcações como 11.5
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            # Quebra os rótulos longos (Escola | Turma (n=...)) para não espremer a área das caixas
            ax.set_yticks(ax.get_yticks())
            ax.set_yticklabels([textwrap.fill(t.get_text(), width=40) for t in ax.get_yticklabels()])

            ax.set_xlabel(params.get('label_x', 'Idade (anos)'))
            ax.set_ylabel(params.get('label_y', 'Escola | Turma'))

            fig.tight_layout()

            # Quebra o título para não ultrapassar a largura da figura (senão a imagem inteira é reduzida no navegador)
            titulo = params.get('titulo', 'Distribuição de Idade por Escola e Turma')
            fig.suptitle(textwrap.fill(titulo, width=90), fontsize=16, y=1.0, va='bottom')

            # dpi=200 para nitidez; o CSS exibe a imagem em 1200 px (metade dos pixels)
            fig.savefig(path_save, dpi=200, bbox_inches='tight')
            self._limpar_memoria()

        except Exception as e:
            print(f"Erro ao gerar gráfico de boxplot de idade: {e}")
            raise e
        
# --- Instância global para uso nos serviços ---
chart_tool = ChartGenerator()