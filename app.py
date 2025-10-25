import os
from banco import BancoDeDados
from usuario import Usuario
from criptografia import Cryptography


class AppMensageria:
    def __init__(self):
        self.banco = BancoDeDados()
        self.usuario = None
        self.crypto = Cryptography()

    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")

    def login(self):
        self.limpar_tela()
        nome = input("Digite seu @usuario: ")
        self.usuario = Usuario(nome, self.banco)
        self.limpar_tela()
        print(f"\nVocê fez o login como: @{nome}\n")

    def menu(self):
        while True:
            print("\n1. Para enviar mensagem")
            print("2. Para ver mensagens não lidas")
            print("3. Para sair")

            opcao = input("\nEscolha a sua ação: ")
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
        destino = input("Enviar para o usuário @: ")
        texto = input("Digite a mensagem (mínimo 50 caracteres): ")
        if len(texto) < 50:
            print("Mensagem muito curta.")
            return

        senha = input("Digite a chave criptográfica: ")
        self.limpar_tela()

        mensagem_cifrada = self.crypto.criptografar(texto, senha)
        self.usuario.enviar_mensagem(destino, mensagem_cifrada)
        print("Mensagem enviada e cifrada com sucesso!")

    def ver_mensagens(self):
        mensagens = self.usuario.listar_nao_lidas()
        self.limpar_tela()
        if not mensagens:
            print("Não existem novas mensagens.")
            return
        
        print("\nMensagens não lidas:")
        for i, msg in enumerate(mensagens):
            print(f"{i+1}. De @{msg['de']}")

        escolha = int(input("\nEscolha o número da mensagem: ")) - 1
        mensagem = mensagens[escolha]
        senha = input("Digite a chave criptográfica para decifrar a mensagem: ")
        self.limpar_tela()

        try:
            texto = self.crypto.descriptografar(mensagem["mensagem"], senha)
            print(f"\nMensagem: {texto}")
            self.usuario.marcar_como_lida(mensagem["_id"])
        except ValueError:
            print("Chave incorreta!")


if __name__ == "__main__":
    try:
        app = AppMensageria()
        app.login()
        app.menu()
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")
