from sqlalchemy.orm import Session
from sqlalchemy.sql.base import _NoArg

from .query import SangrealQuery


class SangrealSession(Session):

    def __init__(
        self,
        bind=None,
        autoflush=True,
        future=True,
        expire_on_commit=True,
        autobegin=True,
        twophase=False,
        binds=None,
        enable_baked_queries=True,
        info=None,
        query_cls=SangrealQuery,
        autocommit=False,
        join_transaction_mode="conditional_savepoint",
        close_resets_only=_NoArg.NO_ARG,
    ):
        super().__init__(bind=bind,
                         autoflush=autoflush,
                         future=future,
                         expire_on_commit=expire_on_commit,
                         autobegin=autobegin,
                         twophase=twophase,
                         binds=binds,
                         enable_baked_queries=enable_baked_queries,
                         info=info,
                         query_cls=query_cls,
                         autocommit=autocommit,
                         join_transaction_mode=join_transaction_mode,
                         close_resets_only=close_resets_only)
