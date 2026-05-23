from typing import List, Any
import pandas as pd
import textwrap

class DataProcessingService:
    def __init__(self):
        # Transformamos a lista global em um atributo da classe
        self.colunas_desejadas = [
            'escola',
            'turma',
            'fx_idade',
            'categoria',
            'auto_avaliacao',
            'avaliacao_jogo',
            'capacidade_critica'
        ]

    async def transforma_em_dataframe(self, lista_modelos: List[Any]) -> pd.DataFrame:
        """Converte modelos (Pydantic ou SQLAlchemy) em DataFrame."""
        try:
            if not lista_modelos:
                return pd.DataFrame()

            data = []
            for item in lista_modelos:
                # Lógica para Pydantic V2 ou V1
                if hasattr(item, 'model_dump'):
                    data.append(item.model_dump())
                elif hasattr(item, 'dict'):
                    data.append(item.dict())
                # Lógica para SQLAlchemy
                else:
                    d = dict(vars(item))
                    d.pop('_sa_instance_state', None) 
                    data.append(d)
            
            return pd.DataFrame.from_records(data)
        except Exception as e:
            print(f"Erro na transformação: {e}")
            raise e

    async def discretizar_coluna(self, df: pd.DataFrame, campo: str, bins: List[int], rotulos: List[str]) -> pd.DataFrame:
        """Discretiza uma coluna numérica em categorias."""
        try:
            nome_nova_coluna = f"fx_{campo}"
            df[nome_nova_coluna] = pd.cut(df[campo], bins=bins, labels=rotulos)
            return df
        except Exception as e:
            print(f"Erro na discretização: {e}")
            raise e

    @staticmethod
    def formata_regra_amigavel(row, max_width=40):
        """Método estático pois não depende de dados da instância."""
        ant = str(row['antecedents']).replace("frozenset({", "").replace("})", "")
        con = str(row['consequents']).replace("frozenset({", "").replace("})", "")

        ant = textwrap.fill(ant, width=max_width)
        con = textwrap.fill(con, width=max_width)

        return f"SE {ant}\n ENTÃO {con}"
    
    
    async def montar_titulo_com_filtros(self, titulo_base: str, filters: Any) -> str:
        if not filters:
            return titulo_base
        
        parts = []

        # Converte o objeto de filtros em um dicionário
        # Se for Pydantic V2 use filters.model_dump()
        # Se for Pydantic V1 use filters.dict()
        # Se for uma classe comum, use vars(filters)
        if hasattr(filters, 'model_dump'):
            filtros_dict = filters.model_dump(exclude_none=True)
        elif hasattr(filters, 'dict'):
            filtros_dict = filters.dict(exclude_none=True)
        else:
            filtros_dict = {k: v for k, v in vars(filters).items() if v is not None}

        # Percorre o dicionário gerado dinamicamente
        for campo, valor in filtros_dict.items():
            # Ignora valores vazios ou strings como "Todos"
            if valor and str(valor).lower() != "todos":
                # Formata o nome do campo (ex: 'fx_idade' -> 'Fx Idade')
                label = campo.replace('_', ' ').capitalize()
                parts.append(f"{label}: {valor}")
                
        if not parts:
            return titulo_base
        
        filtros_str = " | ".join(parts)
        
        return f"{titulo_base}\n({filtros_str})"
            
        