#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB CRUD Operations
Este script demonstra as operações básicas de CRUD (Create, Read, Update, Delete)
no MongoDB usando a biblioteca pymongo.

Autor: Atividade P1 BD
Data: 2024
"""

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from datetime import datetime
import json
from config import MongoConfig


class MongoDBCRUD:
    """Classe para realizar operações CRUD no MongoDB"""
    
    def __init__(self, connection_string=None, database_name=None, environment=None):
        """
        Inicializa a conexão com o MongoDB
        
        Args:
            connection_string (str, optional): String de conexão do MongoDB
            database_name (str, optional): Nome do banco de dados
            environment (str, optional): Ambiente específico ('local', 'docker_host', 'docker_container', 'atlas')
        """
        # Auto-detectar configuração se não fornecida
        if connection_string is None or database_name is None:
            if environment:
                config = MongoConfig.get_config(environment)
            else:
                config = MongoConfig.auto_detect_environment()
            
            self.connection_string = connection_string or config['connection_string']
            self.database_name = database_name or config['database_name']
            self.environment_description = config['description']
        else:
            self.connection_string = connection_string
            self.database_name = database_name
            self.environment_description = "Configuração personalizada"
        self.client = None
        self.db = None
        self.collection = None
        
    def connect(self):
        """Estabelece conexão com o MongoDB"""
        try:
            print(f"🔌 Conectando ao MongoDB...")
            print(f"   Ambiente: {self.environment_description}")
            print(f"   Database: {self.database_name}")
            
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            # Testa a conexão
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            self.collection = self.db['usuarios']
            print("✅ Conexão com MongoDB estabelecida com sucesso!")
            return True
        except ConnectionFailure as e:
            print(f"❌ Erro ao conectar com MongoDB: {e}")
            print(f"   Verifique se o MongoDB está rodando e acessível")
            return False
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return False
    
    def disconnect(self):
        """Fecha a conexão com o MongoDB"""
        if self.client:
            self.client.close()
            print("🔌 Conexão com MongoDB fechada.")
    
    # CREATE - Inserir documentos
    def create_user(self, nome, email, idade, cidade=None):
        """
        Cria um novo usuário no banco de dados
        
        Args:
            nome (str): Nome do usuário
            email (str): Email do usuário
            idade (int): Idade do usuário
            cidade (str, optional): Cidade do usuário
            
        Returns:
            str: ID do documento inserido ou None se houver erro
        """
        try:
            documento = {
                "nome": nome,
                "email": email,
                "idade": idade,
                "cidade": cidade,
                "data_criacao": datetime.now(),
                "ativo": True
            }
            
            resultado = self.collection.insert_one(documento)
            print(f"✅ Usuário criado com sucesso! ID: {resultado.inserted_id}")
            return str(resultado.inserted_id)
            
        except DuplicateKeyError:
            print("❌ Erro: Email já existe no banco de dados")
            return None
        except Exception as e:
            print(f"❌ Erro ao criar usuário: {e}")
            return None
    
    def create_multiple_users(self, usuarios):
        """
        Cria múltiplos usuários de uma vez
        
        Args:
            usuarios (list): Lista de dicionários com dados dos usuários
            
        Returns:
            list: Lista de IDs dos documentos inseridos
        """
        try:
            for usuario in usuarios:
                usuario['data_criacao'] = datetime.now()
                usuario['ativo'] = True
                
            resultado = self.collection.insert_many(usuarios)
            print(f"✅ {len(resultado.inserted_ids)} usuários criados com sucesso!")
            return [str(id) for id in resultado.inserted_ids]
            
        except Exception as e:
            print(f"❌ Erro ao criar usuários: {e}")
            return []
    
    # READ - Ler documentos
    def read_all_users(self):
        """
        Lê todos os usuários do banco de dados
        
        Returns:
            list: Lista de todos os usuários
        """
        try:
            usuarios = list(self.collection.find())
            print(f"📖 Encontrados {len(usuarios)} usuários")
            return usuarios
        except Exception as e:
            print(f"❌ Erro ao ler usuários: {e}")
            return []
    
    def read_user_by_id(self, user_id):
        """
        Lê um usuário específico pelo ID
        
        Args:
            user_id (str): ID do usuário
            
        Returns:
            dict: Dados do usuário ou None se não encontrado
        """
        try:
            from bson import ObjectId
            usuario = self.collection.find_one({"_id": ObjectId(user_id)})
            if usuario:
                print(f"📖 Usuário encontrado: {usuario['nome']}")
            else:
                print("❌ Usuário não encontrado")
            return usuario
        except Exception as e:
            print(f"❌ Erro ao buscar usuário: {e}")
            return None
    
    def read_users_by_filter(self, filtro):
        """
        Lê usuários com base em um filtro
        
        Args:
            filtro (dict): Filtro para busca
            
        Returns:
            list: Lista de usuários que atendem ao filtro
        """
        try:
            usuarios = list(self.collection.find(filtro))
            print(f"📖 Encontrados {len(usuarios)} usuários com o filtro aplicado")
            return usuarios
        except Exception as e:
            print(f"❌ Erro ao buscar usuários: {e}")
            return []
    
    # UPDATE - Atualizar documentos
    def update_user(self, user_id, novos_dados):
        """
        Atualiza um usuário específico
        
        Args:
            user_id (str): ID do usuário
            novos_dados (dict): Novos dados para atualização
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        try:
            from bson import ObjectId
            novos_dados['data_atualizacao'] = datetime.now()
            
            resultado = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": novos_dados}
            )
            
            if resultado.modified_count > 0:
                print(f"✅ Usuário atualizado com sucesso!")
                return True
            else:
                print("❌ Nenhum usuário foi atualizado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao atualizar usuário: {e}")
            return False
    
    def update_multiple_users(self, filtro, novos_dados):
        """
        Atualiza múltiplos usuários com base em um filtro
        
        Args:
            filtro (dict): Filtro para seleção dos usuários
            novos_dados (dict): Novos dados para atualização
            
        Returns:
            int: Número de documentos atualizados
        """
        try:
            novos_dados['data_atualizacao'] = datetime.now()
            
            resultado = self.collection.update_many(
                filtro,
                {"$set": novos_dados}
            )
            
            print(f"✅ {resultado.modified_count} usuários atualizados")
            return resultado.modified_count
            
        except Exception as e:
            print(f"❌ Erro ao atualizar usuários: {e}")
            return 0
    
    # DELETE - Deletar documentos
    def delete_user(self, user_id):
        """
        Deleta um usuário específico
        
        Args:
            user_id (str): ID do usuário
            
        Returns:
            bool: True se deletado com sucesso, False caso contrário
        """
        try:
            from bson import ObjectId
            resultado = self.collection.delete_one({"_id": ObjectId(user_id)})
            
            if resultado.deleted_count > 0:
                print(f"✅ Usuário deletado com sucesso!")
                return True
            else:
                print("❌ Nenhum usuário foi deletado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao deletar usuário: {e}")
            return False
    
    def delete_users_by_filter(self, filtro):
        """
        Deleta múltiplos usuários com base em um filtro
        
        Args:
            filtro (dict): Filtro para seleção dos usuários
            
        Returns:
            int: Número de documentos deletados
        """
        try:
            resultado = self.collection.delete_many(filtro)
            print(f"✅ {resultado.deleted_count} usuários deletados")
            return resultado.deleted_count
            
        except Exception as e:
            print(f"❌ Erro ao deletar usuários: {e}")
            return 0
    
    def delete_all_users(self):
        """
        Deleta todos os usuários (usar com cuidado!)
        
        Returns:
            int: Número de documentos deletados
        """
        try:
            resultado = self.collection.delete_many({})
            print(f"✅ Todos os {resultado.deleted_count} usuários foram deletados")
            return resultado.deleted_count
            
        except Exception as e:
            print(f"❌ Erro ao deletar todos os usuários: {e}")
            return 0
    
    # Métodos auxiliares
    def count_users(self):
        """
        Conta o número total de usuários
        
        Returns:
            int: Número de usuários
        """
        try:
            count = self.collection.count_documents({})
            print(f"📊 Total de usuários: {count}")
            return count
        except Exception as e:
            print(f"❌ Erro ao contar usuários: {e}")
            return 0
    
    def print_users(self, usuarios):
        """
        Imprime usuários de forma formatada
        
        Args:
            usuarios (list): Lista de usuários para imprimir
        """
        if not usuarios:
            print("📝 Nenhum usuário para exibir")
            return
            
        print("\n" + "="*80)
        print("📋 LISTA DE USUÁRIOS")
        print("="*80)
        
        for i, usuario in enumerate(usuarios, 1):
            print(f"\n{i}. ID: {usuario.get('_id')}")
            print(f"   Nome: {usuario.get('nome')}")
            print(f"   Email: {usuario.get('email')}")
            print(f"   Idade: {usuario.get('idade')}")
            print(f"   Cidade: {usuario.get('cidade', 'Não informado')}")
            print(f"   Ativo: {usuario.get('ativo', True)}")
            print(f"   Criado em: {usuario.get('data_criacao', 'N/A')}")
            if 'data_atualizacao' in usuario:
                print(f"   Atualizado em: {usuario.get('data_atualizacao')}")
        
        print("\n" + "="*80)


