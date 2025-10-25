from cryptography.fernet import Fernet, InvalidToken
import base64
import hashlib

class Cryptography:
    def gerar_chave(self, senha: str) -> bytes:
        
        # Gera uma chave 32 bytes a partir da senha fornecida
        # pelo usuário e retorna ela codificada em base64
        chave_hash = hashlib.sha256(senha.encode()).digest() # Gera uma sequência de 32 bytes aleatoriamente derivados da senha
        chave_base64 = base64.urlsafe_b64encode(chave_hash) # Converte os bytes do hash em uma string legíve
        return chave_base64

    def criptografar(self, texto: str, senha: str) -> str:
        
        # Cifra o texto usando a senha fornecida pelo usuário
        chave = self.gerar_chave(senha)  # Gera a chave a partir da senha
        f = Fernet(chave) # Cria um objeto Fernet com a chave
        mensagemCript = f.encrypt(texto.encode()).decode() # Criptografa a mensagem
        return mensagemCript
    
    def descriptografar(self, texto_cifrado: str, senha: str) -> str:
        
        #Descriptografa o texto usando a senha fornecida pelo usuário
        try:
            chave = self.gerar_chave(senha) # Gera a chave a partir da senha
            f = Fernet(chave) # Cria um objeto Fernet com a chave
            mensagemDescript = f.decrypt(texto_cifrado.encode()).decode()  # Descriptografa e converte para string
            return mensagemDescript
        except InvalidToken: # Exceção caso a chave esteja errada
            raise ValueError("Chave incorreta.") # Informa que a chave está incorreta

    