from VectorMass.constants import *
from VectorMass.entity import (DatabaseConfig, EmbeddingConfig)

class ConfigurationManager:
    def __init__(self):
        pass

    def database_config(self) -> DatabaseConfig:

        config = DatabaseConfig(
            db_name=DB_NAME
        )
        return config
    
    def embedding_config(self) -> EmbeddingConfig:

        config = EmbeddingConfig(
            default_embedding_model=DEFAULT_EMBEDDING_MODEL
        )
        return config