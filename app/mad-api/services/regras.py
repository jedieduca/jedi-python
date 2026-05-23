import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from services.graficos import GraficosService
from services.data_processing import DataProcessingService

class RegrasService:
    async def processar_regras_associacao(self, data):
        # Instancia a camada de serviços resposável pela geração dos gráficos
        graficos = GraficosService()
        service = DataProcessingService()
        
        # Transformação inicial
        df = await service.transforma_em_dataframe(data)
            
        # Engenharia de Recursos (Discretização)
        # Isola a regra de negócio: faixas etárias específicas do seu projeto
        df_discre = await service.discretizar_coluna(
            df, 'idade', [0, 18, 35, 60, 100], 
            ['adolescente', 'jovem', 'adulto', 'idoso']
        )
            
        # Preparação One-Hot Encoding
        df_onehot = pd.get_dummies(df_discre[service.colunas_desejadas])
        
        # Execução do Algoritmo Apriori
        frequent_itemsets = apriori(df_onehot, min_support=0.05, use_colnames=True)
        
        with np.errstate(divide='ignore', invalid='ignore'):
            rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.75)

        if rules.empty:
            return None, None
        
        # Geração de saídas (JSON e Imagens)
        regras_json, links_imagens = await graficos.gerar_graficos_e_regras(rules)
        return regras_json, links_imagens