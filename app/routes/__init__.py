from .user import auth as auth_bp
from .calculator import calculator_bp
from .main import main as main_bp
from .guess_number import guess as guess_bp

__all__ = ['auth_bp', 'calculator_bp', 'main_bp', 'guess_bp']
