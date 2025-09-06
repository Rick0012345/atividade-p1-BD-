# MongoDB CRUD Operations com Python

Este projeto demonstra as operações básicas de CRUD (Create, Read, Update, Delete) no MongoDB usando Python e a biblioteca pymongo. O projeto está configurado para rodar com Docker para facilitar o desenvolvimento e deployment.

## 📋 Funcionalidades

- ✅ **CREATE**: Inserir documentos individuais e em lote
- ✅ **READ**: Buscar documentos por ID, filtros e listar todos
- ✅ **UPDATE**: Atualizar documentos individuais e múltiplos
- ✅ **DELETE**: Remover documentos por ID, filtros ou todos
- 🔍 **Operações Avançadas**: Agregações, índices e validações
- 🐳 **Docker**: Ambiente containerizado completo
- 🌐 **Multi-ambiente**: Suporte para local, Docker e MongoDB Atlas

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**
- **PyMongo 4.6.1** - Driver oficial do MongoDB para Python
- **MongoDB** - Banco de dados NoSQL
- **Docker & Docker Compose** - Containerização
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## 📁 Estrutura do Projeto

```
atividade-p1-BD/
├── mongodb_crud.py          # Classe principal com operações CRUD
├── exemplo_avancado.py      # Exemplos avançados (e-commerce, blog, agregações)
├── config.py                # Configurações de conexão para diferentes ambientes
├── requirements.txt         # Dependências Python
├── docker-compose.yml       # Configuração Docker Compose
├── Dockerfile              # Imagem Docker da aplicação
├── init-mongo.js           # Script de inicialização do MongoDB
├── .env.example            # Exemplo de variáveis de ambiente
├── .dockerignore           # Arquivos ignorados pelo Docker
└── README.md               # Este arquivo
```

## 🚀 Como Executar

### Opção 1: Com Docker Compose (Recomendado)

1. **Clone o repositório e navegue até a pasta:**
   ```bash
   cd atividade-p1-BD
   ```

2. **Inicie o ambiente completo:**
   ```bash
   docker-compose up -d
   ```

3. **Execute o exemplo básico:**
   ```bash
   docker-compose exec python_app python mongodb_crud.py
   ```

4. **Execute exemplos avançados:**
   ```bash
   docker-compose exec python_app python exemplo_avancado.py
   ```

### Opção 2: Docker Manual

1. **Inicie o MongoDB:**
   ```bash
   docker run -d --name mongodb \
     -p 27017:27017 \
     -e MONGO_INITDB_ROOT_USERNAME=admin \
     -e MONGO_INITDB_ROOT_PASSWORD=password \
     mongo:latest
   ```

2. **Execute a aplicação Python:**
   ```bash
   # Instalar dependências
   pip install -r requirements.txt
   
   # Executar exemplo básico
   python mongodb_crud.py
   
   # Executar exemplos avançados
   python exemplo_avancado.py
   ```

### Opção 3: MongoDB Atlas (Nuvem)

1. **Configure as variáveis de ambiente:**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas credenciais do MongoDB Atlas
   ```

2. **Execute a aplicação:**
   ```bash
   python mongodb_crud.py
   ```

## 🔧 Configuração

### Variáveis de Ambiente

O projeto suporta diferentes ambientes através de variáveis de ambiente:

```bash
# MongoDB Atlas (Nuvem)
MONGODB_ATLAS_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=crud_database

# Docker (Container para Container)
MONGODB_URI=mongodb://admin:password@mongodb:27017/
```

### Ambientes Suportados

- **local**: MongoDB local sem autenticação
- **docker_host**: MongoDB em container, acesso do host
- **docker_container**: MongoDB em container, acesso entre containers
- **atlas**: MongoDB Atlas (nuvem)

## 📚 Exemplos de Uso

### Exemplo Básico

```python
from mongodb_crud import MongoDBCRUD

# Inicializar (auto-detecta o ambiente)
crude = MongoDBCRUD()
crude.connect()

