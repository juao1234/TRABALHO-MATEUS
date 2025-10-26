import os
from banco import BancoDeDados
from model import Messagem
from crypto import Cryptography

class AppMensageria:
    def __init__(self):
        self.banco = BancoDeDados()
        self.usuario = None
        self.crypto = Cryptography()

    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")

    def login(self):
        self.limpar_tela()
        nome = input("Digite seu @usuario: ").strip()
        if not nome.startswith("@"):
            print("O nome deve começar com '@'.")
            return self.login()
        self.usuario = nome
        self.limpar_tela()
        print(f"\nLogin realizado com sucesso: {self.usuario}\n")

    def menu(self):
        while True:
            print("\n1. Para enviar mensagem")
            print("2. Para ver mensagens não lidas")
            print("3. Para sair")

            opcao = input("\nEscolha a sua ação: ").strip()
            self.limpar_tela()

            if opcao == "1":
                self.enviar()
            elif opcao == "2":
                self.ver_mensagens()
            elif opcao == "3":
                print("Saindo...")
                break
            else:
                print("Opção inválida!")

    def enviar(self):
        destino = input("Enviar para o usuário (comece com @): ").strip()
        
        if not destino.startswith("@"):
            print("O usuário de destino deve começar com '@'.")
            self.limpar_tela()
            return
        
        if destino == self.usuario:
            print("Você não pode enviar mensagem para si mesmo.")
            self.limpar_tela()
            return
        
        texto = input("Digite a mensagem (mínimo 50 caracteres): ").strip()
        if len(texto) < 50:
            print("Mensagem muito curta.")
            return

        senha = input("Digite a chave criptográfica: ").strip()
        self.limpar_tela()

        mensagem_cifrada = self.crypto.criptografar(texto, senha)
        self.banco.enviar_mensagem(self.usuario, destino, mensagem_cifrada)
        print("Mensagem cifrada e enviada com sucesso!")

    def ver_mensagens(self):
        mensagens = self.banco.listar_nao_lidas(self.usuario)
        self.limpar_tela()
        if not mensagens:
            print("Não existem novas mensagens.")
            return
        
        print("\nMensagens não lidas:")
        for i, msg in enumerate(mensagens):
            print(f"{i+1}. De {msg['de']}")

        try:
            escolha = int(input("\nEscolha o número da mensagem: ")) - 1
            mensagem = mensagens[escolha]
        except (ValueError, IndexError):
            print("Escolha inválida.")
            return

        senha = input("Digite a chave criptográfica para decifrar: ").strip()
        self.limpar_tela()

        try:
            texto = self.crypto.descriptografar(mensagem["mensagem"], senha)
            print(f"\nMensagem decifrada:\n{texto}")
            self.banco.marcar_como_lida(mensagem["_id"])
        except ValueError:
            print("Chave incorreta!")

if __name__ == "__main__":
    try:
        app = AppMensageria()
        app.login()
        app.menu()
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")
