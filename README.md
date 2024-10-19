
# Sobre o projeto

O projeto consiste em uma API que coleta dados de eventos do site Sympla nas cidades de Santos, São Vicente e Guarujá por meio de web scraping. 

A API retorna as informações em formato JSON, facilitando a integração com outras plataformas e aplicações.

# Demonstração

![Assista ao vídeo](/video/de%20ZeroLoop%20-%20Hackathon.gif)

# Tecnologias utilizadas
- Python
- Selenium
- Sql Server

# Como executar o projeto

- Pré-requisitos: Python

#### Instalar as blibiotecas
```
pip install -r requirements.txt
```

#### Coletar os dados
```
python scraping.py
```

#### Mandar os dados para o banco
```
python db.py
```

#### Iniciar a api
```
python rotas.py
```

# Autor

Arthur de Souza Silva

[LinkedIn](https://www.linkedin.com/in/arthur-souza-dev/)
