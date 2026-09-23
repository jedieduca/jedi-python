from typing import List, Dict, Tuple, Any
from wordcloud import WordCloud
from services.data_processing import DataProcessingService
from api.v1.endpoints.utils.ChartGenerator import chart_tool

service = DataProcessingService()

class GraficosService:
    
    @staticmethod
    async def criar_grafico_avaliacao(data, path: str, filters: Any = None):
        try:
            # Transformação de dados (Camada de Serviço)
            df = await service.transforma_em_dataframe(data)

            titulo = await service.montar_titulo_com_filtros("Autoavaliação vs Jogo", filters)
          
            # Preparação (Melt)
            df_long = df.melt(
                id_vars='avaliacao', 
                value_vars=['autoavaliacao', 'avaliacao_jogo'], 
                var_name='fonte',
                value_name='pct'
            )
        
            # Chamada simplificada
            await chart_tool.plot_barplot(
                df=df_long,
                path_save=path,
                params={
                    'x': 'avaliacao',
                    'y': 'pct',
                    'hue': 'fonte',
                    'titulo': titulo,
                    'palette': ['royalblue', 'darkorange'],
                    'ylim': 100
                },
                formato_rotulo="{:.1f}%"
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
