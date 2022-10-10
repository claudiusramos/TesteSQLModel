import random

from time import sleep

from tqdm import tqdm

import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker

from pathlib import Path  # Usado no SQLite (Instalado por padrão no python)
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.future.engine import Engine

from models.model_base import ModelBase

__engine: Optional[Engine] = None  # Conexão com o banco


def create_engine(sqlite: bool = False) -> Engine:
    """
        Função para configurar a conexão com o banco de dados
    """
    global __engine

    if __engine:
        return

    if sqlite:
        arquivo_db = 'db/pjg2g.sqlite'
        folder = Path(arquivo_db).parent
        folder.mkdir(parents=True, exist_ok=True)

        conn_str = f'sqlite:///{arquivo_db}'
        __engine = sa.create_engine(url=conn_str, echo=False, connect_args={"check_same_thread": False})

    else:
        conn_str = "posgresql://usuario:senha@localhost:5432/pje2g"
        __engine = sa.create_engine(url=conn_str, echo=False)

    return __engine


def create_session() -> Session:
    """
        Função para configurar a sessão de conexão ao banco de dados
    """

    global __engine

    if not __engine:
        create_engine(sqlite=True)

    __session = sessionmaker(__engine, expire_on_commit=False, class_=Session)

    session: Session = __session()

    return session


def gerar_cor() -> str:
    cor = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

    return cor


def create_tables() -> None:
    global __engine

    if not __engine:
        create_engine(sqlite=True)


    import models.__all_models

    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)
