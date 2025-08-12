from .calculator import calculator_bp
from .guess_number import guess_bp
from .main import main as main_bp
from .user import auth as auth_bp

__all__ = ["auth_bp", "calculator_bp", "main_bp", "guess_bp"]
