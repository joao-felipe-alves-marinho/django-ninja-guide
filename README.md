## Descrição do Repositório

Este repositório contém um exemplo completo de API REST construída com **Django Ninja**, demonstrando como criar um CRUD (Create, Read, Update, Delete) para um recurso “Pet”. A solução inclui:

* Configuração de ambiente Python/Django e Docker
* Definição de modelos, schemas e endpoints usando Django Ninja
* Documentação automática OpenAPI/Swagger
* Estrutura de pastas organizada para facilitar extensão e manutenção

Ele serve como ponto de partida para quem quer aprender a criar APIs tipadas, validadas e documentadas de forma rápida e integrada ao ecossistema Django.

## Sumário

* [Visão Geral](#visão-geral)
* [Instalação](#instalação)
* [Uso](#uso)
* [Endpoints](#endpoints)
* [Estrutura de Pastas](#estrutura-de-pastas)
* [Docker](#docker)
* [Guia Completo](#guia-completo)
* [Licença](#licença)

---

## Visão Geral

Este projeto demonstra:

1. Como configurar um ambiente virtual e instalar dependências (**Django**, **Django Ninja**)
2. Definição de um modelo `Pet` em Django e schemas Pydantic para validação automática
3. Criação de endpoints RESTful (`GET`, `POST`, `PATCH`, `DELETE`) com Django Ninja
4. Geração de documentação interativa em Swagger/OpenAPI (acessível em `/api/v1/docs`)
5. Containerização com Docker para facilitar deploy em múltiplos ambientes

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/meu-projeto-django-ninja.git
cd meu-projeto-django-ninja
```

### 2. Configurar ambiente virtual

```bash
python -m venv venv  
source venv/bin/activate   # Linux / macOS  
venv\Scripts\activate      # Windows  
```

### 3. Instalar dependências

```bash
pip install --upgrade pip  
pip install -r requirements.txt  
```

---

## Uso

1. Aplicar migrações no banco de dados SQLite:

   ```bash
   python manage.py makemigrations  
   python manage.py migrate  
   ```

2. Executar o servidor de desenvolvimento:

   ```bash
   python manage.py runserver  
   ```

3. Acessar a documentação interativa:

   ```
   http://127.0.0.1:8000/api/v1/docs
   ```

---

## Endpoints

| Método | Rota         | Descrição              | Payload (exemplo)                     | Resposta    |
| ------ | ------------ | ---------------------- | ------------------------------------- | ----------- |
| GET    | `/pets`      | Lista todos os pets    | —                                     | `[{…}]`     |
| GET    | `/pets/{id}` | Recupera 1 pet por ID  | —                                     | `{ id, … }` |
| POST   | `/pets`      | Cria um novo pet       | `{ "name": "Rex", "species": "dog" }` | `{ id, … }` |
| PATCH  | `/pets/{id}` | Atualiza campos do pet | `{ "name": "Max" }`                   | `{ id, … }` |
| DELETE | `/pets/{id}` | Remove um pet          | —                                     | HTTP 204    |

---

## Estrutura de Pastas

```
pasta_do_projeto/
├── manage.py
├── meu_projeto/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── minha_api/
│   ├── __init__.py
│   ├── admin.py
│   ├── api.py          # Endpoints com Django Ninja
│   ├── models.py       # Modelo Pet
│   ├── schemas.py      # Schemas do Pet
│   ├── tests.py
│   ├── views.py        # (Opcional)
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py  # (Gerado após makemigrations)
├── db.sqlite3
├── requirements.txt
├── LICENSE
├── .gitignore
├── .dockerignore
└── Dockerfile
```

---

## Docker

1. Build da imagem:

   ```bash
   docker build -t django-ninja-api .
   ```

2. Rodar container:

   ```bash
   docker run -p 8000:8000 django-ninja-api
   ```

Agora a API estará disponível em `http://localhost:8000/api/v1/docs`.

---

## Guia Completo

### Introdução

Neste guia você terá uma visão prática de como criar um CRUD (Create, Read, Update, Delete) em sua API REST construída com Django Ninja.

### Contextualização

#### API REST

**O que é?**
Uma API REST é uma forma de comunicação entre aplicações pela web, usando métodos HTTP como `GET`, `POST`, `PATCH` e `DELETE` para enviar e receber dados de um servidor.

**Por que usar?**
Uma API REST permite que sistemas diferentes troquem dados facilmente, ajudando a criar e expandir serviços com integração simples, escalável e independente da tecnologia usada.

#### Django Ninja

**O que é?**
Django Ninja é um framework web para construir APIs com Django, inspirado fortemente no FastAPI.

**Por que usar?**
Pois ele se integra nativamente ao ORM, à autenticação e outras funcionalidades do Django. Além disso, ao usar type hints do Python e Pydantic, o Django Ninja reduz boilerplate, fornece validação automática de dados e gera documentação OpenAPI/Swagger.

### Configuração

#### Ambiente virtual

Dentro da pasta do projeto, crie e ative um ambiente virtual (`venv`) para gerenciar as dependências:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/macOS
```

#### Instalação Django e Django Ninja

Com o ambiente virtual ativado, instale o Django e o Django Ninja:

```bash
pip install django django-ninja
```

#### Criar projeto e app

```bash
django-admin startproject meu_projeto .  
python manage.py startapp minha_api
```

Adicione `minha_api` em `INSTALLED_APPS` no arquivo `meu_projeto/settings.py`.

### Definição da API

#### Arquivo `api.py`

```python
from ninja import NinjaAPI

api = NinjaAPI()
```

Registre em `meu_projeto/urls.py`:

```bash
from django.urls import path
from minha_api.api import api

urlpatterns = [
    path('api/v1/', api.urls),
]
```

### Criando o CRUD

#### Modelos (`models.py`)

```python
from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

#### Schemas (`schemas.py`)

```python
from ninja import ModelSchema
from .models import Pet

class PetSchema(ModelSchema):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species']

class CreatePetSchema(ModelSchema):
    class Meta:
        model = Pet
        fields = ['name', 'species']

class UpdatePetSchema(ModelSchema):
    class Meta:
        model = Pet
        fields = ['name', 'species']
        fields_optional = '__all__'
```

#### Endpoints (`api.py`)

```python
from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from .models import Pet
from .schemas import PetSchema, CreatePetSchema, UpdatePetSchema

api = NinjaAPI()

@api.get("/pets", response=list[PetSchema])
def get_pets(request):
    return Pet.objects.all()

@api.get("/pets/{pet_id}", response=PetSchema)
def get_pet(request, pet_id: int):
    return get_object_or_404(Pet, id=pet_id)

@api.post("/pets", response={201: PetSchema})
def create_pet(request, payload: CreatePetSchema):
    pet = Pet.objects.create(**payload.dict())
    return 201, pet

@api.patch("/pets/{pet_id}", response=PetSchema)
def update_pet(request, pet_id: int, payload: UpdatePetSchema):
    pet = get_object_or_404(Pet, id=pet_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(pet, attr, value)
    pet.save()
    return pet

@api.delete("/pets/{pet_id}", response:{204: None})
def delete_pet(request, pet_id: int):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.delete()
    return 204, None
```

### Migrações e execução

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/api/v1/docs` para ver o Swagger.

---

## Licença

Este projeto está licenciado sob a **MIT License**.
Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
