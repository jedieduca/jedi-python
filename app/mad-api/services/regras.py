import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from services.graficos import GraficosService
from services.data_processing import DataProcessingService

class RegrasService:
    async def processar_regras_associacao(self, data, filters=None):
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

        # Mesmo conjunto de regras para o JSON (grid) e para os gráficos
        rules = self.filtrar_regras(rules, filters)

        if rules.empty:
            return None, None

        # Geração de saídas (JSON e Imagens)
        regras_json, links_imagens = await graficos.gerar_graficos_e_regras(rules)
        return regras_json, links_imagens

    @staticmethod
    def filtrar_regras(rules: pd.DataFrame, filters) -> pd.DataFrame:
        if filters is None:
            return rules

        if filters.suporte_min is not None:
            rules = rules[rules['support'] >= filters.suporte_min]
        if filters.confianca_min is not None:
            rules = rules[rules['confidence'] >= filters.confianca_min]
        if filters.lift_min is not None:
            rules = rules[rules['lift'] >= filters.lift_min]

        # "Contém" sem diferenciar maiúsculas, sobre os itens unidos por vírgula (igual ao filtro antigo do PHP)
        if filters.antecedente and filters.antecedente.strip():
            termo = filters.antecedente.strip().lower()
            rules = rules[rules['antecedents'].apply(lambda itens: termo in ', '.join(itens).lower())]
        if filters.consequente and filters.consequente.strip():
            termo = filters.consequente.strip().lower()
            rules = rules[rules['consequents'].apply(lambda itens: termo in ', '.join(itens).lower())]

        # copy(): gerar_graficos_e_regras cria a coluna 'regra_formatada' no DataFrame
        return rules.copy()