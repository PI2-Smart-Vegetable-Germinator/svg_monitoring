# SVG Monitoring
Microsserviço de Monitoramento do SVG.

## Instalação e Configuração

### Pré-requisitos

- Para rodar o projeto é necessário ter o Docker e o docker-compose instalados.

- Se ainda não existir, é preciso criar uma rede no docker com o comando `docker network create svg_shared`

### Primeiros passos

Após clonar o repositório, rodar `docker-compose up`. Com o container rodando, inicializar e rodar as migrações do banco de dados com o comando:

- `docker exec -it svg_monitoring_app_1 python manage.py db upgrade`

**Sempre** que for realizada alguma mudança nas tabelas do banco (adicionar/remover tabela, adicionar/remover coluna, etc.) rodar:

- `docker exec -it svg_monitoring_app_1 python manage.py db migrate` 

e em seguida:

- `docker exec -it svg_monitoring_app_1 python manage.py db upgrade`

Este container roda na porta 5001 da máquina _host_.