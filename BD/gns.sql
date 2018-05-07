drop database if exists gns ;

create database gns default character set utf8 default collate utf8_general_ci ;
	
use gns ;


create table Joueur(
	numero_joueur int(11) auto_increment not null ,
	nom_joueur varchar(25) not null unique ,
	mdp_joueur varchar(25) not null ,
	email_joueur varchar(50) not null unique ,
	connecte_joueur bool default False ,
	primary key(numero_joueur) ,
	unique(email_joueur)
) ENGINE = InnoDB ;

create table Partie(
	numero_partie int(11) auto_increment not null ,
	date_creation_partie date not null ,
	initiateur int not null ,
	adversaire int ,
	vainqueur int ,
	suivant int ,
	couleur_initiateur char(1) not null ,
	couleur_adversaire char(2) not null ,
	primary key(numero_partie)
) ENGINE = InnoDB ;


create table Pion(
	numero_pion int(2) not null ,
	est_roi bool ,
	ligne_pion int(2) not null ,
	colonne_pion int(2) not null ,
	numero_partie int not null ,
	couleur_pion char(1) not null ,
	primary key(numero_pion,numero_partie,couleur_pion)
) ENGINE = InnoDB ;


create table Tour (
	numero_tour int(11) auto_increment not null ,
	action_tour varchar(40) ,
	dateheure_tour datetime ,
	numero_joueur int ,
	numero_partie int ,
	primary key( numero_tour , numero_partie )
) ENGINE = InnoDB ;

alter table Partie add constraint FK_Partie_initiateur foreign key(initiateur) references Joueur(numero_joueur) ;
alter table Partie add constraint FK_Partie_adversaire foreign key(adversaire) references Joueur(numero_joueur) ;
alter table Partie add constraint FK_Partie_vainqueur foreign key(vainqueur) references Joueur(numero_joueur) ;
alter table Partie add constraint FK_Partie_suivant foreign key(suivant) references Joueur(numero_joueur) ;

alter table Tour add constraint FK_Tour_numero_joueur foreign key(numero_joueur) references Joueur(numero_joueur) ;
alter table Tour add constraint FK_Tour_numero_partie foreign key(numero_partie) references Partie(numero_partie) ;

alter table Pion add constraint FK_Pion_numero_partie foreign key(numero_partie) references Partie(numero_partie) ;


insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('bba','azerty','bechir.ba.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('ewen','azerty','ewen.prigent.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('amal','azerty','amal.hecker.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('reda','azerty','reda.laroussi.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('owen','azerty','owen.ancelot.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('imane','azerty','imane.benachour.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('david','azerty','david.corrochano.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('ines','azerty','ines.dasilva.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('alice','azerty','alice.gilles.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('nicolas','azerty','nicolas.mazaud.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('seb','azerty','sebastien.neret.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('nitharsan','azerty','nitharsan.nimala.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('adekola','azerty','adekola.olubi.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('daria','azerty','daria.rychkova.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('hugo','azerty','hugo.sousamelo.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('johnny','azerty','johnny.tomburello.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('charlotte','azerty','charlotte.picois.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('driss','azerty','driss.belaroussi.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('aicha','azerty','aicha.mehdi.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('ilona','azerty','ilona.lebrun.sio@gmail.com') ;
insert into Joueur(nom_joueur,mdp_joueur,email_joueur) values('leo','azerty','lionel.romain.sio@gmail.com') ;

insert into Partie(date_creation_partie,initiateur,adversaire,vainqueur,suivant,couleur_initiateur,couleur_adversaire) 
			values(CURRENT_DATE,1,NULL,NULL,1,'N','B') ;
			
insert into Partie(date_creation_partie,initiateur,adversaire,vainqueur,suivant,couleur_initiateur,couleur_adversaire) 
			values(CURRENT_DATE,1,2,NULL,2,'B','N') ;

insert into Partie(date_creation_partie,initiateur,adversaire,vainqueur,suivant,couleur_initiateur,couleur_adversaire) 
			values(CURRENT_DATE,2,NULL,NULL,2,'N','B') ;
			
insert into Partie(date_creation_partie,initiateur,adversaire,vainqueur,suivant,couleur_initiateur,couleur_adversaire) 
			values(CURRENT_DATE,10,NULL,NULL,10,'N','B') ;
			











