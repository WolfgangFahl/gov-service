"""
Created on 2026-03-14

@author: wf
"""
from dataclasses import dataclass

import govservice


@dataclass
class Version:
    """
    Version information for GOV-Service
    """
    name: str = "gov-service"
    version: str = "0.0.1"
    date: str = "2026-03-14"
    updated: str = "2026-03-14"
    description: str = "A local Python service acting as an alternative GOV server"
    authors: str = "Wolfgang Fahl"
    doc_url: str = "https://gov-wiki.genealogy.net/index.php/GOV-Service/Plan"
    chat_url: str = "https://github.com/WolfgangFahl/gov-service/discussions"
    cm_url: str = "https://github.com/WolfgangFahl/gov-service"
