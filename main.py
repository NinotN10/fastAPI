from fastapi import FastAPI, HTTPException, Depends, Request, Query
from sqlalchemy.orm import Session, sessionmaker, joinedload
from sqlalchemy import create_engine
from typing import List, Optional
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder

from database import Universite, Etudiant, Base, DATABASE_URL
from schemas import UniversiteBase, EtudiantBase, EtudiantUpdate

app = FastAPI(debug=True)

DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/api"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """
    Redirige vers la documentation Swagger UI
    """
    response = RedirectResponse(url="/redoc")
    return response



@app.get("/universites/", response_model=List[UniversiteBase])
def lister_universites(
    pays: Optional[str] = Query(None, title="Pays de l'université"),
    iso: Optional[str] = Query(None, title="Code ISO 2 du pays"),
    skip: int = Query(0, ge=0, title="Nombre d'enregistrements à ignorer"),
    limit: int = Query(50, ge=1, title="Nombre maximum d'enregistrements à renvoyer"),
    db: Session = Depends(get_db),
):
    """
    Liste toutes les universités
    """
    query = db.query(Universite).options(joinedload(Universite.etudiants))
    
    if pays:
        query = query.filter(Universite.pays == pays)
    if iso:
        query = query.filter(Universite.iso == iso)
    
    universites = query.offset(skip).limit(limit).all()
    
    for universite in universites:
        universite.etudiants_urls = [f"http://localhost:8000/etudiant/{etudiant.id}" for etudiant in universite.etudiants]
    return universites






@app.get("/universite/{universite_id}", response_model=UniversiteBase)
def lire_universite(universite_id: int, db: Session = Depends(get_db)):
    """
    Récupère une université par son identifiant
    """
    universite = db.query(Universite).filter(Universite.id == universite_id).first()
    if not universite:
        raise HTTPException(status_code=404, detail="Université non trouvée")
    etudiants = db.query(Etudiant).filter(Etudiant.universite_id == universite_id).all()
    universite.etudiants_urls = [f"http://localhost:8000/etudiant/{etudiant.id}" for etudiant in etudiants]
    return universite




# exemple pour l'examen
# @app.get("/etudiants/", response_model=List[EtudiantBase])
# def lister_etudiants(db: Session = Depends(get_db)):
#     """
#     Liste tous les étudiants
#     """
#     etudiants = db.query(Etudiant).all()
#     return etudiants

@app.get("/etudiants/", response_model=List[EtudiantBase])
def lister_etudiants(
    nom: Optional[str] = Query(None),
    prenom: Optional[str] = Query(None),
    iso: Optional[str] = Query(None, title="Code ISO 2 du pays"),
    sexe: Optional[str] = Query(None),
    moyenne: Optional[float] = Query(None),
    moyenne_operation: Optional[str] = Query(None, title="Opération de comparaison pour la moyenne (lt, le, eq, ge, gt)"),
    db: Session = Depends(get_db),
):
    """
    Liste tous les étudiants
    """
    query = db.query(Etudiant).join(Universite)
    
    if nom:
        query = query.filter(Etudiant.nom == nom)
    if prenom:
        query = query.filter(Etudiant.prenom == prenom)
    if sexe:
        query = query.filter(Etudiant.sexe == sexe)
    if moyenne is not None and moyenne_operation:
        if moyenne_operation == "lt":
            query = query.filter(Etudiant.moyenne < moyenne)
        elif moyenne_operation == "le":
            query = query.filter(Etudiant.moyenne <= moyenne)
        elif moyenne_operation == "eq":
            query = query.filter(Etudiant.moyenne == moyenne)
        elif moyenne_operation == "ge":
            query = query.filter(Etudiant.moyenne >= moyenne)
        elif moyenne_operation == "gt":
            query = query.filter(Etudiant.moyenne > moyenne)
    if iso:
        query = query.filter(Universite.iso == iso)

    etudiants = query.all()
    return etudiants





@app.post("/etudiant/", response_model=EtudiantBase)
def create_etudiant(etudiant: EtudiantBase, db: Session = Depends(get_db)):
    """
    Crée un nouvel étudiant
    """
    nouvel_etudiant = Etudiant(**etudiant.dict())
    db.add(nouvel_etudiant)
    db.commit()
    db.refresh(nouvel_etudiant)
    return nouvel_etudiant





@app.get("/etudiant/{etudiant_id}", response_model=EtudiantBase)
def lire_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    """
    Récupère un étudiant par son identifiant
    """
    etudiant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
    if not etudiant:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return etudiant







@app.put("/etudiant/{etudiant_id}", response_model=EtudiantBase)
def mettre_a_jour_etudiant(etudiant_id: int, etudiant: EtudiantUpdate, db: Session = Depends(get_db)):
    """
    Met à jour un étudiant par son identifiant
    """
    etudiant_existant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
    if not etudiant_existant:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")

    etudiant_data = jsonable_encoder(etudiant)
    for key, value in etudiant_data.items():
        if value is not None:
            setattr(etudiant_existant, key, value)

    db.commit()
    db.refresh(etudiant_existant)
    
    return etudiant_existant








@app.delete("/etudiant/{etudiant_id}", status_code=204)
def supprimer_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    """
    Supprime un étudiant par son identifiant
    """
    etudiant_existant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
    if not etudiant_existant:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")

    db.delete(etudiant_existant)
    db.commit()
    return PlainTextResponse(content=f"Étudiant avec l'ID {etudiant_id} supprimé avec succès")

