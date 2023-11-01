-- Active: 1678634787669@@127.0.0.1@3306@api
CREATE TABLE Universite (
  id INT AUTO_INCREMENT,
  universite VARCHAR(255),
  rang INT,
  pays VARCHAR(50),
  iso VARCHAR(10),
  PRIMARY KEY (id)
);


CREATE TABLE Etudiant (
	id INT AUTO_INCREMENT,
	prenom VARCHAR(50),
	nom VARCHAR(50),
	pays VARCHAR(50),
	sexe VARCHAR(50),
	moyenne DECIMAL(4,2),
	universite_id INT,
	FOREIGN KEY (universite_id) REFERENCES Universite(id),
	PRIMARY KEY (id)
);