from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.api.services.validador import ServicoValidador

# Instanciando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServicoBase:
    def __init__(self, repository):
        self._repo = repository
        self._validador: ServicoValidador = ServicoValidador(self._repo)

    async def buscar_atual(self, token: str = Depends(oauth2_scheme)):
        pass

    async def buscar_por_email(self, email: str):
        pass

    def tipo_usuario_in_db(self, *args, **kwargs):
        pass
