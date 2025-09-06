#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo Avançado de Operações CRUD no MongoDB
Este arquivo demonstra cenários mais complexos de uso do MongoDB com pymongo.
"""

from mongodb_crud import MongoDBCRUD
from config import MongoConfig
from datetime import datetime, timedelta
import random


def exemplo_ecommerce():
    """
    Exemplo simulando um sistema de e-commerce simples
    """
    print("🛒 Exemplo: Sistema de E-commerce")
    print("="*50)
    
    # Conectar usando configuração do Docker
    config = MongoConfig.get_config('docker')
    crud = MongoDBCRUD(
        connection_string=config['connection_string'],
        database_name='ecommerce_db'
    )
    
    if not crud.connect():
        print("❌ Erro na conexão")
        return
    
    try:
        # Usar coleção de produtos
        crud.collection = crud.db['produtos']
        
        # Limpar dados anteriores
        crud.collection.delete_many({})
        
        # Criar produtos
        produtos = [
            {
                "nome": "Smartphone Samsung Galaxy",
                "categoria": "Eletrônicos",
                "preco": 1299.99,
                "estoque": 50,
                "descricao": "Smartphone com 128GB de armazenamento",
                "ativo": True,
                "data_criacao": datetime.now()
            },
            {
                "nome": "Notebook Dell Inspiron",
                "categoria": "Informática",
                "preco": 2499.99,
                "estoque": 25,
                "descricao": "Notebook com Intel i5 e 8GB RAM",
                "ativo": True,
                "data_criacao": datetime.now()
            },
            {
                "nome": "Fone de Ouvido Bluetooth",
                "categoria": "Acessórios",
                "preco": 199.99,
                "estoque": 100,
                "descricao": "Fone sem fio com cancelamento de ruído",
                "ativo": True,
                "data_criacao": datetime.now()
            },
            {
                "nome": "Camiseta Básica",
                "categoria": "Roupas",
                "preco": 29.99,
                "estoque": 200,
                "descricao": "Camiseta 100% algodão",
                "ativo": True,
                "data_criacao": datetime.now()
            }
        ]
        
        resultado = crud.collection.insert_many(produtos)
        print(f"✅ {len(resultado.inserted_ids)} produtos criados")
        
        # Buscar produtos por categoria
        print("\n📱 Produtos da categoria 'Eletrônicos':")
        eletronicos = list(crud.collection.find({"categoria": "Eletrônicos"}))
        for produto in eletronicos:
            print(f"  - {produto['nome']}: R$ {produto['preco']}")
        
        # Buscar produtos com preço entre R$ 100 e R$ 500
        print("\n💰 Produtos entre R$ 100 e R$ 500:")
        produtos_faixa = list(crud.collection.find({
            "preco": {"$gte": 100, "$lte": 500}
        }))
        for produto in produtos_faixa:
            print(f"  - {produto['nome']}: R$ {produto['preco']}")
        
        # Atualizar estoque (simular venda)
        print("\n📦 Simulando venda - atualizando estoque:")
        crud.collection.update_one(
            {"nome": "Smartphone Samsung Galaxy"},
            {"$inc": {"estoque": -5}, "$set": {"ultima_venda": datetime.now()}}
        )
        print("  - 5 smartphones vendidos")
        
        # Aplicar desconto em produtos com estoque alto
        print("\n🏷️ Aplicando desconto em produtos com estoque > 50:")
        resultado = crud.collection.update_many(
            {"estoque": {"$gt": 50}},
            {"$set": {"desconto": 10, "promocao": True}}
        )
        print(f"  - {resultado.modified_count} produtos em promoção")
        
        # Buscar produtos em promoção
        print("\n🎉 Produtos em promoção:")
        promocoes = list(crud.collection.find({"promocao": True}))
        for produto in promocoes:
            preco_original = produto['preco']
            preco_desconto = preco_original * (1 - produto['desconto'] / 100)
            print(f"  - {produto['nome']}: R$ {preco_original:.2f} → R$ {preco_desconto:.2f}")
        
        # Relatório de estoque baixo
        print("\n⚠️ Produtos com estoque baixo (< 30):")
        estoque_baixo = list(crud.collection.find({"estoque": {"$lt": 30}}))
        for produto in estoque_baixo:
            print(f"  - {produto['nome']}: {produto['estoque']} unidades")
        
    finally:
        crud.disconnect()


def exemplo_blog():
    """
    Exemplo simulando um sistema de blog
    """
    print("\n📝 Exemplo: Sistema de Blog")
    print("="*50)
    
    config = MongoConfig.get_config('docker')
    crud = MongoDBCRUD(
        connection_string=config['connection_string'],
        database_name='blog_db'
    )
    
    if not crud.connect():
        print("❌ Erro na conexão")
        return
    
    try:
        # Usar coleção de posts
        crud.collection = crud.db['posts']
        crud.collection.delete_many({})
        
        # Criar posts
        posts = [
            {
                "titulo": "Introdução ao MongoDB",
                "autor": "João Silva",
                "conteudo": "MongoDB é um banco de dados NoSQL...",
                "tags": ["mongodb", "nosql", "database"],
                "visualizacoes": 0,
                "likes": 0,
                "comentarios": [],
                "publicado": True,
                "data_publicacao": datetime.now() - timedelta(days=5)
            },
            {
                "titulo": "Python e PyMongo",
                "autor": "Maria Santos",
                "conteudo": "PyMongo é a biblioteca oficial...",
                "tags": ["python", "pymongo", "mongodb"],
                "visualizacoes": 0,
                "likes": 0,
                "comentarios": [],
                "publicado": True,
                "data_publicacao": datetime.now() - timedelta(days=3)
            },
            {
                "titulo": "CRUD Operations",
                "autor": "Pedro Oliveira",
                "conteudo": "CRUD significa Create, Read, Update, Delete...",
                "tags": ["crud", "database", "operations"],
                "visualizacoes": 0,
                "likes": 0,
                "comentarios": [],
                "publicado": False,
                "data_criacao": datetime.now() - timedelta(days=1)
            }
        ]
        
        resultado = crud.collection.insert_many(posts)
        print(f"✅ {len(resultado.inserted_ids)} posts criados")
        
        # Simular visualizações
        print("\n👀 Simulando visualizações:")
        for _ in range(10):
            post_aleatorio = crud.collection.find_one({"publicado": True})
            if post_aleatorio:
                crud.collection.update_one(
                    {"_id": post_aleatorio["_id"]},
                    {"$inc": {"visualizacoes": random.randint(1, 5)}}
                )
        
        # Adicionar comentários
        print("\n💬 Adicionando comentários:")
        post_mongodb = crud.collection.find_one({"titulo": "Introdução ao MongoDB"})
        if post_mongodb:
            comentarios = [
                {
                    "autor": "Ana Costa",
                    "texto": "Excelente artigo!",
                    "data": datetime.now() - timedelta(hours=2)
                },
                {
                    "autor": "Carlos Lima",
                    "texto": "Muito útil, obrigado!",
                    "data": datetime.now() - timedelta(hours=1)
                }
            ]
            
            crud.collection.update_one(
                {"_id": post_mongodb["_id"]},
                {"$push": {"comentarios": {"$each": comentarios}}}
            )
            print(f"  - {len(comentarios)} comentários adicionados")
        
        # Buscar posts por tag
        print("\n🏷️ Posts com tag 'mongodb':")
        posts_mongodb = list(crud.collection.find({"tags": "mongodb"}))
        for post in posts_mongodb:
            print(f"  - {post['titulo']} por {post['autor']}")
        
        # Posts mais visualizados
        print("\n📊 Posts mais visualizados:")
        posts_populares = list(crud.collection.find(
            {"publicado": True}
        ).sort("visualizacoes", -1).limit(3))
        
        for i, post in enumerate(posts_populares, 1):
            print(f"  {i}. {post['titulo']}: {post['visualizacoes']} visualizações")
        
        # Publicar post em rascunho
        print("\n📤 Publicando post em rascunho:")
        crud.collection.update_one(
            {"publicado": False},
            {
                "$set": {
                    "publicado": True,
                    "data_publicacao": datetime.now()
                }
            }
        )
        print("  - Post publicado com sucesso")
        
        # Estatísticas do blog
        print("\n📈 Estatísticas do blog:")
        total_posts = crud.collection.count_documents({})
        posts_publicados = crud.collection.count_documents({"publicado": True})
        total_visualizacoes = list(crud.collection.aggregate([
            {"$group": {"_id": None, "total": {"$sum": "$visualizacoes"}}}
        ]))
        
        print(f"  - Total de posts: {total_posts}")
        print(f"  - Posts publicados: {posts_publicados}")
        if total_visualizacoes:
            print(f"  - Total de visualizações: {total_visualizacoes[0]['total']}")
        
    finally:
        crud.disconnect()


def exemplo_agregacao():
    """
    Exemplo demonstrando operações de agregação
    """
    print("\n📊 Exemplo: Operações de Agregação")
    print("="*50)
    
    config = MongoConfig.get_config('docker')
    crud = MongoDBCRUD(
        connection_string=config['connection_string'],
        database_name='vendas_db'
    )
    
    if not crud.connect():
        print("❌ Erro na conexão")
        return
    
    try:
        # Usar coleção de vendas
        crud.collection = crud.db['vendas']
        crud.collection.delete_many({})
        
        # Gerar dados de vendas
        vendas = []
        produtos = ["Notebook", "Mouse", "Teclado", "Monitor", "Smartphone"]
        vendedores = ["Ana", "Bruno", "Carlos", "Diana", "Eduardo"]
        
        for i in range(50):
            venda = {
                "produto": random.choice(produtos),
                "vendedor": random.choice(vendedores),
                "quantidade": random.randint(1, 10),
                "preco_unitario": round(random.uniform(50, 2000), 2),
                "data_venda": datetime.now() - timedelta(days=random.randint(0, 30))
            }
            venda["total"] = venda["quantidade"] * venda["preco_unitario"]
            vendas.append(venda)
        
        crud.collection.insert_many(vendas)
        print(f"✅ {len(vendas)} vendas geradas")
        
        # Agregação: Vendas por produto
        print("\n📦 Vendas por produto:")
        pipeline_produto = [
            {
                "$group": {
                    "_id": "$produto",
                    "total_vendas": {"$sum": "$total"},
                    "quantidade_vendida": {"$sum": "$quantidade"}
                }
            },
            {"$sort": {"total_vendas": -1}}
        ]
        
        resultado = list(crud.collection.aggregate(pipeline_produto))
        for item in resultado:
            print(f"  - {item['_id']}: R$ {item['total_vendas']:.2f} ({item['quantidade_vendida']} unidades)")
        
        # Agregação: Vendas por vendedor
        print("\n👤 Vendas por vendedor:")
        pipeline_vendedor = [
            {
                "$group": {
                    "_id": "$vendedor",
                    "total_vendas": {"$sum": "$total"},
                    "numero_vendas": {"$sum": 1}
                }
            },
            {"$sort": {"total_vendas": -1}}
        ]
        
        resultado = list(crud.collection.aggregate(pipeline_vendedor))
        for item in resultado:
            media = item['total_vendas'] / item['numero_vendas']
            print(f"  - {item['_id']}: R$ {item['total_vendas']:.2f} ({item['numero_vendas']} vendas, média: R$ {media:.2f})")
        
        # Agregação: Vendas por período
        print("\n📅 Vendas dos últimos 7 dias:")
        data_limite = datetime.now() - timedelta(days=7)
        pipeline_periodo = [
            {"$match": {"data_venda": {"$gte": data_limite}}},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data_venda"
                        }
                    },
                    "total_dia": {"$sum": "$total"},
                    "vendas_dia": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        resultado = list(crud.collection.aggregate(pipeline_periodo))
        for item in resultado:
            print(f"  - {item['_id']}: R$ {item['total_dia']:.2f} ({item['vendas_dia']} vendas)")
        
    finally:
        crud.disconnect()


def menu_exemplos():
    """
    Menu interativo para escolher qual exemplo executar
    """
    print("🎯 Exemplos Avançados de MongoDB CRUD")
    print("="*40)
    print("1. Sistema de E-commerce")
    print("2. Sistema de Blog")
    print("3. Operações de Agregação")
    print("4. Executar todos os exemplos")
    print("0. Sair")
    
    while True:
        try:
            opcao = input("\nEscolha uma opção (0-4): ").strip()
            
            if opcao == "0":
                print("👋 Até logo!")
                break
            elif opcao == "1":
                exemplo_ecommerce()
            elif opcao == "2":
                exemplo_blog()
            elif opcao == "3":
                exemplo_agregacao()
            elif opcao == "4":
                exemplo_ecommerce()
                exemplo_blog()
                exemplo_agregacao()
            else:
                print("❌ Opção inválida. Tente novamente.")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    menu_exemplos()