### Documentação do Projeto AIRBNB
Este guia fornece as instruções necessárias para configurar e executar o projeto AIRBNB, que utiliza Flask, Python e Docker. Siga os passos abaixo para rodar o projeto localmente.

Pré-requisitos
Antes de iniciar, verifique se você tem os seguintes itens instalados:

Python (versão 3.8 ou superior)

Docker e Docker Compose

Git (opcional, para clonar o repositório)

Passo a Passo para Rodar o Projeto
1. Clonar o Repositório (Opcional)
   
2. Instalar as Dependências do Python
Instale as bibliotecas necessárias listadas no arquivo requirements.txt:

pip install -r requirements.txt
3. Configurar o Banco de Dados com Flask-Migrate
O projeto utiliza o Flask-Migrate para gerenciar as migrações do banco de dados. Siga as etapas abaixo para configurá-lo corretamente:

a. Inicializar o Sistema de Migrações
Execute o seguinte comando para criar a pasta de migrações:

flask db init
Observação: Se o comando flask não for reconhecido, você pode tentar:

python -m flask db init
b. Criar a Primeira Migração
Gere o script de migração com base nos modelos do banco de dados:

flask db migrate -m "Initial migration"
c. Aplicar as Migrações ao Banco de Dados
Execute o comando abaixo para aplicar as migrações e criar as tabelas no banco de dados:

flask db upgrade
4. Configurar e Subir os Contêineres com Docker
O projeto usa Docker para rodar o Flask e o MySQL em contêineres. Siga as instruções abaixo:

a. Criar e Subir os Contêineres
Execute o comando abaixo para construir e iniciar os contêineres:

docker-compose up --build
Este comando irá:

Construir a imagem do Flask

Iniciar o contêiner do MySQL

Configurar a rede entre os contêineres

b. Verificar se os Contêineres Estão em Execução
Para verificar se os contêineres estão rodando corretamente, utilize o seguinte comando:

docker ps
Você deverá ver dois contêineres ativos: um para o Flask e outro para o MySQL.

5. Acessar o Projeto
Após subir os contêineres, o projeto estará disponível em:

Flask: http://localhost:5000

MySQL: Acessível na porta 3306 (ou 3307, dependendo da configuração no docker-compose.yml)

phpMyAdmin (opcional): http://localhost:8080, caso tenha sido configurado no docker-compose.yml
