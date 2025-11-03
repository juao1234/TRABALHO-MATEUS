import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class MensagemRepository:
    """Responsável por salvar e buscar mensagens no MongoDB."""

    def __init__(self):
        uri = os.getenv("MONGO_URI")
        db_name = os.getenv("DB_NAME")
        collection_name = os.getenv("COLLECTION_MESSAGES")
        
        # Valida se as variáveis foram configuradas
        if not uri:
            raise ValueError("❌ MONGO_URI não configurada no arquivo .env")
        if not db_name:
            raise ValueError("❌ DB_NAME não configurada no arquivo .env")
        if not collection_name:
            raise ValueError("❌ COLLECTION_MESSAGES não configurada no arquivo .env")
        
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Testa a conexão
            client.server_info()
            
            self.db = client[db_name]
            self.col = self.db[collection_name]
        except Exception as e:
            raise ConnectionError(f"❌ Erro ao conectar ao MongoDB: {e}")
        
    def salvar_mensagem(self, msg_dict: dict):
        """Insere uma nova mensagem na coleção."""
        # Adiciona campos de controle se não existirem
        if "status" not in msg_dict:
            msg_dict["status"] = "nova"
        if "timestamp" not in msg_dict:
            msg_dict["timestamp"] = datetime.now().isoformat()
            
        self.col.insert_one(msg_dict)
    
    def buscar_nao_lidas(self, destinatario):
        """Retorna todas as mensagens não lidas ordenadas por data."""
        return list(
            self.col.find({
                "receiver": destinatario,
                "status": "nova"
            }).sort("timestamp", 1)
        )

    def marcar_como_lida(self, msg_id):
        """Atualiza o status da mensagem."""
        self.col.update_one(
            {"_id": msg_id},
            {
                "$set": {
                    "status": "lida",
                    "read_at": datetime.now().isoformat()
                }
            },
        )