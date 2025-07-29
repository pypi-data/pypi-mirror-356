"""
Moduł dostawców dla biblioteki webload.
"""

from typing import Dict, Type, List

from webload.providers.base import BaseProvider

# Słownik zarejestrowanych dostawców
PROVIDERS: Dict[str, Type[BaseProvider]] = {}

def register_provider(name: str, provider_class: Type[BaseProvider]) -> None:
    """
    Rejestruje dostawcę w systemie.
    
    Args:
        name: Nazwa dostawcy
        provider_class: Klasa dostawcy
    """
    PROVIDERS[name.lower()] = provider_class

def get_provider_class(name: str) -> Type[BaseProvider]:
    """
    Zwraca klasę dostawcy na podstawie nazwy.
    
    Args:
        name: Nazwa dostawcy
        
    Returns:
        Klasa dostawcy
        
    Raises:
        ValueError: Jeśli dostawca o podanej nazwie nie istnieje
    """
    name = name.lower()
    if name not in PROVIDERS:
        raise ValueError(f"Dostawca '{name}' nie jest zarejestrowany")
    return PROVIDERS[name]

def get_all_providers() -> List[str]:
    """
    Zwraca listę wszystkich zarejestrowanych dostawców.
    
    Returns:
        Lista nazw dostawców
    """
    return list(PROVIDERS.keys())

# Importowanie wszystkich dostawców
from webload.providers.wise import WiseProvider
from webload.providers.paypal import PayPalProvider
from webload.providers.openai import OpenAIProvider
from webload.providers.aftermarket import AftermarketProvider
from webload.providers.ddregistrar import DDRegistrarProvider
from webload.providers.premium import PremiumProvider
from webload.providers.namecheap import NamecheapProvider
from webload.providers.fiverr import FiverrProvider
from webload.providers.ovh import OVHProvider
from webload.providers.ionos import IONOSProvider
from webload.providers.strato import STRATOProvider
from webload.providers.sav import SAVProvider
from webload.providers.spaceship import SpaceshipProvider
from webload.providers.meetup import MeetupProvider
from webload.providers.adobe import AdobeProvider
from webload.providers.godaddy import GoDaddyProvider
from webload.providers.afternic import AfternicProvider
from webload.providers.scribd import ScribdProvider
from webload.providers.envato import EnvatoProvider
from webload.providers.proton import ProtonProvider
from webload.providers.linkedin import LinkedInProvider

# Rejestracja dostawców
register_provider("wise", WiseProvider)
register_provider("paypal", PayPalProvider)
register_provider("openai", OpenAIProvider)
register_provider("aftermarket", AftermarketProvider)
register_provider("ddregistrar", DDRegistrarProvider)
register_provider("premium", PremiumProvider)
register_provider("namecheap", NamecheapProvider)
register_provider("fiverr", FiverrProvider)
register_provider("ovh", OVHProvider)
register_provider("ionos", IONOSProvider)
register_provider("strato", STRATOProvider)
register_provider("sav", SAVProvider)
register_provider("spaceship", SpaceshipProvider)
register_provider("meetup", MeetupProvider)
register_provider("adobe", AdobeProvider)
register_provider("godaddy", GoDaddyProvider)
register_provider("afternic", AfternicProvider)
register_provider("scribd", ScribdProvider)
register_provider("envato", EnvatoProvider)
register_provider("proton", ProtonProvider)
register_provider("linkedin", LinkedInProvider)

__all__ = [
    "BaseProvider",
    "register_provider",
    "get_provider_class",
    "get_all_providers",
    "PROVIDERS",
    "WiseProvider",
    "PayPalProvider",
    "OpenAIProvider",
    "AftermarketProvider",
    "DDRegistrarProvider",
    "PremiumProvider",
    "NamecheapProvider",
    "FiverrProvider",
    "OVHProvider",
    "IONOSProvider",
    "STRATOProvider",
    "SAVProvider",
    "SpaceshipProvider",
    "MeetupProvider",
    "AdobeProvider",
    "GoDaddyProvider",
    "AfternicProvider",
    "ScribdProvider",
    "EnvatoProvider",
    "ProtonProvider",
    "LinkedInProvider"
]
