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

            titulo = await service.montar_titulo_com_filtros("Média de Acertos/Erros por Categoria e Turma", filters)

            # Preparação dos dados: Transformação de Wide para Long (Melt)
            # Mapeamos as colunas do banco para nomes amigáveis
            mapping = {'media_acertos': 'Acerto', 'media_erros': 'Erro'}

            # Transformar para formato longo
            df_melt = df.melt(
                id_vars=['categoria', 'turma'],
                value_vars=['media_acertos', 'media_erros'],
                var_name='Tipo',
                value_name='media'
            )

            # Criar a coluna combinada para o eixo X (ex: "Acerto - Turma A")
            df_melt['Tipo'] = df_melt['Tipo'].replace(mapping)
            df_melt['Legenda_X'] = df_melt['Tipo'] + ' - ' + df_melt['turma']
            
            # Definir a ordem das barras para ficarem agrupadas por turma
            turmas = sorted(df['turma'].unique())
            ordem_x = []
            for t in turmas:
                ordem_x.extend([f"Acerto - {t}", f"Erro - {t}"])
            
            # Chamar a função mestra da classe
            await chart_tool.plot_barplot(
                df=df_melt,
                path_save=path,
                params={
                    'x': 'Legenda_X',
                    'y': 'media',
                    'hue': 'categoria',
                    'order': ordem_x,
                    'titulo': titulo,
                    'label_x': 'Turmas / Tipo',
                    'label_y': 'Média (%)',
                    'ylim': 100
                },
                formato_rotulo="{:.1f}%"
            )            
        except Exception as e:
            print(f"Erro no serviço de gráficos: {e}")
            raise e

    @staticmethod
    async def criar_grafico_partida(data, path: str, filters: Any = None):
        try:
            # Transformação de dados (Camada de Serviço)
            df = await service.transforma_em_dataframe(data)

            titulo = await service.montar_titulo_com_filtros("Desempenho Médio: Partida Inicial vs Partida Final", filters)
            
            # Mapeamento para nomes amigáveis na legenda
            mapping = {'PI': 'Partida Inicial', 'PF': 'Partida Final'}
            
            # Transformação de Wide para Long
            df_melt = df.melt(
                id_vars=['escola', 'turma'], 
                value_vars=['PI', 'PF'], 
                var_name='momento', 
                value_name='media'
            )
            
            # Substitui os nomes técnicos pelos nomes do mapping
            df_melt['momento'] = df_melt['momento'].replace(mapping)
            
            # Criar a legenda do eixo X combinando Escola e Turma
            df_melt['eixo_x'] = df_melt['escola'] + " (" + df_melt['turma'] + ")"
            
            # Definir a ordem das barras (Agrupar Pré e Pós por Escola/Turma)
            eixos_unicos = df_melt['eixo_x'].unique()
            ordem_x = sorted(eixos_unicos)

            # Chamada da classe ChartGenerator
            await chart_tool.plot_barplot(
                df=df_melt,
                path_save=path,
                params={
                    'x': 'eixo_x',
                    'y': 'media',
                    'hue': 'momento', # O que diferencia as cores das barras
                    'order': ordem_x,
                    'titulo': titulo,
                    'label_x': 'Escola (Turma)',
                    'label_y': 'Média de Acertos (%)',
                    'ylim': 100,
                    'palette': ['#34495e', '#2ecc71'] # Cores customizadas (Cinza e Verde)
                },
                formato_rotulo="{:.1f}%"
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
            
            # Chamada à ferramenta de plotagem (Apresentação)
            await chart_tool.plot_barplot(
                df=df_melt,
                path_save=path,
                params={
                    'x': 'categoria',
                    'y': 'quantidade',
                    'hue': 'tipo_noticia',
                    'titulo': titulo,
                    'label_x': 'Categorias',
                    'label_y': 'Quantidade de Respostas',
                    'palette': ['#e74c3c', '#2ecc71'],
                    'ylim': df_melt['quantidade'].max()
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
