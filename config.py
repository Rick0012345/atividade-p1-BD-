#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuração para conexão com MongoDB
Este arquivo contém as configurações para diferentes ambientes de MongoDB.
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

class MongoConfig:
    """Configurações para conexão com MongoDB"""
    
    # Configurações para MongoDB local (sem autenticação)
    LOCAL = {
        'connection_string': 'mongodb://localhost:27017/',
        'database_name': 'crud_database',
        'description': 'MongoDB local sem autenticação'
    }
    
    # Configurações para MongoDB no Docker (host)
    DOCKER_HOST = {
        'connection_string': 'mongodb://admin:password@localhost:27017/',
        'database_name': 'crud_database',
        'description': 'MongoDB rodando em container Docker (acesso do host)'
    }
    
    # Configurações para MongoDB no Docker (container para container)
    DOCKER_CONTAINER = {
        'connection_string': os.getenv(
            'MONGODB_URI',
            'mongodb://admin:password@mongodb:27017/'
        ),
        'database_name': os.getenv('MONGODB_DATABASE', 'crud_database'),
        'description': 'MongoDB rodando em container Docker (acesso entre containers)'
    }
    
    # Configurações para MongoDB Atlas (nuvem)
    ATLAS = {
        'connection_string': os.getenv(
            'MONGODB_ATLAS_URI', 
            'mongodb+srv://<username>:<password>@<cluster>.mongodb.net/'
        ),
        'database_name': os.getenv('MONGODB_DATABASE', 'crud_database'),
        'description': 'MongoDB Atlas (nuvem)'
    }
    
    # Configuração padrão (Docker container)
    DEFAULT = DOCKER_CONTAINER
    
    @classmethod
    def get_config(cls, environment='docker_container'):
        """
        Retorna a configuração para o ambiente especificado
        
        Args:
            environment (str): Ambiente desejado ('local', 'docker_host', 'docker_container', 'atlas')
            
        Returns:
            dict: Configuração do ambiente
        """
        configs = {
            'local': cls.LOCAL,
            'docker_host': cls.DOCKER_HOST,
            'docker_container': cls.DOCKER_CONTAINER,
            'docker': cls.DOCKER_CONTAINER,  # Alias para compatibilidade
            'atlas': cls.ATLAS
        }
        
        return configs.get(environment.lower(), cls.DEFAULT)
    
    @classmethod
    def list_environments(cls):
        """
        Lista todos os ambientes disponíveis
        
        Returns:
            dict: Dicionário com todos os ambientes e suas descrições
        """
        return {
            'local': cls.LOCAL['description'],
            'docker_host': cls.DOCKER_HOST['description'],
            'docker_container': cls.DOCKER_CONTAINER['description'],
            'atlas': cls.ATLAS['description']
        }


    @classmethod
    def auto_detect_environment(cls):
        """
        Detecta automaticamente o ambiente baseado nas variáveis de ambiente
        
        Returns:
            dict: Configuração detectada automaticamente
        """
        # Se estiver rodando em container (variável MONGODB_URI definida)
        if os.getenv('MONGODB_URI'):
            return cls.DOCKER_CONTAINER
        
        # Se MongoDB Atlas URI estiver definida
        if os.getenv('MONGODB_ATLAS_URI'):
            return cls.ATLAS
        
        # Padrão para desenvolvimento local
        return cls.DOCKER_HOST


# Exemplo de uso
if __name__ == "__main__":
    print("Ambientes disponíveis:")
    for env, desc in MongoConfig.list_environments().items():
        print(f"  {env}: {desc}")
    
    print("\nConfiguração auto-detectada:")
    config = MongoConfig.auto_detect_environment()
    print(f"  Connection String: {config['connection_string']}")
    print(f"  Database: {config['database_name']}")
    print(f"  Descrição: {config['description']}")