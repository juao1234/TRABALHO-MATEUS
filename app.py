import os
import time

from crypto import Cryptography
from model import Messagem
from repository import MensagemRepository


class AppMensageria:
    def __init__(self):
        self.banco = MensagemRepository()
        self.usuario = None
        self.crypto = Cryptography()

    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")

    def cabecalho(self, titulo):
        """Exibe um cabeçalho formatado"""
        print("\n" + "="*50)
        print(f"  {titulo.upper()}")
        print("="*50)

    def login(self):
        self.limpar_tela()
        self.cabecalho("LOGIN")
        nome = input("\nDigite seu @usuario: ").strip()
        
        if not nome.startswith("@"):
            print("\nO nome deve começar com '@'.")
            time.sleep(1.5)
            return self.login()
        
        self.usuario = nome
        print(f"\nLogin realizado com sucesso!")
        print(f"   Bem-vindo, {self.usuario}")
        time.sleep(2)
        self.limpar_tela()

    def menu(self):
        while True:
            self.cabecalho(f"MENU - {self.usuario}")
            print("\n  [1] Enviar mensagem")
            print("  [2] Ver mensagens não lidas")
            print("  [3] Sair")
            print("\n" + "-"*50)

            opcao = input("\n➤ Escolha uma opção: ").strip()
            self.limpar_tela()

            if opcao == "1":
                self.enviar()
            elif opcao == "2":
                self.ver_mensagens()
            elif opcao == "3":
                print("\nAté logo!\n")
                break
            else:
                print("\nOpção inválida!")
                time.sleep(1)

    def enviar(self):
        self.cabecalho("ENVIAR MENSAGEM")
        
        destino = input("\nPara (comece com @): ").strip()
        
        if not destino.startswith("@"):
            print("\nO usuário deve começar com '@'.")
            time.sleep(1.5)
            return
        
        if destino == self.usuario:
            print("\nVocê não pode enviar mensagem para si mesmo.")
            time.sleep(1.5)
            return
        
        print(f"\nEscreva sua mensagem (mínimo 50 caracteres)")
        texto = input("➤ ").strip()
        
        if len(texto) < 50:
            print(f"\nMensagem muito curta! ({len(texto)}/50 caracteres)")
            time.sleep(1.5)
            return
        
        if len(texto) == 0:
            print("\nMensagem vazia!")
            time.sleep(1.5)
            return

        senha = input("\nChave criptográfica: ").strip()
        
        if not senha:
            print("\nSenha não pode ser vazia!")
            time.sleep(1.5)
            return

        # Criptografa a mensagem
        mensagem_cifrada = self.crypto.criptografar(texto, senha)
        
        # Cria objeto Messagem e salva
        mensagem = Messagem(
            sender=self.usuario,
            receiver=destino,
            content=mensagem_cifrada
        )
        
        self.banco.salvar_mensagem(mensagem.to_dict())
        
        print("\nMensagem cifrada e enviada com sucesso!")
        print(f"   De: {self.usuario} → Para: {destino}")
        time.sleep(2)

    def ver_mensagens(self):
        mensagens = self.banco.buscar_nao_lidas(self.usuario)
        
        if not mensagens:
            self.cabecalho("MENSAGENS")
            print("\nNão existem novas mensagens.\n")
            time.sleep(1.5)
            return
        
        self.cabecalho(f"MENSAGENS NÃO LIDAS ({len(mensagens)})")
        
        for i, msg_dict in enumerate(mensagens):
            msg = Messagem.from_dict(msg_dict)
            data = msg.timestamp.strftime("%d/%m/%Y %H:%M")
            print(f"\n  [{i+1}] De: {msg.sender}")
            print(f"      {data}")
        
        print("\n" + "-"*50)

        try:
            escolha = int(input("\nEscolha o número da mensagem: ")) - 1
            if escolha < 0 or escolha >= len(mensagens):
                raise IndexError
            mensagem_dict = mensagens[escolha]
        except (ValueError, IndexError):
            print("\nEscolha inválida!")
            time.sleep(1.5)
            return

        senha = input("\nChave para decifrar: ").strip()
        self.limpar_tela()

        try:
            mensagem = Messagem.from_dict(mensagem_dict)
            texto = self.crypto.descriptografar(mensagem.content, senha)
            
            self.cabecalho("MENSAGEM DECIFRADA")
            print(f"\nDe: {mensagem.sender}")
            print(f"{mensagem.timestamp.strftime('%d/%m/%Y às %H:%M')}")
            print("\n" + "-"*50)
            print(f"\n{texto}")
            print("\n" + "-"*50)
            
            self.banco.marcar_como_lida(mensagem_dict["_id"])
            input("\nPressione ENTER para voltar...")
            
        except ValueError:
            print("\nChave incorreta! Não foi possível decifrar.")
            time.sleep(2)


if __name__ == "__main__":
    try:
        app = AppMensageria()
        app.login()
        app.menu()
    except KeyboardInterrupt:
        print("\n\nEncerrado pelo usuário.\n")
