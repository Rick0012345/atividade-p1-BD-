// Script de inicialização do MongoDB
// Este script é executado quando o container MongoDB é criado pela primeira vez

print('Iniciando configuração do MongoDB...');

// Conectar ao banco de dados crud_database
db = db.getSiblingDB('crud_database');

// Criar coleção de usuários com validação de schema
db.createCollection('usuarios', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['nome', 'email', 'idade'],
      properties: {
        nome: {
          bsonType: 'string',
          description: 'Nome do usuário - obrigatório'
        },
        email: {
          bsonType: 'string',
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$',
          description: 'Email válido - obrigatório'
        },
        idade: {
          bsonType: 'int',
          minimum: 0,
          maximum: 150,
          description: 'Idade entre 0 e 150 anos - obrigatório'
        },
        cidade: {
          bsonType: 'string',
          description: 'Cidade do usuário - opcional'
        },
        ativo: {
          bsonType: 'bool',
          description: 'Status ativo do usuário'
        }
      }
    }
  }
});

// Criar índice único para email
db.usuarios.createIndex({ 'email': 1 }, { unique: true });

// Criar índices para melhor performance
db.usuarios.createIndex({ 'nome': 1 });
db.usuarios.createIndex({ 'idade': 1 });
db.usuarios.createIndex({ 'cidade': 1 });
db.usuarios.createIndex({ 'ativo': 1 });

// Inserir alguns dados de exemplo
db.usuarios.insertMany([
  {
    nome: 'Admin User',
    email: 'admin@exemplo.com',
    idade: 30,
    cidade: 'São Paulo',
    ativo: true,
    data_criacao: new Date(),
    tipo: 'administrador'
  },
  {
    nome: 'Usuário Teste',
    email: 'teste@exemplo.com',
    idade: 25,
    cidade: 'Rio de Janeiro',
    ativo: true,
    data_criacao: new Date(),
    tipo: 'usuario'
  }
]);

// Criar outras coleções para os exemplos avançados
db.createCollection('produtos');
db.createCollection('posts');
db.createCollection('vendas');

// Criar índices para a coleção de produtos
db.produtos.createIndex({ 'nome': 1 });
db.produtos.createIndex({ 'categoria': 1 });
db.produtos.createIndex({ 'preco': 1 });
db.produtos.createIndex({ 'ativo': 1 });

// Criar índices para a coleção de posts
db.posts.createIndex({ 'titulo': 1 });
db.posts.createIndex({ 'autor': 1 });
db.posts.createIndex({ 'tags': 1 });
db.posts.createIndex({ 'publicado': 1 });
db.posts.createIndex({ 'data_publicacao': -1 });

// Criar índices para a coleção de vendas
db.vendas.createIndex({ 'produto': 1 });
db.vendas.createIndex({ 'vendedor': 1 });
db.vendas.createIndex({ 'data_venda': -1 });

print('Configuração do MongoDB concluída com sucesso!');
print('Coleções criadas: usuarios, produtos, posts, vendas');
print('Índices criados para melhor performance');
print('Dados de exemplo inseridos na coleção usuarios');