"""
Workaround específico para Termux/Android donde uvx tiene problemas de permisos.
"""
import os
import json
import shutil
import subprocess
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def is_termux() -> bool:
    """Detecta si estamos ejecutándose en Termux."""
    return (
        os.path.exists('/data/data/com.termux') or 
        'TERMUX_VERSION' in os.environ or
        'com.termux' in os.environ.get('PREFIX', '')
    )

def is_android() -> bool:
    """Detecta si estamos en Android."""
    return (
        os.path.exists('/system/build.prop') or
        os.path.exists('/android_root') or
        'ANDROID_ROOT' in os.environ
    )

def check_mcp_package_installed(package_name: str) -> bool:
    """Verifica si un paquete MCP está instalado."""
    try:
        result = subprocess.run(
            ['python', '-c', f'import {package_name.replace("-", "_")}'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False

def install_mcp_package(package_name: str) -> bool:
    """Instala un paquete MCP usando pip."""
    try:
        logger.info(f"Installing {package_name} using pip...")
        result = subprocess.run(
            ['pip', 'install', package_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info(f"Successfully installed {package_name}")
            return True
        else:
            logger.error(f"Failed to install {package_name}: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error installing {package_name}: {e}")
        return False

def get_termux_compatible_config(original_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convierte la configuración MCP para ser compatible con Termux.
    Reemplaza uvx con python -m para evitar problemas de permisos.
    """
    if not original_config.get('mcpServers'):
        return original_config
    
    compatible_config = {"mcpServers": {}}
    
    for server_name, server_config in original_config['mcpServers'].items():
        if server_config.get('disabled', False):
            continue
            
        # Crear configuración compatible
        new_config = server_config.copy()
        
        # Si usa uvx, cambiar a python -m
        if server_config.get('command') == 'uvx':
            args = server_config.get('args', [])
            if args:
                package_name = args[0]
                
                # Verificar si el paquete está instalado
                if not check_mcp_package_installed(package_name):
                    logger.warning(f"Package {package_name} not installed, attempting to install...")
                    if not install_mcp_package(package_name):
                        logger.error(f"Failed to install {package_name}, skipping server {server_name}")
                        continue
                
                # Cambiar comando a python -m
                new_config['command'] = 'python'
                new_config['args'] = ['-m', package_name.replace('-', '_')]
                
                logger.info(f"Converted {server_name}: uvx {package_name} -> python -m {package_name.replace('-', '_')}")
        
        # Configurar variables de entorno para Termux
        env = new_config.get('env', {})
        
        # Configurar directorio temporal en ubicación accesible
        termux_tmp = os.path.expanduser('~/tmp')
        if not os.path.exists(termux_tmp):
            os.makedirs(termux_tmp, exist_ok=True)
        
        env.update({
            'TMPDIR': termux_tmp,
            'TMP': termux_tmp,
            'TEMP': termux_tmp,
            'PYTHONPATH': os.environ.get('PYTHONPATH', ''),
            'PATH': os.environ.get('PATH', ''),
        })
        
        new_config['env'] = env
        compatible_config['mcpServers'][server_name] = new_config
    
    return compatible_config

def create_termux_mcp_config() -> Optional[Dict[str, Any]]:
    """
    Crea una configuración MCP específica para Termux con servidores básicos.
    """
    termux_tmp = os.path.expanduser('~/tmp')
    if not os.path.exists(termux_tmp):
        os.makedirs(termux_tmp, exist_ok=True)
    
    # Configuración básica que funciona en Termux
    config = {
        "mcpServers": {
            "mcp-requests": {
                "command": "python",
                "args": ["-m", "mcp_requests"],
                "env": {
                    "TMPDIR": termux_tmp,
                    "TMP": termux_tmp,
                    "TEMP": termux_tmp,
                },
                "transport": "stdio"
            }
        }
    }
    
    # Verificar e instalar mcp-requests si es necesario
    if not check_mcp_package_installed('mcp_requests'):
        logger.info("mcp-requests not found, attempting to install...")
        if install_mcp_package('mcp-requests'):
            return config
        else:
            logger.warning("Could not install mcp-requests, returning empty config")
            return {"mcpServers": {}}
    
    return config

def apply_termux_workaround(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aplica el workaround de Termux a la configuración MCP.
    """
    if not (is_termux() or is_android()):
        logger.info("Not running on Termux/Android, using original config")
        return config
    
    logger.info("Detected Termux/Android environment, applying workaround...")
    
    try:
        # Intentar convertir la configuración existente
        compatible_config = get_termux_compatible_config(config)
        
        # Si no hay servidores activos, usar configuración básica
        if not compatible_config.get('mcpServers'):
            logger.info("No compatible servers found, using basic Termux config")
            compatible_config = create_termux_mcp_config()
        
        logger.info(f"Termux workaround applied. Active servers: {list(compatible_config.get('mcpServers', {}).keys())}")
        return compatible_config
        
    except Exception as e:
        logger.error(f"Error applying Termux workaround: {e}")
        # Fallback a configuración básica
        return create_termux_mcp_config() or {"mcpServers": {}}

def setup_termux_environment():
    """
    Configura el entorno de Termux para MCP.
    """
    if not (is_termux() or is_android()):
        return
    
    logger.info("Setting up Termux environment for MCP...")
    
    # Crear directorio temporal
    termux_tmp = os.path.expanduser('~/tmp')
    if not os.path.exists(termux_tmp):
        os.makedirs(termux_tmp, exist_ok=True)
        logger.info(f"Created temporary directory: {termux_tmp}")
    
    # Configurar variables de entorno
    os.environ['TMPDIR'] = termux_tmp
    os.environ['TMP'] = termux_tmp
    os.environ['TEMP'] = termux_tmp
    
    logger.info("Termux environment setup completed")