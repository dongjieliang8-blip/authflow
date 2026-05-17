"""Sample authentication code for AuthFlow demo."""
import hashlib
import sqlite3


class AuthManager:
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)

    # Vulnerability: Plaintext password storage
    def register(self, username, password):
        self.db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)  # No hashing!
        )
        self.db.commit()

    # Vulnerability: SQL injection
    def login(self, username, password):
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        result = self.db.execute(query).fetchone()
        return result is not None

    # Vulnerability: No rate limiting
    def login_attempt(self, username, password):
        """No protection against brute force."""
        return self.login(username, password)

    # Vulnerability: Session not invalidated
    def create_session(self, user_id):
        token = hashlib.md5(str(user_id).encode()).hexdigest()  # Weak token
        self.db.execute(
            "INSERT INTO sessions (user_id, token) VALUES (?, ?)",
            (user_id, token)
        )
        self.db.commit()
        return token
