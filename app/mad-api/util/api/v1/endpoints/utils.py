import matplotlib
matplotlib.use('Agg') # Força o backend não-interativo ANTES do pyplot
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Any
from fastapi import HTTPException,status
from wordcloud import WordCloud
from api.v1.endpoints.utils.ChartGenerator import chart_tool
import pandas as pd

colunas_desejadas = [
    'escola',
    'turma',
    'fx_idade',
    'categoria',
    'auto_avaliacao',
    'avaliacao_jogo',
    'capacidade_critica'
]

async def transforma_em_dataframe(lista_modelos: List[Any]) -> pd.DataFrame:
    try:
        """
        Converte uma lista de modelos (Pydantic ou SQLAlchemy) em DataFrame,
        removendo metadados internos do SQLAlchemy.
        """
        if not lista_modelos:
            return pd.DataFrame()

        data = []
        for item in lista_modelos:
            # Se for Pydantic (V2)
            if hasattr(item, 'model_dump'):
                data.append(item.model_dump())
            # Se for Pydantic (V1)
            elif hasattr(item, 'dict'):
                data.append(item.dict())
            # Se for um modelo SQLAlchemy
            else:
                d = dict(vars(item))
                d.pop('_sa_instance_state', None) # Remove o erro de serialização
                data.append(d)
        
        return pd.DataFrame.from_records(data)
    except Exception as e:
        print(f"Erro durante o processo de transformação do DataFrame: {e}")

async def discretizar_coluna(df: pd.DataFrame, campo: str, bins: List[int], rotulos: List[str]) -> pd.DataFrame:
    try:
        """
        Discretiza uma coluna numérica em categorias (bins).
        
        :param df: O DataFrame original.
        :param campo: O nome da coluna (ex: 'idade').
        :param bins: Lista de limites (ex: [0, 18, 35, 60, 100]).
        :param rotulos: Lista de nomes das faixas (ex: ['adolescente', 'jovem', ...]).
        :return: DataFrame com a nova coluna adicionada.
        """
        nome_nova_coluna = f"fx_{campo}"
        
        # Executa a discretização
        df[nome_nova_coluna] = pd.cut(
            df[campo],
            bins=bins,
            labels=rotulos
        )
        
        return df
    except Exception as e:
        print(f"Erro durante o processo de discretização da coluna: {e}")


def limpar_nome(item_set):
    # Remove prefixos comuns gerados pelo get_dummies ou discretização
    substituicoes = ['fx_idade', 'categoria_', 'escola_', 'turma_',  'auto_avaliacao_', 'avaliacao_jogo_', 'capacidade_critica_']
    nova_lista = []
    for item in item_set:
        for s in substituicoes:
            item = item.replace(s, '')
        nova_lista.append(item)
    return nova_lista


async def gerar_graficos_e_regras(regras: pd.DataFrame) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    try:
        # Forçar a limpeza de qualquer gráfico anterior na memória
        plt.clf()
        plt.close('all')

        # --- Top 10 Lift ---
        rules_plot = regras.sort_values(by='lift', ascending=False).head(10)
        plt.figure(figsize=(12, 8))

        # Criando os labels com tratamento de strings
        labels = [f"{limpar_nome(a)} \n=> {limpar_nome(c)}" for a, c in zip(rules_plot['antecedents'], rules_plot['consequents'])]

        plt.barh(range(len(rules_plot)), rules_plot['lift'], color='skyblue')

        plt.yticks(
            range(len(rules_plot)),
            labels,
            fontsize=9,
            va='center'
#            [f"{list(a)} => {list(c)}" for a, c in zip(rules_plot['antecedents'], rules_plot['consequents'])]
        )

        plt.xlabel('Lift')
        plt.title('Top 10 Regras por Lift')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.subplots_adjust(left=0.3)
        path_lift = "static/regras/img/top10_lift.png"
        plt.savefig(path_lift)
        plt.close('all') # Importante: Libera memória

        # --- Dispersão ---
        plt.figure(figsize=(8, 6))
        plt.scatter(regras['support'], regras['confidence'], alpha=0.7, c=regras['lift'], cmap='viridis')
        plt.xlabel('Support')
        plt.ylabel('Confidence')
        plt.colorbar(label='Lift')
        plt.tight_layout()
        path_scatter = "static/regras/img/dispersao.png"
        plt.savefig(path_scatter)
        plt.close('all')

        # Preparar JSON
        rules_list = regras[['antecedents', 'consequents', 'support', 'confidence', 'lift']].copy()
        rules_list['antecedents'] = rules_list['antecedents'].apply(list)
        rules_list['consequents'] = rules_list['consequents'].apply(list)
        
        return rules_list.to_dict(orient='records'),{
            "grafico_lift": "static/regras/img/top10_lift.png",
            "grafico_dispersao": "static/regras/img/dispersao.png"
        }
    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Regras: {e}")


