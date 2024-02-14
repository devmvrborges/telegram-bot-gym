# Bot de Telegram para Treino na Academia

Este é um bot de Telegram desenvolvido em Python utilizando a biblioteca Telebot. O bot oferece funcionalidades para auxiliar no treino na academia, incluindo o envio de uma lista de exercícios e exibição de gifs de ajuda.

## Funcionalidades

- O bot oferece uma lista de treinos disponíveis para o usuário escolher.
- Para cada treino escolhido, o bot exibe uma lista de exercícios com opções para visualizar descrições, marcar como concluído e obter ajuda através de gifs explicativos.
- Os dados dos treinos e exercícios são carregados a partir de arquivos JSON.

## Requisitos

- Python 3.x
- Telebot
- Dotenv

## Como Usar

1. Clone este repositório para o seu ambiente local.
2. Instale as dependências utilizando `pip install -r requirements.txt`.
3. Configure as variáveis de ambiente em um arquivo `.env` com a chave `BOT_TOKEN`.
4. Execute o bot utilizando `python nome_do_arquivo.py`.

## Estrutura do Projeto

- `nome_do_arquivo.py`: Arquivo principal contendo a lógica do bot.
- `treino_a.json`: Arquivo JSON contendo os dados do treino A.
- Outros arquivos e diretórios: Outros arquivos e diretórios relacionados ao projeto.
