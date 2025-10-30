# 🦸‍♂️ Hero Lib

[![Status do
Workflow](https://img.shields.io/github/actions/workflow/status/saraivagustavo/libHero/publish.yml?branch=main&style=for-the-badge)](https://github.com/saraivagustavo/libHero/actions)
[![PyPI](https://img.shields.io/pypi/v/saraivaHeroLib?style=for-the-badge)](https://pypi.org/project/saraivaHeroLib/)
[![Versão do
Python](https://img.shields.io/pypi/pyversions/saraivaHeroLib?style=for-the-badge)](https://pypi.org/project/saraivaHeroLib/)
[![Licença](https://img.shields.io/pypi/l/saraivaHeroLib?style=for-the-badge)](https://pypi.org/project/saraivaHeroLib/)

A **Hero Lib** é uma biblioteca Python para o gerenciamento de **Heróis** e suas respectivas **Habilidades**, criada com o objetivo de demonstrar uma arquitetura limpa e desacoplada entre **camada de domínio** e **camada de API**.

Desenvolvida utilizando `SQLModel` (baseada em `Pydantic` e `SQLAlchemy`), a biblioteca define modelos de dados, DTOs e classes de serviço genéricas para CRUD, tornando o uso simples e extensível.

---

## ✨ Principais Features

- **Gerenciamento de Heróis**: CRUD completo para a entidade `Hero` (Nome, Poder, Nível, etc.).  
- **Gerenciamento de Habilidades**: CRUD para a entidade `Skill` (Nome, Dano, Tipo).  
- **Relacionamento**: Modela um relacionamento um-para-muitos (um `Hero` pode possuir múltiplas `Skill`).  
- **Arquitetura Genérica**: Baseada nos padrões `Repository` e `Service`, para máxima reutilização.  
- **Validação de Dados**: Feita automaticamente via `SQLModel` e `Pydantic`.  
- **Compatibilidade com FastAPI**: Ideal para ser integrada em APIs REST modernas.

---

## 🚀 Instalação

Você pode instalar a biblioteca diretamente do PyPI:

```bash
pip install saraivaHeroLib
```

---

## 💡 Exemplo de Uso (Quick Start)

Veja como é simples configurar um banco de dados em memória e usar os serviços para criar e listar heróis:

```python
from sqlmodel import create_engine, Session, SQLModel
from hero_lib.models import Hero
from hero_lib.dto import HeroCreate
from hero_lib.repository import Repository
from hero_lib.service import Service

# 1. Configurar o Engine (ex: SQLite em memória)
engine = create_engine("sqlite:///:memory:")

# 2. Criar as tabelas no banco de dados
SQLModel.metadata.create_all(engine)

# 3. Instanciar Repository e Service genéricos para o modelo 'Hero'
hero_repo = Repository(Hero)
hero_service = Service(hero_repo)

# 4. Criar um novo herói
print("Criando herói...")
with Session(engine) as session:
    hero_dto = HeroCreate(
        nome="Arthur",
        poder="Espada Sagrada",
        nivel=5
    )
    hero = hero_service.create(session=session, data=hero_dto)
    print(f"-> Herói Criado: {hero.nome} (ID: {hero.id})")

# 5. Listar todos os heróis
print("\nListando heróis...")
with Session(engine) as session:
    herois = hero_service.list(session=session, offset=0, limit=10)
    for h in herois:
        print(f"-> Herói Encontrado: {h.nome}")
```

**Saída Esperada:**

```
Criando herói...
-> Herói Criado: Arthur (ID: 1)

Listando heróis...
-> Herói Encontrado: Arthur
```

---

## 🏛️ Estrutura da Biblioteca

A `hero_lib` segue uma organização modular e desacoplada:

```
hero_lib/
├── models.py        # Modelos de dados (Hero, Skill)
├── dto.py           # Data Transfer Objects (Create, Read, Update)
├── repository.py    # Classe Repository genérica (CRUD)
├── service.py       # Classe Service genérica (lógica de negócios)
└── database.py      # Configuração e inicialização do banco
```

---

## ⚙️ Integração com API (FastAPI)

A biblioteca pode ser usada facilmente em uma aplicação **FastAPI**.  
Exemplo básico (`main.py`):

```python
from fastapi import FastAPI
from hero_lib.database import init_db

app = FastAPI(title="Hero API")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Bem-vindo à Hero API!"}
```

Para executar:

```bash
uvicorn main:app --reload
```

---

## 📦 Exemplo de Integração Completa (FastAPI + HeroLib)

Abaixo está um exemplo simples de API completa utilizando a biblioteca `HeroLib`:

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from hero_lib.database import get_session, init_db
from hero_lib.models import Hero
from hero_lib.dto import HeroCreate
from hero_lib.repository import Repository
from hero_lib.service import Service

app = FastAPI(title="Hero API", version="1.0.0")

@app.on_event("startup")
def startup_event():
    init_db()

repo = Repository(Hero)
service = Service(repo)

@app.post("/heroes/", response_model=Hero)
def create_hero(hero_data: HeroCreate, session: Session = Depends(get_session)):
    return service.create(session, hero_data)

@app.get("/heroes/", response_model=list[Hero])
def list_heroes(session: Session = Depends(get_session)):
    return service.list(session, 0, 10)

@app.get("/heroes/{hero_id}", response_model=Hero)
def get_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = service.get(session, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Herói não encontrado")
    return hero

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = service.delete(session, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Herói não encontrado")
    return {"message": f"Herói {hero_id} removido com sucesso"}
```

---

## 🧑‍💻 Contribuição e Desenvolvimento

Se desejar contribuir com o projeto, siga estes passos para configurar o ambiente local:

### 1️⃣ Clone o repositório:

```bash
git clone https://github.com/saraivagustavo/HeroLib.git
cd HeroLib/hero_lib
```

### 2️⃣ Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # (ou .\venv\Scripts\activate no Windows)
```

### 3️⃣ Instale as dependências (incluindo as de desenvolvimento):

```bash
pip install -e .[dev]
```

> O `-e .` instala o pacote em modo editável.

### 4️⃣ Rode os testes:

```bash
pytest
```

---

## 📝 Licença

Este projeto é distribuído sob a licença **MIT**.  
Consulte o arquivo `LICENSE` para mais detalhes.
