from typing import Any
from fastapi import FastAPI, APIRouter
from pathlib import Path
from .internationalisation_manager import InternationalisationManager
from .config_manager import ConfigManager
from .router import ArcCmsRouter

_intl = InternationalisationManager()
_config = ConfigManager()
_router = ArcCmsRouter()

def init_app():
    """Initialise toutes les ressources"""
    _intl.load_all()
    _config.load_all()

def t(key: str, locale: str = 'fr', module: str = "global", **kwargs) -> str:
    """Récupère une traduction"""
    value = _intl.get(module, key, locale) or key
    return value.format(**kwargs) if kwargs else value

def cfg(key: str, default: Any = None, module: str = "global") -> Any:
    """Récupère une configuration"""
    return _config.get(module, key, default)

def register_routes(router: APIRouter, base_path: str):
    """Enregistre les routes (nouvelle fonction exposée)"""
    _router.register_routes(router, Path(base_path))