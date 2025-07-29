from fastapi import APIRouter, Request
from pathlib import Path
import importlib
import inspect
import sys
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ArcCmsRouter:
    @staticmethod
    def _get_route_path(filepath: Path, base_path: Path) -> str:
        """Convertit le chemin du fichier en route"""
        relative_path = filepath.relative_to(base_path).with_suffix('')
        parts = []
        
        for part in relative_path.parts:
            if part == 'index':
                continue
            if part.startswith('_'):
                continue
            if part.startswith('[') and part.endswith(']'):
                part = f"{{{part[1:-1]}}}"
            parts.append(part)
        
        return '/' + '/'.join(parts)

    @staticmethod
    def _get_route_params(module: Any) -> Dict[str, Any]:
        """Extrait les paramètres de la fonction handler"""
        if hasattr(module, 'get'):
            func = module.get
        elif hasattr(module, 'default'):
            func = module.default
        else:
            return {}
        
        sig = inspect.signature(func)
        return {
            name: param.default if param.default != inspect.Parameter.empty else ...
            for name, param in sig.parameters.items()
            if name not in ['request', 'self']
        }

    @classmethod
    def register_routes(cls, router: APIRouter, base_path: Path):
        """Enregistre toutes les routes avec gestion des paramètres"""
        # Convertir en Path si c'est une string
        base_path = Path(base_path) if isinstance(base_path, str) else base_path
        
        # S'assurer que le chemin de base est absolu
        if not base_path.is_absolute():
            base_path = base_path.resolve()
        
        # Ajouter le répertoire parent au PYTHONPATH temporairement
        parent_dir = str(base_path.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        for filepath in base_path.glob('**/*.py'):
            if filepath.name.startswith(('_', '.')) or not filepath.is_file():
                continue

            route_path = cls._get_route_path(filepath, base_path)
            
            # Calculer le nom du module différemment
            module_path_parts = filepath.relative_to(base_path.parent).with_suffix('').parts
            module_path = '.'.join(module_path_parts)
            
            try:
                module = importlib.import_module(module_path)
                params = cls._get_route_params(module)
                
                # Enregistrement des méthodes HTTP
                for method in ['get', 'post', 'put', 'delete', 'patch']:
                    if hasattr(module, method):
                        handler = getattr(module, method)
                        getattr(router, method)(
                            route_path,
                            **({'response_model': handler.__annotations__.get('return')} 
                               if hasattr(handler, '__annotations__') else {})
                        )(handler)
                
                # Fallback pour export default
                if hasattr(module, 'default') and not any(hasattr(module, m) for m in ['get', 'post', 'put', 'delete', 'patch']):
                    handler = module.default
                    router.get(
                        route_path,
                        **({'response_model': handler.__annotations__.get('return')} 
                           if hasattr(handler, '__annotations__') else {})
                    )(handler)
                
                logger.info(f"Route registered: {route_path} -> {module_path}")
                
            except Exception as e:
                logger.error(f"Failed to load route {filepath}: {str(e)}")
                continue