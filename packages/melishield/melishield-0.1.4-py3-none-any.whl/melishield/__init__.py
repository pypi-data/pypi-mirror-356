"""
MeliShield - Una librería que saluda con estilo
"""

def _print_giant_hello():
    """Imprime un saludo gigante"""
    hello_art = """
    
██╗  ██╗ ██████╗ ██╗      █████╗ 
██║  ██║██╔═══██╗██║     ██╔══██╗
███████║██║   ██║██║     ███████║
██╔══██║██║   ██║██║     ██╔══██║
██║  ██║╚██████╔╝███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝

    ¡MeliShield te saluda! 🛡️
    """
    print(hello_art)

# Ejecutar el saludo al importar el paquete
_print_giant_hello()

# Funciones principales del paquete
def saludar(nombre="Mundo"):
    """Función que saluda de manera personalizada"""
    _print_giant_hello()
    return f"¡Hola {nombre} desde MeliShield!"

def proteger():
    """Función que simula protección"""
    _print_giant_hello()
    return "🛡️ MeliShield está activo y protegiendo tu código"

def version():
    """Devuelve la versión del paquete"""
    _print_giant_hello()
    return "0.1.4"

# Exportar las funciones principales
__all__ = ['saludar', 'proteger', 'version']
__version__ = "0.1.4" 