'''
from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['argon2'], deprecated='auto')
'''
from fastapi import status, HTTPException
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

CRIPTO = PasswordHasher()

def verificar_senha(senha: str, hash_senha: str) -> bool:
    '''
    Função para verificar se a senha está correta, comparando a senha em texto puro, informada pelo usuário, e o hash da senha
    estará salvo no banco de dados durante a criação da conta.
    '''
    try:
        return CRIPTO.verify(hash_senha, senha)
    except VerifyMismatchError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def gerar_hash_senha(senha: str) -> str:
    '''
    Função que gera e retorna o hash da senha.
    '''
    return CRIPTO.hash(senha)