# CREATE - Criar usuário
user_id = crude.create_user("João Silva", "joao@email.com", 30, "São Paulo")

# READ - Ler usuários
usuarios = crude.read_all_users()
crude.print_users(usuarios)

# UPDATE - Atualizar usuário
crude.update_user(user_id, {"idade": 31, "cidade": "Rio de Janeiro"})

# DELETE - Deletar usuário
crude.delete_user(user_id)

crude.disconnect()
```

### Exemplo com Configuração Específica

```python
from mongodb_crud import MongoDBCRUD
from config import MongoConfig

# Usar configuração específica
config = MongoConfig.get_config('docker_host')
crude = MongoDBCRUD(
    connection_string=config['connection_string'],
    database_name=config['database_name']
)
```

## 🎯 Funcionalidades Implementadas

### Operações CRUD Básicas

- **CREATE**:
  - `create_user()` - Criar usuário individual
  - `create_multiple_users()` - Criar múltiplos usuários

- **READ**:
  - `read_all_users()` - Listar todos os usuários
  - `read_user_by_id()` - Buscar por ID
  - `read_users_by_filter()` - Buscar com filtros

- **UPDATE**:
  - `update_user()` - Atualizar usuário individual
  - `update_multiple_users()` - Atualizar múltiplos usuários

- **DELETE**:
  - `delete_user()` - Deletar usuário individual
  - `delete_users_by_filter()` - Deletar com filtros
  - `delete_all_users()` - Deletar todos (cuidado!)

### Funcionalidades Avançadas

- **Validação de Schema** - Validação automática de dados
- **Índices** - Índices para melhor performance
- **Agregações** - Operações de agregação complexas
- **Tratamento de Erros** - Tratamento robusto de exceções
- **Logging** - Logs detalhados das operações

## 📊 Exemplos Avançados

O arquivo `exemplo_avancado.py` contém três cenários completos:

1. **Sistema de E-commerce**
   - Gestão de produtos
   - Controle de estoque
   - Sistema de promoções

2. **Sistema de Blog**
   - Gestão de posts
   - Sistema de comentários
   - Estatísticas de visualização

3. **Operações de Agregação**
   - Relatórios de vendas
   - Análises por período
   - Métricas de performance

## 🐳 Docker

### Comandos Úteis

```bash
# Iniciar ambiente
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar ambiente
docker-compose down

# Rebuild da aplicação
docker-compose up -d --build

# Shell interativo Python
docker-compose exec python_app python -i

# Shell MongoDB
docker-compose exec mongodb mongosh -u admin -p password --authenticationDatabase admin
```

### Volumes

- **mongodb_data**: Persistência dos dados do MongoDB
- **./**: Código da aplicação montado no container

## 🔍 Monitoramento

### Verificar Status dos Containers

```bash
docker-compose ps
```

### Acessar Logs

```bash
# Logs da aplicação Python
docker-compose logs python_app

# Logs do MongoDB
docker-compose logs mongodb
```

### Conectar ao MongoDB

```bash
# Via container
docker-compose exec mongodb mongosh -u admin -p password --authenticationDatabase admin

# Via host (se porta 27017 estiver exposta)
mongosh mongodb://admin:password@localhost:27017/
```

## 🛡️ Segurança

- **Autenticação**: MongoDB configurado com usuário e senha
- **Rede Isolada**: Containers em rede privada
- **Validação de Dados**: Schema validation no MongoDB
- **Tratamento de Erros**: Prevenção de vazamento de informações

## 📝 Logs e Debugging

O projeto inclui logging detalhado:

- ✅ Conexões bem-sucedidas
- ❌ Erros de conexão e operação
- 📊 Estatísticas de operações
- 🔍 Informações de debug

## 🤝 Contribuição

Este é um projeto acadêmico individual para demonstração de operações CRUD no MongoDB.

## 📄 Licença

Projeto desenvolvido para fins educacionais - Atividade P1 BD.

---

**Desenvolvido por:** [Patrick Oliveira]  
**Disciplina:** Banco de Dados  
**Data:** -05-09-2025