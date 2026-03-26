
import datetime
import os
from PyQt6.QtWidgets import QFrame, QTextEdit
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

_SALT = b"JustForYou_39i24892_v1" # Key must be the same across save/load.
_KEY_SIZE = 32   # 32 bytes = AES-256
_NONCE_SIZE = 12  # 12 bytes = standard for AES-GCM

def _derive_key(password: str) -> bytes:
    """
    Derive a strong AES key from a password using PBKDF2.
    - Slow by design (480k iterations) → resists brute-force attacks
    - Same password + salt → same key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=_KEY_SIZE,
        salt=_SALT,
        iterations=480_000,
    )
    return kdf.derive(password.encode("utf-8"))

class History:

    def __init__(self, password: str):
        self.history_text_edit = None
        self._file_path = "history.bin"

        # AES-GCM provides encryption + integrity (tamper detection)
        self._aes = AESGCM(_derive_key(password))

    def setup(self):
        self.history_text_edit = QTextEdit()
        self.history_text_edit.setReadOnly(True)
        self.history_text_edit.setFrameShape(QFrame.Shape.NoFrame)

    def update(self, element):
        timestamp_str = datetime.datetime.now().strftime("%H:%M:%S")
        self.history_text_edit.append(f"[{timestamp_str}]: {element}")

    def clear(self):
        if self.history_text_edit:
            self.history_text_edit.clear()
        if os.path.exists(self._file_path):
            os.remove(self._file_path)


    def _get_log_path(self) -> str:
        os.makedirs(self.log_dir, exist_ok=True)
        filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".bin"
        return os.path.join(self.log_dir, filename)

    def load(self):
        """Read file → extract nonce + ciphertext → decrypt → restore text."""
        if not os.path.exists(self._file_path):
            return
        try:
            with open(self._file_path, "rb") as f:
                nonce = f.read(_NONCE_SIZE)   # first 12 bytes = nonce
                ciphertext = f.read()          # rest = ciphertext + 16-byte GCM tag

            # Decrypt + verify integrity
            # If password is wrong OR file modified → raises exception
            plaintext = self._aes.decrypt(nonce, ciphertext, None)
            if self.history_text_edit:
                self.history_text_edit.setPlainText(plaintext.decode("utf-8").strip())
        except Exception as e:
            print(f"History.load error: {e}")

    def save(self):
        """Serialize text → encrypt → store as [nonce | ciphertext+tag]."""
        if not self.history_text_edit:
            return
        content = self.history_text_edit.toPlainText().strip()
        if not content:
            return
        try:
            nonce = os.urandom(_NONCE_SIZE)  # must be unique per encryption
            # AES-GCM returns: ciphertext + 16-byte authentication tag
            ciphertext = self._aes.encrypt(nonce, content.encode("utf-8"), None)
            with open(self._file_path, "wb") as f:
                f.write(nonce)        # [0:12]  — 12 raw bytes
                f.write(ciphertext)   # [12:]   — ciphertext + 16-byte auth tag
        except Exception as e:
            print(f"History.save error: {e}")



history = History("JustForYou2349#")