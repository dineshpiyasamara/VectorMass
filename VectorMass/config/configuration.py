from VectorMass.constants import *
from VectorMass.utils.common import read_yaml, create_directories
from VectorMass.entity import (DatabaseConfig, EmbeddingConfig)

class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)


    def database_config(self) -> DatabaseConfig:

        config = DatabaseConfig(
            db_name=self.config.db_name
        )
        return config
    
    def embedding_config(self) -> EmbeddingConfig:

        config = EmbeddingConfig(
            default_embedding_model=self.config.default_embedding_model
        )
        return config