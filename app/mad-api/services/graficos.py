from typing import List, Dict, Tuple, Any
from wordcloud import WordCloud
import pandas as pd
from services.data_processing import DataProcessingService
from api.v1.endpoints.utils.ChartGenerator import chart_tool

service = DataProcessingService()

class GraficosService:
    
    @staticmethod
    async def criar_grafico_avaliacao(data, path: str, filters: Any = None):
        try:
            df = await service.transforma_em_dataframe(data)

            titulo = await service.montar_titulo_com_filtros("Autoavaliação vs Avaliação do Jogo por Escola e Turma", filters)

            # Garante uma linha por (escola, turma, tipo, nota)
            df_pizza = df.groupby(['escola', 'turma', 'tipo_avaliacao', 'nota'], as_index=False)['qtd'].sum()

            await chart_tool.plot_pizzas_comparativas(
                df=df_pizza,
                path_save=path,
                params={
                    'titulo': titulo,
                    'col_grupo': 'tipo_avaliacao',
                    'col_categoria': 'nota',
                    'col_valor': 'qtd',
                    'ordem_grupos': ['Autoavaliação', 'Avaliação do jogo'],
                    'titulo_legenda': 'Nota'
                }
            )
        except Exception as e:
            print(f"Erro no serviço de gráficos: {e}")
            raise e


    @staticmethod
    async def criar_grafico_categoria(data, path: str, filters: Any = None):
        try:
            # Transformação de dados (Camada de Serviço)
            df = await service.transforma_em_dataframe(data)

            # Montar título considerando filtros (ex: Escola X, Categoria Y)
            # Isso ajuda a contexto do gráfico mesmo que os dados sejam parciais
            titulo_base = "Média de Acertos/Erros por Categoria e Turma"
            titulo = await service.montar_titulo_com_filtros(titulo_base, filters)

            # Preparação dos dados: Transformação de Wide para Long (Melt)
            df_melt = df.melt(
                id_vars=['categoria', 'turma'],
                value_vars=['media_acertos', 'media_erros'],
                var_name='Tipo', # Nome técnico temporário
                value_name='media'
            )

            # Mapeamento para nomes amigáveis na interface
            mapping_tipo = {'media_acertos': 'Acerto', 'media_erros': 'Erro'}
            df_melt['Tipo'] = df_melt['Tipo'].replace(mapping_tipo)
            
            # --- NOVA CHAMADA PARA O GRÁFICO FACETADO ---
            # Em vez de chamar o chart_tool.plot_barplot antigo,
            # chamamos a nossa nova função especializada.
            
            # Você precisará importar a função plot_faceted_categorical_chart aqui
            # ou movê-la para dentro da classe ChartGenerator.

            await chart_tool.plot_faceted_categorical_chart(
                df=df_melt,
                path_save=path,
                params={
                    'titulo': titulo,
                    # Outros parâmetros específicos que sua função de plotagem precise
                }
            )
                      
        except Exception as e:
            print(f"Erro no serviço de gráficos: {e}")
            raise e

    @staticmethod
    async def criar_grafico_partida(data, path: str, filters: Any = None):
        try:
            # Transformação de dados
            df = await service.transforma_em_dataframe(data)

            titulo = await service.montar_titulo_com_filtros("Desempenho Médio: Partida Inicial vs Partida Final", filters)
            
            mapping = {'PI': 'Partida Inicial', 'PF': 'Partida Final'}
            
            # Transformação de Wide para Long
            df_melt = df.melt(
                id_vars=['escola', 'turma'], 
                value_vars=['PI', 'PF'], 
                var_name='momento', 
                value_name='media'
            )
            
            df_melt['momento'] = df_melt['momento'].replace(mapping)
            # df_melt['eixo_y'] = df_melt['escola'] + " (" + df_melt['turma'] + ")"
            df_melt['eixo_y'] = df_melt['turma']

            # Nova chamada direcionada para o gerador no formato horizontal/facetado
            await chart_tool.plot_faceted_partida_chart(
                df=df_melt,
                path_save=path,
                params={
                    'titulo': titulo
                }
            )            
        except Exception as e:
            print(f"Erro no serviço de gráficos: {e}")
            raise e

    @staticmethod
    async def criar_grafico_perfil(data, path: str, filters: Any = None):
        try:
            # Transformação de dados (Camada de Serviço)
            df = await service.transforma_em_dataframe(data)

            titulo = await service.montar_titulo_com_filtros("Comparativo: Notícias Fake vs. Não Fake por Categoria", filters)
            
            # Lógica de negócio específica para a visualização
            df_melt = df.melt(
                id_vars=['categoria'], 
                value_vars=['fake_qt', 'nao_fake_qt'],
                var_name='tipo_noticia', 
                value_name='quantidade'
            )
            
            df_melt['tipo_noticia'] = df_melt['tipo_noticia'].replace({
                'fake_qt': 'Fake', 
                'nao_fake_qt': 'Não Fake'
            })
            
            # Chamada à ferramenta de plotagem com EIXOS INVERTIDOS
            await chart_tool.plot_barplot(
                df=df_melt,
                path_save=path,
                params={
                    'x': 'quantidade',          # Invertido: quantidade agora vai para o eixo X
                    'y': 'categoria',           # Invertido: categoria agora vai para o eixo Y
                    'hue': 'tipo_noticia',
                    'titulo': titulo,
                    'label_x': 'Quantidade de Notícias',  # Rótulo atualizado do eixo X
                    'label_y': 'Categorias',               # Rótulo atualizado do eixo Y
                    'palette': ['#e74c3c', '#2ecc71'],
                    'xlim': df_melt['quantidade'].max()    # Usa limite horizontal em vez de ylim
                },
                formato_rotulo="{:.0f}"
            )
        except Exception as e:
            print(f"Erro no serviço de gráficos: {e}")
            raise e
    
    @staticmethod
    async def gerar_graficos_e_regras(df_regras) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
        try:
            # Preparação: Criar a coluna de texto formatada
            df_regras['regra_formatada'] = df_regras.apply(service.formata_regra_amigavel, axis=1)
            
            # Gerar Gráfico de Dispersão (Todas as Regras)
            path_scatter = "static/regras/img/regras_dispersao.png"
            await chart_tool.plot_scatter(
                df=df_regras,
                path_save=path_scatter,
                params={
                    'x': 'support',
                    'y': 'confidence',
                    'hue': 'lift',
                    'size': 'lift',
                    'titulo': 'Dispersão das Regras (Suporte vs Confiança)'
                }
            )
            
            # Gerar Gráfico Top 10 (Baseado no Lift)
            df_top10 = df_regras.nlargest(10, 'lift')
            path_top10 = "static/regras/img/regras_top10.png"
            await chart_tool.plot_horizontal_bars(
                df=df_top10,
                path_save=path_top10,
                params={
                    'x': 'lift',
                    'y': 'regra_formatada',
                    'titulo': 'Top 10 Regras por Lift (Força de Associação)',
                    'label_x': 'Valor de Lift'
                }
            )

            # Preparar JSON
            rules_list = df_regras[['antecedents', 'consequents', 'support', 'confidence', 'lift']].copy()
            rules_list['antecedents'] = rules_list['antecedents'].apply(list)
            rules_list['consequents'] = rules_list['consequents'].apply(list)
            
            return rules_list.to_dict(orient='records'),{
                "grafico_lift": path_top10,
                "grafico_dispersao": path_scatter
            }
        except Exception as e:
            print(f"Erro no serviço de gráficos: {e}")
            raise e       
    
    @staticmethod
    async def criar_nuvem_palavaras(nuvem: WordCloud, path: str):
        try:
            
            # Apenas delegamos para a classe mestre
            await chart_tool.plot_wordcloud(
                nuvem=nuvem, 
                path_save=path,
                titulo= 'Nuvem de Palavras das Notícias'
            )        
        except Exception as e:
            print(f"Erro no serviço de gráficos: {e}")
            raise e

    @staticmethod
    async def criar_grafico_ranking_partidas(data, path: str, filters: Any = None):
        try:
            df = await service.transforma_em_dataframe(data)

            # Garante ordenação e tipo numérico
            df = await service.preparar_dados_ranking(df, coluna_quantidade='numero_partidas')

            df = df.sort_values(by='numero_partidas', ascending=False)

            # Cria rótulo do eixo Y composto: Escola - Turma - Aluno
            df['rotulo_aluno'] = df['escola'] + " | " + df['turma'] + " | " + df['aluno']

            titulo = await service.montar_titulo_com_filtros("Ranking de Partidas Jogadas por Aluno", filters)

            await chart_tool.plot_ranking_horizontal_bars(
                df=df,
                path_save=path,
                params={
                    'x': 'numero_partidas',
                    'y': 'rotulo_aluno',
                    'titulo': titulo,
                    'label_x': 'Quantidade de Partidas',
                    'label_y': 'Escola | Turma | Aluno',
                    'palette': 'viridis'
                }
            )
        except Exception as e:
            print(f"Erro no serviço de gráficos de ranking: {e}")
            raise e

    @staticmethod
    async def criar_grafico_perfil_escolas(data, path: str, filters: Any = None):
        try:
            df = await service.transforma_em_dataframe(data)

            titulo = await service.montar_titulo_com_filtros("Distribuição Qualitativa e Quantitativa por Escola", filters)

            # Transformação WIDE para LONG
            df_melt = df.melt(
                id_vars=['escola'],
                value_vars=['num_turmas', 'num_discentes', 'num_docentes', 'num_gestores', 'num_secretarios'],
                var_name='metrica',
                value_name='quantidade'
            )

            # Mapeamento de rótulos amigáveis
            labels_map = {
                'num_turmas': 'Turmas',
                'num_discentes': 'Discentes',
                'num_docentes': 'Docentes',
                'num_gestores': 'Gestores',
                'num_secretarios': 'Secretaria'
            }
            df_melt['metrica'] = df_melt['metrica'].replace(labels_map)

            await chart_tool.plot_perfil_escolas_chart(
                df=df_melt,
                path_save=path,
                params={'titulo': titulo}
            )
        except Exception as e:
            print(f"Erro no serviço de gráfico de perfil das escolas: {e}")
            raise e 

    @staticmethod
    async def criar_grafico_capacidade_critica(data, path: str, filters: Any = None):
        try:
            df = await service.transforma_em_dataframe(data)

            # 1. Agrupa e conta a quantidade absoluta por Escola, Turma e Capacidade Crítica
            df_agrupado = df.groupby(['escola', 'turma', 'capacidade_critica']).size().reset_index(name='quantidade')

            # 2. Calcula o Total de cada Turma para obter o percentual individual
            df_agrupado['total_turma'] = df_agrupado.groupby(['escola', 'turma'])['quantidade'].transform('sum')
            
            # 3. Calcula o percentual da capacidade crítica dentro daquela escola/turma
            df_agrupado['percentual'] = (df_agrupado['quantidade'] / df_agrupado['total_turma']) * 100

            titulo = await service.montar_titulo_com_filtros("Distribuição de Capacidade Crítica por Escola e Turma", filters)

            # Chama o gerador de gráfico enviando os dados já agrupados e calculados
            await chart_tool.plot_capacidade_critica_chart(
                df=df_agrupado,
                path_save=path,
                params={'titulo': titulo}
            )
        except Exception as e:
            print(f"Erro no serviço de gráficos de capacidade crítica: {e}")
            raise e

    @staticmethod
    async def criar_grafico_analise_idade(data, path: str, filters: Any = None):
        try:
            df = await service.transforma_em_dataframe(data)

            # 1. Garante tipo numérico e remove jogadores sem idade (não entram no gráfico)
            df['idade'] = pd.to_numeric(df['idade'], errors='coerce')
            df = df.dropna(subset=['idade'])

            if df.empty:
                raise ValueError("Nenhum jogador com idade informada para gerar o gráfico.")

            df['escola'] = df['escola'].fillna('Escola não informada')
            df['turma'] = df['turma'].fillna('Turma não informada')

            # 2. Quantidade de alunos em cada escola/turma (exibida no rótulo)
            df['n'] = df.groupby(['escola', 'turma'])['idade'].transform('size')

            # 3. Rótulo do eixo Y: se já filtrou por escola, mostra apenas a turma
            filtrou_escola = bool(filters and filters.escola)
            if filtrou_escola:
                df['rotulo'] = df['turma'] + " (n=" + df['n'].astype(str) + ")"
                label_y = 'Turma'
            else:
                df['rotulo'] = df['escola'] + " | " + df['turma'] + " (n=" + df['n'].astype(str) + ")"
                label_y = 'Escola | Turma'

            # 4. Ordem das caixas: por escola e depois por turma
            ordem = (
                df.sort_values(['escola', 'turma'])['rotulo']
                .drop_duplicates()
                .tolist()
            )

            # 5. Identifica outliers por grupo (mesma regra dos bigodes do boxplot: 1,5 × IQR)
            q1 = df.groupby('rotulo')['idade'].transform(lambda s: s.quantile(0.25))
            q3 = df.groupby('rotulo')['idade'].transform(lambda s: s.quantile(0.75))
            iqr = q3 - q1
            df['outlier'] = (df['idade'] < q1 - 1.5 * iqr) | (df['idade'] > q3 + 1.5 * iqr)


            titulo = await service.montar_titulo_com_filtros("Distribuição de Idade por Escola e Turma", filters)

            await chart_tool.plot_boxplot_idade_chart(
                df=df,
                path_save=path,
                params={
                    'x': 'idade',
                    'y': 'rotulo',
                    'order': ordem,
                    'titulo': titulo,
                    'label_x': 'Idade (anos)',
                    'label_y': label_y,
                    'col_outlier': 'outlier',
                    'col_id': 'id_jogador'
                }
            )
        except Exception as e:
            print(f"Erro no serviço de gráficos de análise de idade: {e}")
            raise e
