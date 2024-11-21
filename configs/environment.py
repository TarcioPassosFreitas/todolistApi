import os
from functools import lru_cache
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


@lru_cache
def get_env_filename() -> str:
    """
    Retorna o nome do arquivo .env com base na variável de ambiente 'ENV'.
    """
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    """
    Classe de configuração de ambiente, baseada nas variáveis de ambiente do .env.
    """
    API_VERSION: str = Field(..., description="Versão da API")
    APP_NAME: str = Field(..., description="Nome da aplicação")
    DATABASE_DIALECT: str = Field(..., description="Dialeto do banco de dados")
    DATABASE_HOSTNAME: str = Field(..., description="Endereço do host do banco")
    DATABASE_NAME: str = Field(..., description="Nome do banco")
    DATABASE_PASSWORD: str = Field(..., description="Senha do banco")
    DATABASE_PORT: int = Field(..., description="Porta de conexão com o banco")
    DATABASE_USERNAME: str = Field(..., description="Usuário do banco")
    DEBUG_MODE: bool = Field(..., description="Modo de depuração")

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True
    )


@lru_cache
def get_environment_variables() -> EnvironmentSettings:
    """
    Retorna as configurações de ambiente como uma instância de EnvironmentSettings.
    """
    return EnvironmentSettings(_env_file=get_env_filename(), _env_file_encoding="utf-8")
