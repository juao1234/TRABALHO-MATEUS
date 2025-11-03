# TRABALHO-MATEUS

Este é um projeto de um sistema de mensagens seguras via linha de comando. As mensagens são criptografadas de ponta a ponta, garantindo que apenas o destinatário com a chave correta possa lê-las.

## Funcionalidades

- **Login de Usuário:** Identificação do usuário através de um nome com "@".
- **Envio de Mensagens Criptografadas:** As mensagens são criptografadas antes de serem enviadas para o banco de dados.
- **Caixa de Entrada:** Verificação de mensagens não lidas.
- **Leitura de Mensagens:** As mensagens são descriptografadas para leitura.

## Como Usar

### Pré-requisitos

- Python 3
- MongoDB

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/TRABALHO-MATEUS.git
   cd TRABALHO-MATEUS
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows, use `.venv\Scripts\activate`
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   - Renomeie o arquivo `example.env` para `.env`.
   - Abra o arquivo `.env` e, se necessário, altere a string de conexão do MongoDB (`MONGO_URI`) e outras variáveis para corresponder à sua configuração.

### Execução

Para iniciar a aplicação, execute o seguinte comando no terminal:

```bash
python app.py
```

Siga as instruções no terminal para fazer login, enviar e receber mensagens.