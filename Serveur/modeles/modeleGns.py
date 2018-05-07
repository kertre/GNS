#!/usr/bin/python
# -*- coding: utf-8 -*-


import mysql.connector



connexionBD = None

def getConnexionBD() :
	global connexionBD
	try :
		if connexionBD == None :
			connexionBD = mysql.connector.connect(
					host = 'localhost' ,
					user = 'root' ,
					password = 'azerty' ,
					database = 'gns'
				)
		return connexionBD
	except :
		return None


def seConnecter( nomJoueur , mdpJoueur ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requeteConnexion = '''
				select numero_joueur , email_joueur
				from Joueur
				where nom_joueur = %s
				and mdp_joueur = %s
			'''
			
		requeteJoueurConnecte = '''
				update Joueur
				set connecte_joueur = True
				where nom_joueur = %s
			'''
			
		curseur.execute( requeteConnexion , ( nomJoueur , mdpJoueur ) )
		
		unTuple = curseur.fetchone()
		
		if unTuple != None :
			
			joueur = {}
			joueur[ 'numero_joueur' ] = unTuple[ 0 ]
			joueur[ 'nom_joueur' ] = nomJoueur
			joueur[ 'email_joueur' ] = unTuple[ 1 ]
			
			curseur.execute( requeteJoueurConnecte , ( nomJoueur , ) )
			connexionBD.commit()
			
			return joueur
			
		else :
			return None
			
	except :
		if connexionBD != None :
			print 'Connexion annulée'
			connexionBD.rollback()
			
		print "[seConnecter] Nok"
		
		return -1


def seDeconnecter( numeroJoueur ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requeteJoueurDeconnecte = '''
				update Joueur
				set connecte_joueur = False
				where numero_joueur = %s
			'''
			
		curseur.execute( requeteJoueurDeconnecte , ( numeroJoueur , ) )
		connexionBD.commit()
		
		return curseur.rowcount
			
			
	except :
		if connexionBD != None :
			print 'Connexion annulée'
			connexionBD.rollback()
			
		print "[seConnecter] Nok"
		
		return -1


def getPartie( numeroPartie ) :
	# A modifier (BD v2)
	try :
		curseur = getConnexionBD().cursor()
		
		requetePartie = '''
				select date_creation_partie
				from Partie
				where numero_partie = %s
			'''
			
		curseur.execute( requetePartie , ( numeroPartie , ) )
		
		unTuple = curseur.fetchone()
		
		if unTuple != None :
			partie = {}
			partie[ 'numero_partie' ] = numeroPartie
			partie[ 'date_creation_partie' ] = unTuple[ 0 ]
			return partie
			
		else :
			return None
			
	except :
		return None
	


def getPions( numeroPartie ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requetePions = '''
			select numero_pion , est_roi , ligne_pion , colonne_pion , couleur_pion
			from Pion
			where numero_partie = %s
			'''
			
		curseur.execute( requetePions , ( numeroPartie , ) )

		lesPions = []
		
		for unTuple in curseur :
			unPion = {}
			unPion[ 'numero_pion' ] = unTuple[ 0 ]
			unPion[ 'est_roi' ] = unTuple[ 1 ]
			unPion[ 'ligne_pion' ] = unTuple[ 2 ]
			unPion[ 'colonne_pion' ] = unTuple[ 3 ]
			unPion[ 'couleur_pion' ] = unTuple[ 4 ]
			
			lesPions.append( unPion )
			
		print lesPions
		return lesPions
			
	except :
		return None
	
	



def initierPartie( numJoueur , couleur ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requetePartie = '''
			insert into Partie(date_creation_partie,initiateur,suivant,couleur_initiateur,couleur_adversaire)
			values(CURRENT_DATE,%s,%s,%s,%s)
			'''

		requetePion = '''
			insert into Pion(numero_pion,est_roi,ligne_pion,colonne_pion,numero_partie,couleur_pion)
			values(%s,%s,%s,%s,%s,%s)
			'''
		
		#connexionBD.start_transaction()
		
		if couleur == 'N' :
			print 'Joueur est Noir'
			curseur.execute( requetePartie , ( numJoueur , numJoueur , 'N' , 'B' ) )
			print 'Ok'
		else :
			print 'Joueur est Bleu'
			curseur.execute( requetePartie , ( numJoueur , None , 'B' , 'N' ) )
			print 'Ok'
		
		numPartie = curseur.lastrowid
		
		source = open( 'data/pions.csv' , 'r' )
		source.readline()
		for unPion in source :
			couleur , numero , roi , ligne, colonne = unPion.rstrip().split(',')
			curseur.execute( requetePion , ( numero , roi , ligne , colonne , numPartie , couleur ) )
			
		source.close()
		
		connexionBD.commit()
		
		curseur.close()
		
		return numPartie

	except :
		if connexionBD != None :
			print 'Création annulée'
			connexionBD.rollback()
			
		print "[creerPartie] Nok"
		
		return -1
		
		
def rejoindrePartie( numJoueur , numPartie , couleur ) :
	
	try :
		curseur = getConnexionBD().cursor()
		
		requetePartieAdversaire = '''
			update Partie
			set adversaire = %s
			where numero_partie = %s
			'''
			
		requetePartieSuivant = '''
			update Partie
			set suivant = %s
			where numero_partie = %s
			'''
			
		curseur.execute( requetePartieAdversaire , ( numJoueur , numPartie ) )
		
		if couleur == 'N' :
			curseur.execute( requetePartieSuivant , ( numJoueur , numPartie ) )
		
		connexionBD.commit()
		
		curseur.close()
		
		return numPartie

	except :
		if connexionBD != None :
			print 'Modification annulée'
			connexionBD.rollback()
			
		print "[rejoidnrePartie] Nok"
		
		return -1
	


def getMesPartiesEnAttente( numJoueur ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requeteParties = '''
			select Partie.numero_partie , Partie.date_creation_partie , 
				Couleur.numero_couleur , Couleur.nom_couleur
			from Partie
			inner join Opposer opp1
			on opp1.numero_partie = Partie.numero_partie
			inner join Joueur
			on opp1.numero_joueur = Joueur.numero_joueur
			inner join Couleur
			on opp1.numero_couleur = Couleur.numero_couleur
			where opp1.numero_partie in (
				select opp2.numero_partie 
				from Opposer opp2
				group by(opp2.numero_partie) 
				having count(*) = 1
			)
			and opp1.numero_joueur = %s 
			and Partie.vainqueur is null ;
			'''
		
		curseur.execute( requeteParties , ( numJoueur , ) )
		
		parties = []
		for unTuple in curseur :
			unePartie = {}
			unePartie[ 'numero' ] = unTuple[ 0 ]
			unePartie[ 'creation' ] = str(unTuple[ 1 ])
			unePartie[ 'numero_couleur' ] = unTuple[ 2 ]
			unePartie[ 'nom_couleur' ] = unTuple[ 3 ]
			parties.append( unePartie )
			
		return parties
			
	except :	
		return None
		
		
		
		
def getMesPartiesEnCours( numJoueur ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requeteParties = '''
			select Partie.numero_partie , Partie.date_creation_partie , 
				Couleur.numero_couleur , Couleur.nom_couleur ,
				Joueur.nom_joueur
			from Partie
			inner join Opposer opp1
			on opp1.numero_partie = Partie.numero_partie
			inner join Joueur
			on opp1.numero_joueur = Joueur.numero_joueur
			inner join Couleur
			on opp1.numero_couleur = Couleur.numero_couleur
			where opp1.numero_partie in (
				select opp2.numero_partie 
				from Opposer opp2
				where opp2.numero_joueur = %s
			)
			and opp1.numero_joueur <> %s 
			and Partie.vainqueur is null ;
			'''
		
		curseur.execute( requeteParties , ( numJoueur , numJoueur ) )
		
		parties = []
		for unTuple in curseur :
			unePartie = {}
			unePartie[ 'numero' ] = unTuple[ 0 ]
			unePartie[ 'creation' ] = str(unTuple[ 1 ])
			unePartie[ 'numero_couleur' ] = unTuple[ 2 ]
			unePartie[ 'nom_couleur' ] = unTuple[ 3 ]
			unePartie[ 'nom_joueur' ] = unTuple[ 4 ]
			parties.append( unePartie )
			
		return parties
			
	except :	
		return None

def getPartiesEnAttente( numJoueur ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requeteParties = '''
			select Partie.numero_partie , Partie.date_creation_partie , 
				Couleur.numero_couleur , Couleur.nom_couleur ,
				Joueur.nom_joueur
			from Partie
			inner join Opposer opp1
			on opp1.numero_partie = Partie.numero_partie
			inner join Joueur
			on opp1.numero_joueur = Joueur.numero_joueur
			inner join Couleur
			on opp1.numero_couleur = Couleur.numero_couleur
			where opp1.numero_partie in (
				select opp2.numero_partie 
				from Opposer opp2
				group by(opp2.numero_partie) 
				having count(*) = 1
			)
			and opp1.numero_joueur <> %s 
			and Partie.vainqueur is null ;
			'''
		
		curseur.execute( requeteParties , ( numJoueur , ) )
		
		parties = []
		for unTuple in curseur :
			unePartie = {}
			unePartie[ 'numero' ] = unTuple[ 0 ]
			unePartie[ 'creation' ] = str(unTuple[ 1 ])
			unePartie[ 'numero_couleur' ] = unTuple[ 2 ]
			unePartie[ 'nom_couleur' ] = unTuple[ 3 ]
			unePartie[ 'nom_joueur' ] = unTuple[ 4 ]
			parties.append( unePartie )
			
		return parties
			
	except :	
		return None		


		
def getParties() :
	try :
		curseur = getConnexionBD().cursor()
		
		requeteParties = '''
			select numero_partie , date_creation_partie
			from Partie
			'''
		
		curseur.execute( requeteParties , () )
		
		parties = []
		for unTuple in curseur :
			unePartie = {}
			unePartie[ 'numero' ] = unTuple[ 0 ]
			unePartie[ 'creation' ] = str(unTuple[ 1 ])
			parties.append( unePartie )
			
		return parties
			
	except :	
		return None
		
		
