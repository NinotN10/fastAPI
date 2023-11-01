from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship


DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/api"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Universite(Base):
    __tablename__ = "Universite"

    id = Column(Integer, primary_key=True, index=True)
    universite = Column(String, index=True)
    rang = Column(Integer)
    pays = Column(String, index=True)
    iso = Column(String, index=True)

    etudiants = relationship("Etudiant", back_populates="universite")

class Etudiant(Base):
    __tablename__ = "Etudiant"

    id = Column(Integer, primary_key=True, index=True)
    prenom = Column(String)
    nom = Column(String)
    pays = Column(String, index=True)
    sexe = Column(String)
    moyenne = Column(Float, index=True)

    universite_id = Column(Integer, ForeignKey("Universite.id"))
    universite = relationship("Universite", back_populates="etudiants")

Base.metadata.create_all(bind=engine)
