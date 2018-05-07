#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
from modeles import modeleGns

app = Flask( __name__ )

@app.route( '/' , methods = [ 'GET' ] )
def accueillir() :
	return 'GNS'
	
	
@app.route( '/joueurs/seconnecter/<nomJoueur>/<mdpJoueur>' , methods = [ 'PUT' ] )
def seConnecter( nomJoueur , mdpJoueur ) :
	#infosJoueur = json.loads( request.data )
	
	print "SeConnecter> " + nomJoueur + " " + mdpJoueur
	joueur = modeleGns.seConnecter( nomJoueur , mdpJoueur )
	
	print joueur
	
	reponse = make_response( '' )
	reponse.mimetype = 'text/plain'
	
	if joueur != None :		
		reponse.status_code = 200
		
	else :
		reponse.status_code = 404
	
	return reponse
	

@app.route( '/joueurs/<numeroJoueur>/sedeconnecter' , methods = [ 'PUT' ] )
def seDeconnecter( numeroJoueur ) :
	reponse = make_response( '' )
	reponse.mimetype = 'text/plain'
	
	resultat = modeleGns.seDeconnecter( numeroJoueur )
	
	if resultat == 1 :
		reponse.status_code = 200
	else :
		reponse.status_code = 404
	
	return reponse


@app.route( '/parties/<numeroPartie>/pions' , methods = [ 'GET' ] )
def getPions( numeroPartie ) :
	print '[getPions]'
	lesPions = modeleGns.getPions( numeroPartie )
	
	if lesPions != None :
		corpsReponse = json.dumps( lesPions )
		print corpsReponse
		reponse = make_response( corpsReponse )
		reponse.mimetype = 'application/json'
		reponse.status_code = 200
		
	else :
		reponse = make_response( '' )
		reponse.mimetype = 'text/plain'
		reponse.status_code = 404
		
	return reponse
	
@app.route( '/parties/<numeroPartie>' , methods = [ 'GET' ])
def getPartie( numeroPartie ) :
	print '[getPartie]'
	unePartie = modeleGns.getPartie( numeroPartie )
	
	if unePartie != None :
		corpsReponse = json.dumps( unePartie )
		print unePartie
		reponse = make_response( unePartie )
		reponse.mimetype = 'application/json'
		reponse.status_code = 200
		
	else :
		reponse = make_response( '' )
		reponse.mimetype = 'text/plain'
		reponse.status_code = 404
		
	return reponse
	



	
@app.route( '/joueurs/<numJoueur>/parties/<couleur>' , methods = [ 'POST' ] )
def initierPartie( numJoueur , couleur ) :
	print '[initierPartie]'
	reponse = make_response( '' )
	reponse.mimetype = 'text/plain'
	numPartie = modeleGns.initierPartie( numJoueur , couleur )
	if numPartie != -1 :
		reponse.status_code = 200
	else :
		reponse.status_code = 500
	return reponse
	

@app.route( '/joueurs/<numJoueur>/parties/<numPartie>/<couleur>' , methods = [ 'PUT' ] )
def rejoindrePartie( numJoueur , numPartie , couleur ) :
	print '[rejoindrePartie]'
	reponse = make_response( '' )
	reponse.mimetype = 'text/plain'
	numPartie = modeleGns.rejoindrePartie( numJoueur , numPartie , couleur )
	if numPartie != -1 :
		reponse.status_code = 201
		reponse.headers['Location'] = '/parties/' + str( numPartie )
	else :
		reponse.status_code = 500
	return reponse



@app.route( '/joueurs/<numJoueur>/mesparties/enattente' , methods = [ 'GET' ] )
def getMesPartiesEnAttente( numJoueur ) :
	print '[getMesPartiesEnAttente]'
	lesParties = modeleGns.getMesPartiesEnAttente( numJoueur )

	if lesParties != None :
		corpsReponse = json.dumps( lesParties )
		reponse = make_response( corpsReponse )
		reponse.mimetype = 'application/json'
		reponse.status_code = 200
		
	else :
		reponse = make_response( '' )
		reponse.mimetype = 'text/plain'
		reponse.status_code = 404
		
	return reponse


@app.route( '/joueurs/<numJoueur>/parties/encours' , methods = [ 'GET' ] )
def getMesPartiesEnCours( numJoueur ) :
	print '[getPartiesEnCours]'
	lesParties = modeleGns.getMesPartiesEnCours( numJoueur )

	if lesParties != None :
		corpsReponse = json.dumps( lesParties )
		reponse = make_response( corpsReponse )
		reponse.mimetype = 'application/json'
		reponse.status_code = 200
		
	else :
		reponse = make_response( '' )
		reponse.mimetype = 'text/plain'
		reponse.status_code = 404
		
	return reponse



@app.route( '/parties' , methods = [ 'GET' ] )
def getParties() :
	print '[listerParties]'
	
	lesParties = modeleGns.getParties()

	if lesParties != None :
		corpsReponse = json.dumps( lesParties )
		reponse = make_response( corpsReponse )
		reponse.mimetype = 'application/json'
		reponse.status_code = 200
		
	else :
		reponse = make_response( '' )
		reponse.mimetype = 'text/plain'
		reponse.status_code = 404
		
	return reponse



@app.route( '/parties/enattente/joueurs/<numJoueur>' )
def getPartiesEnAttente( numJoueur ) :
	print '[listerParties]'
	
	lesParties = modeleGns.getPartiesEnAttente()

	if lesParties != None :
		corpsReponse = json.dumps( lesParties )
		reponse = make_response( corpsReponse )
		reponse.mimetype = 'application/json'
		reponse.status_code = 200
		
	else :
		reponse = make_response( '' )
		reponse.mimetype = 'text/plain'
		reponse.status_code = 404
		
	return reponse



if __name__ == '__main__' :
	app.run( debug = True , host = '0.0.0.0' , port = 5000 )