'''
    try:
        # Forçar a limpeza de qualquer gráfico anterior na memória
        plt.clf()
        plt.close('all')

        # 1. Garantir que as colunas sejam numéricas (converte de Decimal/String para Float)
        colunas_valores = ['autoavaliacao', 'avaliacao_jogo']
        for col in colunas_valores:
            if col in dados.columns:
                dados[col] = pd.to_numeric(dados[col], errors='coerce').fillna(0).astype(float)

        # Transformar o DataFrame para formato longo (long-form) para usar no seaborn
        df_long = pd.melt(
            dados,
            id_vars='avaliacao',
            value_vars=colunas_valores,
            var_name='fonte',
            value_name='percentual_acertos'
        )

        # Criar o gráfico de barras com seaborn
        plt.figure(figsize=(10, 6))
        grafico = sns.barplot(
            data=df_long,
            x='avaliacao',
            y='percentual_acertos',
            hue='fonte',
            palette=['royalblue', 'darkorange'],
            errorbar=None
        )

        # ADICIONAR OS VALORES NAS BARRAS (O que faltava)
        for barra in grafico.patches:
            altura = barra.get_height()
            if altura > 0:
                grafico.annotate(
                    f'{altura:.1f}%', # Formata com uma casa decimal e símbolo %
                    (barra.get_x() + barra.get_width() / 2, altura),
                    ha='center', 
                    va='bottom',
                    fontsize=9,
                    fontweight='normal'
                )

        # Ajustes estéticos
        plt.title('Percentual de Acertos por Avaliação (Autoavaliação vs Avaliação do Jogo)')
        plt.xlabel('Avaliação')
        plt.ylabel('Percentual de Acertos (%)')
        plt.ylim(0, 115)
        plt.xticks(rotation=45)
        plt.legend(title='Fonte')
        plt.tight_layout()
        path_avaliacao = "static/estatisticas/img/acertos_avaliacao.png"
        plt.savefig(path_avaliacao)
        # Importante: Libera memória
        plt.close('all')
'''
async def gerar_grafico_avaliacoes(dados: pd.DataFrame, path_imagem: str):
    try:
        # Preparação (Melt)
        df_long = dados.melt(
            id_vars='avaliacao', 
            value_vars=['autoavaliacao', 'avaliacao_jogo'], 
            var_name='fonte',
            value_name='pct'
        )
    
        # Chamada simplificada
        await chart_tool.plot_barplot(
            df=df_long,
            path_save=path_imagem,
            params={
                'x': 'avaliacao',
                'y': 'pct',
                'hue': 'fonte',
                'titulo': 'Autoavaliação vs Jogo',
                'palette': ['royalblue', 'darkorange']
            }
        )
    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Avaliações: {e}")

async def gerar_grafico_categoria_turma(dados: pd.DataFrame):
    try:
        # Forçar a limpeza de qualquer gráfico anterior na memória
        plt.clf()
        plt.close('all')

        # Transformar para formato longo
        df_meltado = dados.melt(
            id_vars=['categoria', 'turma'],
            value_vars=['media_acertos', 'media_erros'],
            var_name='Tipo',
            value_name='Média'
        )
        
        # Normalização dos nomes para bater com a 'ordem'
        # Transformamos 'media_acertos' em 'acerto' e 'media_erros' em 'erro'        
        df_meltado['Tipo'] = df_meltado['Tipo'].replace({
            'media_acertos': 'acerto', 
            'media_erros': 'erro'
        })

        # Criar coluna combinando tipo e turma para o eixo X
        df_meltado['Tipo_Turma'] = df_meltado['Tipo'] + ' - ' + df_meltado['turma']

        # Identifica quais turmas realmente existem nos dados recebidos após o filtro
        turmas_na_base = dados['turma'].unique() 

        # Cria a ordem dinamicamente baseada no que foi encontrado
        # Isso garante que a ordem 'Acerto' seguido de 'Erro' se mantenha para cada turma
        ordem_dinamica = []
        for t in sorted(turmas_na_base): # sorted garante ordem alfabética (Turma A, B...)
            ordem_dinamica.append(f'acerto - {t}')
            ordem_dinamica.append(f'erro - {t}')

        # Criar o gráfico de barras com seaborn
        plt.figure(figsize=(10, 6))

        grafico = sns.barplot(
            data=df_meltado,
            x='Tipo_Turma',
            y='Média',
            hue='categoria',
            order=ordem_dinamica,
            palette='Set2')
        
        # Adiciona os valores nas barras
        for barra in grafico.patches:
            altura = barra.get_height()
            if altura > 0:
                grafico.annotate(
                    f'{altura:.0f}%',
                    (barra.get_x() + barra.get_width() / 2, altura),
                    ha='center',
                    va='bottom',
                    fontsize=9
                )
            
        # Ajustes finais
        plt.title('Percentual de Acerto/Erro por Turma e Categoria', fontsize=14)
        plt.xlabel('Tipo de Resposta por Turma')
        plt.ylabel('Média')
        plt.ylim(0, 100)
        plt.legend(title='Categoria')
        plt.tight_layout()

        path_avaliacao = "static/estatisticas/img/categoria_turma.png"
        plt.savefig(path_avaliacao)
        # Importante: Libera memória
        plt.close('all')
    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Categorias: {e}") 

