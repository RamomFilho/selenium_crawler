# Selenium Cralwer

Construido com as seguintes ferramentas:

- Selenium
- Docker

## Instalação
Preparação de ambiente da aplicação.
Para aplicação é indicado rodar em um ambiente isolado, uma [virtualenv](https://docs.python.org/pt-br/dev/library/venv.html).
Requisitos:

* Python 3.6+
* Docker  20.10+


Com o ambiente virtual ativado instale as dependências com o seguinte comando no terminal:
```shell
$ pip install -r requirements.txt
```

## Como executar o projeto

Vamos executar os comandos abaixo partindo que esteja no diretório raiz onde fez o clone do projeto.
```sh
docker run -d -p 4444:4444 selenium/standalone-chrome
python crawler.py

```


