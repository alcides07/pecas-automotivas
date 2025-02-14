  <section align="center" style="margin-bottom: 2em">
      <img style="border-radius: 50%;" src="https://github.com/user-attachments/assets/355aa48e-e756-4ed7-ace6-116ef04c235b" width='120px'; alt="Logo peças automotivas"/>
    <h4>API de Peças Automotivas 🔥⚙️ </h4>
    <div>
      <a href="#funcionalidades">Funcionalidades</a> •
      <a href="#configuracao-ambiente">Configuração do ambiente</a> •
      <a href="#tarefas-assincronas">Tarefas assíncronas</a> •
      <a href="#testes">Execução dos testes</a> 
    </div>
  </section>

<hr>

<p>Esta API RESTful para consulta de peças automotivas foi desenvolvida utilizando o Django Rest Framework. O sistema oferece funcionalidades para listar, consultar e gerenciar o estoque de peças automotivas. Além disso, permite a importação assíncrona de peças através de planilhas e inclui uma funcionalidade automática para reposição de estoque.</p>

<hr>

## <div id="funcionalidades">🆙 Principais Funcionalidades</div>

#### ✅ Listagem, criação, edição e exclusão de peças (parts)
> Facilite a gestão de peças automotivas.

#### ✅ Importação assíncrona de novas peças via planilha CSV
> Economize tempo importando dados de peças de forma assíncrona.

#### ✅ Listagem, criação, edição e exclusão de modelos de carros (car_models)
> Gerencie modelos de carros com eficiência.

#### ✅ Associação de peças a modelos de carros e gestão de estoque de peças
> Mantenha o controle preciso do inventário de peças e suas associações.

#### ✅ Listagem e cadastro de usuários comuns e administradores 
> Administre usuários com permissões diferentes.

#### ✅ Login de usuários via token JWT
> Garanta segurança nas autenticações com tokens JWT.

#### ✅ Consulta de status de tarefas assíncronas
> Monitore o andamento de tarefas assíncronas em tempo real.

<hr>

## <div id="configuracao-ambiente">🔧 Configuração e execução do ambiente</div>

> Para executar o projeto, certifique-se de que sua máquina possui as seguintes ferramentas:

- [Python 3.12](https://www.python.org/) (obrigatório)
- [PostgreSQL](https://www.postgresql.org/) (obrigatório)
- [Docker](https://docs.docker.com/engine/) (desejável)
- [Docker Compose](https://docs.docker.com/compose) (desejável)
- [Make](https://www.gnu.org/software/make/manual/make.html) (opcional)

<details open>
  <summary><h3>Execução com Docker Compose:</h3></summary>

#### Clone o repositório:

```
git clone https://github.com/alcides07/pecas-automotivas.git
```

#### Acesse o diretório gerado:

```
cd pecas-automotivas
```

#### Execute a aplicação:

```
docker-compose up --build
```

#### Acesse a documentação da API (openAPI):

```
http://localhost:8000/api/docs/
```
</details>

<details>
<summary><h3>Execução com Make (Makefile) </h3></summary>

> A utilização do Make nesse caso serve apenas para simplificar o processo de execução. Nos bastidores, quem realiza a tarefa é o docker-compose.

#### Clone o repositório:

```
git clone https://github.com/alcides07/pecas-automotivas.git
```

#### Acesse o diretório gerado:

```
cd pecas-automotivas
```

#### Execute a aplicação:

```
make full
```

#### Acesse a documentação da API (openAPI):

```
http://localhost:8000/api/docs/
```
</details>

## <div id="tarefas-assincronas">👷 Tarefas assíncronas </div>

A tarefa assíncrona disponível pode ser acessada em `http://localhost:8000/api/parts/upload/`. Para utilizá-la, envie um arquivo CSV contendo as colunas `part_number`, `name`, `details`, `price` e `quantity`, com as informações das peças a serem cadastradas em lote.

Após o envio, um trabalhador `Celery` processará a tarefa. Você pode acompanhar o status do andamento da tarefa em `http://localhost:8000/api/tasks/`, informando o identificador da tarefa para obter detalhes sobre o progresso.

## <div id="testes">🧪 Execução dos testes </div>

Os testes foram desenvolvidos utilizando as ferramentas `pytest`, `factory-boy` e `faker`, que auxiliam na criação de objetos fictícios conforme necessário, proporcionando a construção automatizada dos cenários de teste.

Você pode executar os testes utilizando qualquer um dos seguintes comandos:

`pytest` | `make test` | `docker exec -it pecas-api-dev pytest`
