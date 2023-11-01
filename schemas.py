from pydantic import BaseModel, Field
from typing import List, Optional

class EtudiantBase(BaseModel):
    prenom: str = Field(..., example="John", title="Prénom de l'étudiant")
    nom: str = Field(..., example="Doe", title="Nom de l'étudiant")
    pays: str = Field(..., example="Male", title="pays d'origine de l'étudiant")
    sexe: str = Field(..., example="Male", title="Sexe de l'étudiant")
    moyenne: Optional[float] = Field(None, example=15.5, title="Moyenne de l'étudiant")
    universite_id: int = Field(..., example=1, title="ID de l'université à laquelle l'étudiant appartient")
    
    class Config:
        orm_mode = True


class UniversiteBase(BaseModel):
    universite: str = Field(..., example="Université Paris-Dauphine", title="Nom de l'université")
    rang: int = Field(..., example="1", title="rang de l'université au classement de Shanghai 2020")
    pays: str = Field(..., example="France", title="Pays de l'université")
    iso: str = Field(..., example="FR", title="Code ISO 2 de l'universite")
    etudiants_urls: List[str] = []
    
    class Config:
        orm_mode = True


class EtudiantUpdate(BaseModel):
    prenom: Optional[str] = Field(example="John", title="Prénom de l'étudiant")
    moyenne: Optional[float] = Field(None, example=15.5, title="Moyenne de l'étudiant")
    universite_id: Optional[int] = Field(None, example=1, title="ID de l'université à laquelle l'étudiant appartient")

