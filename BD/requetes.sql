// Toutes les parties

select numero_partie , date_creation_partie ,
	j1.numero_joueur as 'nunInit', j1.nom_joueur as 'nomInit', p.couleur_initiateur as 'coulInit',
	j2.numero_joueur as 'numAdv', j2.nom_joueur as 'nomAdv' , p.couleur_adversaire as 'coulAdv',
	p.suivant , p.vainqueur
from Partie p
inner join Joueur j1 on p.initiateur = j1.numero_joueur
inner join Joueur j2 on p.adversaire = j2.numero_joueur
where p.adversaire is not null

union

select numero_partie , date_creation_partie ,
	j1.numero_joueur as 'numero_initiateur', j1.nom_joueur as 'nom_initiateur', p.couleur_initiateur as 'coulInit', 
	null, null,  p.couleur_adversaire as 'coulAdv',
	p.suivant , p.vainqueur
from Partie p
inner join Joueur j1 on p.initiateur = j1.numero_joueur
where p.adversaire is not null

;


// Mes parties en attente (Joueur 5)

select numero_partie , date_creation_partie ,
	couleur_initiateur
from Partie
where initiateur = 5
and adversaire is null ;


// Mes parties en cours (Joueur 5)

select numero_partie , date_creation_partie ,
	p.couleur_initiateur as 'coulInit',
	j.numero_joueur as 'numAdv', j.nom_joueur as 'nomAdv' , p.couleur_adversaire as 'coulAdv',
	p.suivant
from Partie p
inner join Joueur j on p.adversaire = j.numero_joueur
where p.adversaire is not null
and p.vainqueur is null
and ( p.initiateur = 5  or p.adversaire = 5 ) ;







