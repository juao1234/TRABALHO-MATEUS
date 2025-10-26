from datetime import datetime

class Messagem:
    def __init__(self, sender, receiver, content, status="nova", timestamp=None):
       
        self.sender = sender
       
        self.receiver = receiver
       
        self.content = content
        
        self.status = status
       
        self.timestamp = timestamp or datetime.now()

    def mark_as_read(self):
        
        self.status = "lida"

    def to_dict(self):
        
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        
        return cls(
            sender=data["sender"],
            receiver=data["receiver"],
            content=data["content"],
            status=data.get("status", "nova"),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None,
        )
