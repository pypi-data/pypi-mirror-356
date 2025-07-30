from dotenv import load_dotenv, find_dotenv, set_key
from cryptography.fernet import Fernet
import os

# region TODOs for future implementations:
# TODO [ ] Log errors instead of printing them (es. con logging module)
# TODO [ ] Raise custom exceptions for missing or invalid keys
# TODO [ ] Aggiungere supporto per rotazione chiavi e versionamento
# TODO [ ] Verificare validità della chiave (lunghezza, base64) prima di usarla
# TODO [ ] Creare un wrapper per criptare/dcriptare interi oggetti o dizionari
# endregion

load_dotenv()


def get_fernet():
    """
   Retrieve the Fernet object using the key from environment variables.
   """
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path, override=True)

    key = os.getenv("FERNET_KEY")
    if not key:
        # Genera una nuova chiave
        key = Fernet.generate_key().decode()
        # Salva nel file .env (creandolo o aggiornandolo)
        set_key(dotenv_path, "FERNET_KEY", key)
        os.environ["FERNET_KEY"] = key  # aggiorna anche l'env corrente

    try:
        return Fernet(key.encode())
    except Exception as ex:
        print(f"Failed to initialize Fernet: {ex}")
        raise


def encrypt(text: str) -> str:
    """
    Encrypt a string using Fernet.
    """
    return get_fernet().encrypt(text.encode()).decode()


def decrypt(token: str) -> str:
    """
    Decrypt a Fernet-encrypted string.
    """
    return get_fernet().decrypt(token.encode()).decode()