async def gerar_grafico_partida_escola(dados: pd.DataFrame):
    try:

        # Forçar a limpeza de qualquer gráfico anterior na memória
        plt.clf()
        plt.close('all')
        
        # Transformar para formato longo
        df_meltado = dados.melt(
            id_vars=['escola', 'turma'],
            value_vars=['PI', 'PF'],
            var_name='Tipo',
            value_name='Média'
        )
        
        # Criar coluna combinando tipo e turma para o eixo X
        df_meltado['Tipo_Turma'] = df_meltado['Tipo'] + ' - ' + df_meltado['turma']

        # Definir ordem personalizada
        # ordem = ['PI - Turma A', 'PF - Turma A', 'PI - Turma B', 'PF - Turma B', 'PI - Turma C', 'PF - Turma C']
        # Identifica quais turmas realmente existem nos dados recebidos após o filtro
        turmas_na_base = dados['turma'].unique() 

        # Cria a ordem dinamicamente baseada no que foi encontrado
        # Isso garante que a ordem 'Acerto' seguido de 'Erro' se mantenha para cada turma
        ordem_dinamica = []
        for t in sorted(turmas_na_base): # sorted garante ordem alfabética (Turma A, B...)
            ordem_dinamica.append(f'PI - {t}')
            ordem_dinamica.append(f'PF - {t}') 

        # Criar o gráfico de barras com seaborn
        plt.figure(figsize=(10, 6))

        # Supondo que sua lista de cores seja algo como:
        cores = ["#3498db", "#e74c3c"] 
 
        # Verifique quantos itens únicos existem na coluna que você está plotando
        # Se estiver plotando por 'escola', por exemplo:
        n_colors = dados['escola'].nunique()

        grafico = sns.barplot(
            data=df_meltado,
            x='Tipo_Turma',
            y='Média',
            hue='escola',
            order=ordem_dinamica,
            palette=cores[:n_colors] # Fatia a lista para o tamanho exato
            # palette=['royalblue', 'darkorange']
        )
        
        # Adiciona os valores nas barras
        for barra in grafico.patches:
            altura = barra.get_height()
            if altura > 0:
                grafico.annotate(
                    f'{altura:.2f}%',
                    (barra.get_x() + barra.get_width() / 2, altura),
                    ha='center',
                    va='bottom',
                    fontsize=9
                )
            
        # Ajustes finais
        plt.title('Percentual de Acertos por Tipo da Partida e Turma', fontsize=14)
        plt.xlabel('Desempenho por Tipo da Partida e Turma')
        plt.ylabel('Média')
        plt.ylim(0, 100)
        plt.legend(title='escola')
        plt.tight_layout()

        path_avaliacao = "static/estatisticas/img/escola_turma.png"
        plt.savefig(path_avaliacao)
        # Importante: Libera memória
        plt.close('all')
    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Partidas: {e}") 

async def gerar_grafico_perfil_noticia(dados: pd.DataFrame):
    try:
        # 1. Limpeza total antes de começar
        plt.clf()
        plt.close('all')

        # 2. Conversão explícita para garantir que o filtro numérico funcione no plot
        dados['fake_qt'] = pd.to_numeric(dados['fake_qt'], errors='coerce').fillna(0)
        dados['nao_fake_qt'] = pd.to_numeric(dados['nao_fake_qt'], errors='coerce').fillna(0)
        
        # 3. Criar figura e eixo explicitamente
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 4. Plotar definindo EXPLICITAMENTE as colunas (isso remove o ID automaticamente)
        dados.plot(
            kind='bar',
            x='categoria', # Deve ser minúsculo conforme seu Model
            y=['fake_qt', 'nao_fake_qt'],
            ax=ax,
            color=['#e74c3c', '#2ecc71'],
            label=['Fake', 'Não Fake']
        )

        # 5. Configurações de títulos e labels
        ax.set_title('Comparativo: Notícias Fake vs. Não Fake por Categoria')
        ax.set_ylabel('Quantidade')
        ax.set_xlabel('Categoria')
        
        # 6. Adicionar os rótulos de dados (valores em cima das barras)
        for p in ax.patches:
            ax.annotate(str(int(p.get_height())), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', 
                        xytext=(0, 9), 
                        textcoords='offset points')

        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 7. Salvar usando o objeto da figura (fig) em vez de plt
        path_save = "static/estatisticas/img/perfil_noticia.png"
        fig.savefig(path_save)
        plt.close('all') 
        
    except Exception as e:
        print(f"Erro ao gerar gráfico de perfil: {e}")

async def gerar_nuvem_palavras(nuvem: WordCloud):
    try:
        # 1. Limpeza total antes de começar
        plt.clf()
        plt.close('all')

        # 4. Exibindo o resultado
        plt.figure(figsize=(10, 5))
        plt.imshow(nuvem, interpolation='bilinear')
        plt.axis("off") # Remove os eixos do gráfico
        plt.tight_layout(pad=0)
        plt.show()

        path_save = "static/nuvem_palavaras/img/nuvem_palavras.png"
        plt.savefig(path_save)
        # Importante: Libera memória
        plt.close('all') 

        
    except Exception as e:
        print(f"Erro ao gerar gráfico de perfil: {e}")