def demonstrar_crud():
    """
    Função para demonstrar todas as operações CRUD
    """
    print("🚀 Iniciando demonstração das operações CRUD no MongoDB")
    print("="*60)
    
    # Inicializar conexão
    crud = MongoDBCRUD()
    
    if not crud.connect():
        print("❌ Não foi possível conectar ao MongoDB. Verifique se o serviço está rodando.")
        return
    
    try:
        # Limpar dados anteriores para demonstração
        print("\n🧹 Limpando dados anteriores...")
        crud.delete_all_users()
        
        # CREATE - Demonstração
        print("\n" + "="*60)
        print("📝 DEMONSTRAÇÃO CREATE (Criar)")
        print("="*60)
        
        # Criar usuário individual
        user_id1 = crud.create_user("João Silva", "joao@email.com", 30, "São Paulo")
        user_id2 = crud.create_user("Maria Santos", "maria@email.com", 25, "Rio de Janeiro")
        user_id3 = crud.create_user("Pedro Oliveira", "pedro@email.com", 35)
        
        # Criar múltiplos usuários
        usuarios_batch = [
            {"nome": "Ana Costa", "email": "ana@email.com", "idade": 28, "cidade": "Belo Horizonte"},
            {"nome": "Carlos Lima", "email": "carlos@email.com", "idade": 32, "cidade": "Salvador"},
            {"nome": "Lucia Ferreira", "email": "lucia@email.com", "idade": 29, "cidade": "Fortaleza"}
        ]
        crud.create_multiple_users(usuarios_batch)
        
        # READ - Demonstração
        print("\n" + "="*60)
        print("📖 DEMONSTRAÇÃO READ (Ler)")
        print("="*60)
        
        # Ler todos os usuários
        print("\n📋 Todos os usuários:")
        todos_usuarios = crud.read_all_users()
        crud.print_users(todos_usuarios)
        
        # Ler usuário por ID
        if user_id1:
            print(f"\n🔍 Buscando usuário por ID ({user_id1}):")
            usuario = crud.read_user_by_id(user_id1)
            if usuario:
                crud.print_users([usuario])
        
        # Ler usuários por filtro
        print("\n🔍 Usuários com idade maior que 30:")
        usuarios_filtrados = crud.read_users_by_filter({"idade": {"$gt": 30}})
        crud.print_users(usuarios_filtrados)
        
        print("\n🔍 Usuários de São Paulo:")
        usuarios_sp = crud.read_users_by_filter({"cidade": "São Paulo"})
        crud.print_users(usuarios_sp)
        
        # UPDATE - Demonstração
        print("\n" + "="*60)
        print("✏️ DEMONSTRAÇÃO UPDATE (Atualizar)")
        print("="*60)
        
        # Atualizar usuário individual
        if user_id1:
            print(f"\n🔄 Atualizando usuário {user_id1}:")
            crud.update_user(user_id1, {
                "idade": 31,
                "cidade": "Brasília",
                "telefone": "(11) 99999-9999"
            })
            
            # Mostrar usuário atualizado
            usuario_atualizado = crud.read_user_by_id(user_id1)
            crud.print_users([usuario_atualizado])
        
        # Atualizar múltiplos usuários
        print("\n🔄 Atualizando todos os usuários com idade menor que 30:")
        crud.update_multiple_users(
            {"idade": {"$lt": 30}},
            {"status": "jovem", "desconto": 10}
        )
        
        # Mostrar usuários atualizados
        usuarios_jovens = crud.read_users_by_filter({"status": "jovem"})
        crud.print_users(usuarios_jovens)
        
        # DELETE - Demonstração
        print("\n" + "="*60)
        print("🗑️ DEMONSTRAÇÃO DELETE (Deletar)")
        print("="*60)
        
        # Contar usuários antes da deleção
        crud.count_users()
        
        # Deletar usuário por ID
        if user_id3:
            print(f"\n🗑️ Deletando usuário {user_id3}:")
            crud.delete_user(user_id3)
        
        # Deletar usuários por filtro
        print("\n🗑️ Deletando usuários com idade maior que 32:")
        crud.delete_users_by_filter({"idade": {"$gt": 32}})
        
        # Mostrar usuários restantes
        print("\n📋 Usuários restantes:")
        usuarios_restantes = crud.read_all_users()
        crud.print_users(usuarios_restantes)
        
        # Contar usuários após deleções
        crud.count_users()
        
        print("\n" + "="*60)
        print("✅ Demonstração CRUD concluída com sucesso!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Erro durante a demonstração: {e}")
    
    finally:
        # Fechar conexão
        crud.disconnect()


if __name__ == "__main__":
    demonstrar_crud()