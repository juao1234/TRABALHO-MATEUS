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
        nome = input("\n👤 Digite seu @usuario: ").strip()
        
        if not nome.startswith("@"):
            print("\n❌ O nome deve começar com '@'.")
            time.sleep(1.5)
            return self.login()
        
        self.usuario = nome
        print(f"\n✅ Login realizado com sucesso!")
        print(f"   Bem-vindo, {self.usuario}")
        time.sleep(2)
        self.limpar_tela()

    def menu(self):
        while True:
            self.cabecalho(f"MENU - {self.usuario}")
            print("\n  [1] 📤 Enviar mensagem")
            print("  [2] 📬 Ver mensagens não lidas")
            print("  [3] 🚪 Sair")
            print("\n" + "-"*50)

            opcao = input("\n➤ Escolha uma opção: ").strip()
            self.limpar_tela()

            if opcao == "1":
                self.enviar()
            elif opcao == "2":
                self.ver_mensagens()
            elif opcao == "3":
                print("\n👋 Até logo!\n")
                break
            else:
                print("\n❌ Opção inválida!")
                time.sleep(1)

    def enviar(self):
        self.cabecalho("ENVIAR MENSAGEM")
        
        destino = input("\n📨 Para (comece com @): ").strip()
        
        if not destino.startswith("@"):
            print("\n❌ O usuário deve começar com '@'.")
            time.sleep(1.5)
            return
        
        if destino == self.usuario:
            print("\n❌ Você não pode enviar mensagem para si mesmo.")
            time.sleep(1.5)
            return
        
        print(f"\n✏️  Escreva sua mensagem (máximo 50 caracteres)")
        texto = input("➤ ").strip()
        
        if len(texto) > 50:
            print(f"\n❌ Mensagem muito longa! ({len(texto)}/50 caracteres)")
            time.sleep(1.5)
            return
        
        if len(texto) == 0:
            print("\n❌ Mensagem vazia!")
            time.sleep(1.5)
            return

        senha = input("\n🔐 Chave criptográfica: ").strip()
        
        if not senha:
            print("\n❌ Senha não pode ser vazia!")
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
        
        print("\n✅ Mensagem cifrada e enviada com sucesso!")
        print(f"   De: {self.usuario} → Para: {destino}")
        time.sleep(2)

    def ver_mensagens(self):
        mensagens = self.banco.buscar_nao_lidas(self.usuario)
        
        if not mensagens:
            self.cabecalho("MENSAGENS")
            print("\n📭 Não existem novas mensagens.\n")
            time.sleep(1.5)
            return
        
        self.cabecalho(f"MENSAGENS NÃO LIDAS ({len(mensagens)})")
        
        for i, msg_dict in enumerate(mensagens):
            msg = Messagem.from_dict(msg_dict)
            data = msg.timestamp.strftime("%d/%m/%Y %H:%M")
            print(f"\n  [{i+1}] 📩 De: {msg.sender}")
            print(f"      🕐 {data}")
        
        print("\n" + "-"*50)

        try:
            escolha = int(input("\n➤ Escolha o número da mensagem: ")) - 1
            if escolha < 0 or escolha >= len(mensagens):
                raise IndexError
            mensagem_dict = mensagens[escolha]
        except (ValueError, IndexError):
            print("\n❌ Escolha inválida!")
            time.sleep(1.5)
            return

        senha = input("\n🔐 Chave para decifrar: ").strip()
        self.limpar_tela()

        try:
            mensagem = Messagem.from_dict(mensagem_dict)
            texto = self.crypto.descriptografar(mensagem.content, senha)
            
            self.cabecalho("MENSAGEM DECIFRADA")
            print(f"\n📨 De: {mensagem.sender}")
            print(f"🕐 {mensagem.timestamp.strftime('%d/%m/%Y às %H:%M')}")
            print("\n" + "-"*50)
            print(f"\n{texto}")
            print("\n" + "-"*50)
            
            self.banco.marcar_como_lida(mensagem_dict["_id"])
            input("\n✅ Pressione ENTER para voltar...")
            
        except ValueError:
            print("\n❌ Chave incorreta! Não foi possível decifrar.")
            time.sleep(2)


if __name__ == "__main__":
    try:
        app = AppMensageria()
        app.login()
        app.menu()
    except KeyboardInterrupt:
        print("\n\n👋 Encerrado pelo usuário.\n")