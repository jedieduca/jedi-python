import os
import time
import uuid

# Imagens geradas há mais tempo que isso são apagadas (a tela e o PDF usam a imagem logo após gerá-la)
TTL_SEGUNDOS = 60 * 60


def caminho_unico(path_relativo: str) -> str:
    """
    'static/estatisticas/img/ranking.jpg' -> 'static/estatisticas/img/ranking_<uuid>.jpg'
    Cada requisição grava o próprio arquivo: usuários com filtros diferentes não sobrescrevem
    a imagem um do outro. Aproveita para apagar as imagens antigas do mesmo gráfico.
    """
    pasta, arquivo = os.path.split(path_relativo)
    nome, ext = os.path.splitext(arquivo)
    _limpar_antigos(pasta, nome, ext)
    return f"{pasta}/{nome}_{uuid.uuid4().hex}{ext}"


def _limpar_antigos(pasta: str, nome: str, ext: str) -> None:
    limite = time.time() - TTL_SEGUNDOS
    try:
        arquivos = os.listdir(pasta)
    except OSError:
        return

    for arquivo in arquivos:
        if arquivo.startswith(f"{nome}_") and arquivo.endswith(ext):
            caminho = os.path.join(pasta, arquivo)
            try:
                if os.path.getmtime(caminho) < limite:
                    os.remove(caminho)
            except OSError:
                pass   # outro worker já apagou
