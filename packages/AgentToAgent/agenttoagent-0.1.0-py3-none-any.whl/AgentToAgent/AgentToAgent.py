
from threading import Lock
from time import time

class AgentToAgent:
    def __init__(self):
        self.inboxes = {}
        self.lock = Lock()

    def send(self, fromAgent, toAgent, content, ttl=None):
        """Send a message with optional Time-To-Live (seconds)"""
        message = {
            "from": fromAgent,
            "to": toAgent,
            "content": content,
            "timestamp": time(),
            "expiry": time() + ttl if ttl else None,
        }
        with self.lock:
            self.inboxes.setdefault(toAgent, []).append(message)

    def receive(self, agentName, allowedFrom=None):
        """Retrieve and remove all valid messages for agentName from allowed senders"""
        with self.lock:
            inbox = self.inboxes.get(agentName, [])
            now = time()
            validMessages = [
                m for m in inbox
                if (not m["expiry"] or m["expiry"] > now)
                and (allowedFrom is None or m["from"] in allowedFrom)
            ]
            self.inboxes[agentName] = [m for m in inbox if m not in validMessages]
        return validMessages

    def purgeExpired(self):
        """Optionally call this to remove expired messages from all inboxes"""
        with self.lock:
            now = time()
            for agent, inbox in self.inboxes.items():
                self.inboxes[agent] = [m for m in inbox if not m["expiry"] or m["expiry"] > now]
