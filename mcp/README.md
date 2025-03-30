# Desafio Técnico C2S:
## Client-server MCP para consulta de Veículos

### (1) --  Montando o ambiente
* Baixar o repositório https://github.com/julio-cascalles/temp.git
* entrar na pasta do projeto (/temp/mcp)
* Executar o comando 
```
pip install -r requirements.txt
```
* Executar o programa, usando a opção 1
> Isso deixará o servidor local escutando na porta 5000

* Abrir outro terminal para o client na mesma pasta
* **Quando o banco de dados estiver VAZIO**, execute o programa usando a opçção 2;
* Execute o programa usando a opção para enviar consultas (opção 3 - o lado cliente).
* Envie consultas usando o formato chave valor indicado no prompt
```
Exemplo:
    marca=Honda modelo=Fit cor=azul
```

### (2) --  Estrutura das pastas
* /dados
    *  veiculo.py : O modelo de dados para a tabela `Veiculo`;
    * cores.py : Contém todas as cores possíveis;
    * marca.py : Contém as marcas e modelos;
    * status : Contém os possíveis status dos veículos.
* /rotas
    * client.py : Define a função `read_mcp` para enviar consultas para o servidor;
    * server.py : Permite iniciar o servidor com uma função de callback para processar as consultas recebidas;
    * const.py : Contém os valores para HOST e PORT.
* /interface
    * client.py : Interage com o usuário para montar a consulta no terminal, validando os campos e seus conteúdos;
    * server.py : Ativa a classe de servidor 
    (em /rotas) com a função `retornar_consulta`
    * dados.py : Permite criar o banco de dados com uma quantidade de dados definida pelo usuário (entre 100 e 5000)
* /util
    * duck_model.py - Biblioteca que _eu desenvolvi_ para lidar com arquivos Parquet de forma mais flexível (como um ORM simplificado);
