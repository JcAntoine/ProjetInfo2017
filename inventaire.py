# -*- coding: UTF-8 -*-

import sys
import pygame
from pygame.locals import *
clock = pygame.time.Clock()


#personnages = [ string nom_personnage,
#[	[string nom_img_sur_map, transparence],
#	[string nom_img_sur_combat, transparence], # transparence : bool + r, g, b
#	[string nom_img_dialogues, transparence]
#],
#[ objets_equipes ],   # tuple : pour chaque emplacement, l'id d'un objet -> -1 = rien
#( caracs ) ]	      # tuple : pour chaque carac, deux nombres : max et actuel
def affiche_Equipement(fond_inventaire,fenetre,itemFinal,personnage,objets) :
    fenetre.blit(fond_inventaire,(0,0))
    objetsPers = personnage[2]
    for idAffichage,idObjet in enumerate(objetsPers) :
        if idObjet != -1 :
            #affichage de l'objet
            image =  itemFinal.subsurface(objets[idObjet][5][2]*32,objets[idObjet][5][1]*32,32,32)
            image = pygame.transform.scale(image,(64,64))
            fenetre.blit(image,(262+108*(idAffichage%2),48+83*(idAffichage//2)))
    pygame.display.update(pygame.Rect(259,47,181,341)) #259 et non 260 pour enlever le cadre

def trouveCaseEq(coordonnes) : #on veut trouver la case sélectionnée ou survolée de l'équipement
    x, y = coordonnes
    for idC in range (8) :
        if idC%2 == 0 : #sur la colonne de gauche
            if 260 <= x <= 330 and 48+83*(idC//2) <= y <= 112+83*(idC//2) :
                return idC
        else :
            if 370 <= x <= 440 and 48+83*(idC//2) <= y <= 112+83*(idC//2) :
                return idC
    return -1 #aucune case trouvée

#inventaire = [nb_objet dans le sac pour chaque id_objet]
def affiche_dansInventaire(font_inventaire,fenetre,itemFinal,inventaire,objets) :
    policevs = pygame.font.Font("Polices/arial.TTF",15)
    fenetre.blit(font_inventaire,(0,0))
    idAffichage = 0
    for idObjet,nbObjet in enumerate (inventaire) :
        if nbObjet != 0 :
            #affichage de l'objet
            fenetre.blit(itemFinal,(553+38*(idAffichage%6),66+36*(idAffichage//6)),(objets[idObjet][5][2]*32,objets[idObjet][5][1]*32,32,32))
            nb = policevs.render(str(nbObjet),True,pygame.Color(255,0,0))
            fenetre.blit(nb,(553+38*(idAffichage%6),66+36*(idAffichage//6)))
            idAffichage += 1
    pygame.display.update(pygame.Rect(552,65,301,371)) #552 et non 553 pour effacer le cadre

def trouveCaseInv(coordonnes) :
    x, y = coordonnes
    for idC in range (48) :
        if 553+38*(idC%6) <= x <= 585+38*(idC%6) and 66+36*(idC//6) <= y <= 98+36*(idC//6) :
            return idC
    return -1 #aucune case trouvée

def trouveIdObjet(inventaire,idCase) :
    idC = -1
    for idObjet,nbObjet in enumerate (inventaire) :
        if nbObjet != 0 :
            idC += 1
            if idCase == idC : #c'est l'objet qu'on cherche
                return idObjet
    return -1 #normalement n'arrive jamais

def majPers(fenetre,image) : #mise à jour de l'affichage en fonction du joueur sélectionné
    fenetre.blit(image,(0,0))
    pygame.display.update(pygame.Rect(0,0,155,300))

def equipementObjet(fenetre,sauvegarde,objets,idObjet,joueurSel) :
    typeObjet = objets[idObjet][0]
    personnage = sauvegarde[0][joueurSel]
    inventaire = sauvegarde[1]
    if typeObjet == 4 : #cas particulier de la bague, qui peut être équipée à deux endroits
        if personnage[2][3] == -1 :
            personnage[2][3] = idObjet
        elif personnage[2][7] == -1 :
            personnage[2][7] = idObjet
        else : #pour ajouter l'objet, on doit en enlever un autre
            idObjetRetire = personnage[2][7]
            personnage[2][7] = idObjet
            sauvegarde[1][idObjetRetire] += 1
        sauvegarde[1][idObjet] -= 1 #on retire l'objet de l'inventaire
    elif typeObjet == 1 or typeObjet == 2 or typeObjet == 3 or typeObjet == 5 or typeObjet == 6 or typeObjet == 7 : #les autres objets équipables
        if personnage[2][typeObjet-1] == -1 :
            personnage[2][typeObjet-1] = idObjet
        else : #pour ajouter l'objet, on doit en enlever un autre
            idObjetRetire =personnage[2][typeObjet-1]
            personnage[2][typeObjet-1] = idObjet
            sauvegarde[1][idObjetRetire] += 1
        sauvegarde[1][idObjet] -= 1 #on retire l'objet de l'inventaire
    else : #l'objet n'est pas équipable
        pass
    return sauvegarde

#sauvegarde = [personnages, inventaire, pnjs]
#personnages = [ string nom_personnage,
#[	[string nom_img_sur_map, transparence],
#	[string nom_img_sur_combat, transparence], # transparence : bool + r, g, b
#	[string nom_img_dialogues, transparence]
#],
#[ objets_equipes ],   # liste : pour chaque emplacement, l'id d'un objet -> -1 = rien
#( caracs ) ]	      # tuple : pour chaque carac, deux nombres : max et actuel
#inventaire = [nb_objet dans le sac pour chaque id_objet]
def inventaire(sauvegarde,objets) :
    #initialisations
    pygame.font.init()
    #création fenêtre
    fenetre = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Inventaire")
    #création fond
    fond_inventaire = pygame.image.load("Projets/images/inventaire/fond_defaut.png").convert()
    fond_inventaire = pygame.transform.scale(fond_inventaire,(800,600))
    fenetre.blit(fond_inventaire,(0,0))
    #initialisation des images
    imagesPerso = [pygame.image.load("Projets/images/inventaire/adrien.png").convert(),pygame.image.load("Projets/images/inventaire/trinity.png").convert(),pygame.image.load("Projets/images/inventaire/jc.png").convert()]
    majPers(fenetre,imagesPerso[0]) #par défaut, adrien est sélectionné
    cadreB = pygame.image.load("Projets/images/inventaire/cadre6666.png")
    cadreS = pygame.image.load("Projets/images/inventaire/cadre3434.png")
    itemFinal = pygame.image.load("Projets/images/inventaire/itemFinal2.png")
    pygame.display.flip()
    #création polices
    policeb = pygame.font.Font("Polices/ARBLANCA.TTF", 25)
    polices = pygame.font.Font("Polices/ARBLANCA.TTF", 18)
    policevs = pygame.font.Font("Polices/arial.TTF",15)
    #initialisation variables
    joueurSel = 0 #par défaut, adrien est sélectionnée
    continuer = True
    affiche_dansInventaire(fond_inventaire,fenetre,itemFinal,sauvegarde[1],objets)
    affiche_Equipement(fond_inventaire,fenetre,itemFinal,sauvegarde[0][joueurSel],objets)
    pygame.event.pump()
    while continuer:
        clock.tick(100) #permet de ne pas surcharger le processeur
        event = pygame.event.poll() #prend un événement dans la queue (potentiellement aucun)
        if event.type == QUIT: #si clic sur la croix rouge en haut à gauche
            continuer = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE: #si clic sur Echap
            continuer = False
        elif event.type == MOUSEMOTION :
            if 260 <= event.pos[0] < 450 : #on survole un équipement
                idCase = trouveCaseEq(event.pos)
                #vérifier que la case est équipée
                idObjet = sauvegarde[0][joueurSel][2][idCase]
                if idCase != -1 and idObjet != -1 : #on trouve une case et elle est équipée
                    #afficher le nom
                    nom = policeb.render(objets[idObjet][1],True,pygame.Color(220,220,220))
                    fenetre.blit(fond_inventaire,(0,0))
                    fenetre.blit(nom,(260,390))
                    pygame.display.update(pygame.Rect(260,390,180,110))
                else : #on ne survole plus rien
                    fenetre.blit(fond_inventaire,(0,0))
                    pygame.display.update(pygame.Rect(260,390,180,110))
            elif 560 <= event.pos[0] < 790 : #on survole un objet de l'inventaire
                idCase = trouveCaseInv(event.pos)
                #vérifier qu'il y a un objet sur la case
                if idCase != -1 and idCase < len(sauvegarde[1])-sauvegarde[1].count(0) : #on trouve une case et elle est remplie
                    idObjet = trouveIdObjet(sauvegarde[1],idCase)
                    #afficher le nom
                    nom = policeb.render(objets[idObjet][1],True,pygame.Color(220,220,220))
                    fenetre.blit(fond_inventaire,(0,0))
                    fenetre.blit(nom,(540,440))
                    pygame.display.update(pygame.Rect(540,440,250,140))
                else : #on ne survole plus rien
                    fenetre.blit(fond_inventaire,(0,0))
                    pygame.display.update(pygame.Rect(540,440,250,140))
            else : #on ne survole plus rien
                fenetre.blit(fond_inventaire,(0,0))
                pygame.display.update(pygame.Rect(260,390,180,110))
                pygame.display.update(pygame.Rect(540,440,250,140))
        elif event.type == MOUSEBUTTONDOWN :
            if 0 <= event.pos[0] < 150 : #zone de choix des joueurs
                if 0 <= event.pos[1] < 100 and joueurSel != 0 : #on sélectionne le joueur 0
                    joueurSel = 0
                    #mettre à jour le fond (partie gauche)
                    majPers(fenetre,imagesPerso[joueurSel])
                    #mise à jour de l'équipement
                    affiche_Equipement(fond_inventaire,fenetre,itemFinal,sauvegarde[0][0],objets)
                elif 100 <= event.pos[1] < 200 and joueurSel != 1 : #on sélectionne le joueur 1
                    joueurSel = 1
                    #mettre à jour le fond (partie gauche)
                    majPers(fenetre,imagesPerso[joueurSel])
                    #mise à jour de l'équipement
                    affiche_Equipement(fond_inventaire,fenetre,itemFinal,sauvegarde[0][1],objets)
                elif 200 <= event.pos[1] < 300 and joueurSel != 2 : #on sélectionne le joueur 2
                    joueurSel = 2
                    #mettre à jour le fond (partie gauche)
                    majPers(fenetre,imagesPerso[joueurSel])
                    #mise à jour de l'équipement
                    affiche_Equipement(fond_inventaire,fenetre,itemFinal,sauvegarde[0][2],objets)
            elif 150 <= event.pos[0] < 550 : #zone de l'équipement du joueur
                idCase = trouveCaseEq(event.pos)
                #vérifier que la case est équipée
                idObjet = sauvegarde[0][joueurSel][2][idCase]
                if idCase != -1 and idObjet != -1 : #la case est équipée
                    #afficher le nom, la description, le prix et mettre la case en surbrillance
                    fenetre.blit(fond_inventaire,(0,0))
                    image =  itemFinal.subsurface(objets[idObjet][5][2]*32,objets[idObjet][5][1]*32,32,32)
                    image = pygame.transform.scale(image,(64,64))
                    fenetre.blit(image,(262+108*(idCase%2),48+83*(idCase//2)))
                    fenetre.blit(cadreB,(261+108*(idCase%2),47+83*(idCase//2)))
                    pygame.display.update(pygame.Rect(261+108*(idCase%2),47+83*(idCase//2),66,66))
                    nom = policeb.render(objets[idObjet][1],True,pygame.Color(220,220,220))
                    description = polices.render(objets[idObjet][3],True,pygame.Color(220,220,220))
                    fenetre.blit(nom,(260,390))
                    fenetre.blit(description,(260,420))
                    #créer un bouton 'Retirer'
                    retirer = polices.render('Retirer',True,pygame.Color(220,220,220))
                    fenetre.blit(retirer,(380,480))
                    pygame.display.update(pygame.Rect(260,390,180,110))
                    #n'oublions pas de mettre le prix (pas au même endroit)
                    prix = policevs.render(str(objets[idObjet][2]),True,pygame.Color(220,220,220))
                    fenetre.blit(prix,(720,385))
                    pygame.display.update(pygame.Rect(720,385,70,15))
                    attente = True
                    while attente :
                        clock.tick(100) #permet de ne pas surcharger le processeur
                        event = pygame.event.poll() #prend un événement dans la queue (potentiellement aucun)
                        if event.type == QUIT: #si clic sur la croix rouge en haut à gauche
                            return sauvegarde, objets
                        elif event.type == KEYDOWN and event.key == K_ESCAPE: #si clic sur Echap
                            attente = False
                        elif event.type == MOUSEBUTTONDOWN :
                            if 380 <= event.pos[0] < 440 and 480 <= event.pos[1] < 500 :
                                #on retire l'équipement et on l'ajoute à l'inventaire
                                sauvegarde[0][joueurSel][2][idCase] = -1
                                sauvegarde[1][idObjet] += 1
                                attente = False
                            else :
                                attente = False
                    #on réactualise l'affichage
                    affiche_Equipement(fond_inventaire,fenetre,itemFinal,sauvegarde[0][joueurSel],objets)
                    affiche_dansInventaire(fond_inventaire,fenetre,itemFinal,sauvegarde[1],objets)
                    pygame.display.update(pygame.Rect(260,390,180,110)) #on efface les caractéristiques
                    pygame.display.update(pygame.Rect(720,385,70,15)) #et le prix
            elif 550 <= event.pos[0] : #zone de l'inventaire commun
                idCase = trouveCaseInv(event.pos)
                #vérifier qu'il y a un objet sur la case
                if idCase != -1 and idCase < len(sauvegarde[1])-sauvegarde[1].count(0) : #on trouve une case et elle est remplie
                    idObjet = trouveIdObjet(sauvegarde[1],idCase)
                    #afficher le nom, la description, le prix et mettre la case en surbrillance
                    fenetre.blit(itemFinal,(553+38*(idCase%6),66+36*(idCase//6)),(objets[idObjet][5][2]*32,objets[idObjet][5][1]*32,32,32))
                    nb = policevs.render(str(sauvegarde[1][idObjet]),True,pygame.Color(255,0,0))
                    fenetre.blit(nb,(553+38*(idCase%6),66+36*(idCase//6)))
                    fenetre.blit(cadreS,(552+38*(idCase%6),65+36*(idCase//6)))
                    pygame.display.update(pygame.Rect(552+38*(idCase%6),65+36*(idCase//6),34,34))
                    nom = policeb.render(objets[idObjet][1],True,pygame.Color(220,220,220))
                    fenetre.blit(fond_inventaire,(0,0))
                    fenetre.blit(nom,(540,440))
                    description = polices.render(objets[idObjet][3],True,pygame.Color(220,220,220))
                    fenetre.blit(description,(540,470))
                    #créer un bouton 'Equiper'
                    equiper = polices.render("Equiper",True,pygame.Color(220,220,220))
                    fenetre.blit(equiper,(730,560))
                    pygame.display.update(pygame.Rect(540,440,250,140))
                    attente = True
                    while attente :
                        clock.tick(100) #permet de ne pas surcharger le processeur
                        event = pygame.event.poll() #prend un événement dans la queue (potentiellement aucun)
                        if event.type == QUIT: #si clic sur la croix rouge en haut à gauche
                            return sauvegarde, objets
                        elif event.type == KEYDOWN and event.key == K_ESCAPE: #si clic sur Echap
                            attente = False
                        elif event.type == MOUSEBUTTONDOWN :
                            if 730 <= event.pos[0] < 790 and 560 <= event.pos[1] < 580 :
                                #on retire l'inventaire et on l'ajoute à l'équipement du joueur sélectionné
                                sauvegarde = equipementObjet(fenetre,sauvegarde,objets,idObjet,joueurSel)
                                attente = False
                            else :
                                attente = False
                    #on réactualise l'affichage
                    affiche_Equipement(fond_inventaire,fenetre,itemFinal,sauvegarde[0][joueurSel],objets)
                    affiche_dansInventaire(fond_inventaire,fenetre,itemFinal,sauvegarde[1],objets)
                    pygame.display.update(pygame.Rect(540,440,250,140)) #on efface les caractéristiques

    pygame.font.quit()
    pygame.quit()
    return sauvegarde, objets
#sauvegarde = [personnages, inventaire, pnjs]
#personnages = [ string nom_personnage,
#[	[string nom_img_sur_map, transparence],
#	[string nom_img_sur_combat, transparence], # transparence : bool + r, g, b
#	[string nom_img_dialogues, transparence]
#],
#[ objets_equipes ],   # liste : pour chaque emplacement, l'id d'un objet -> -1 = rien
#( caracs ) ]	      # tuple : pour chaque carac, deux nombres : max et actuel
#inventaire = [nb_objet dans le sac pour chaque id_objet]
personnage1 = [None,None,[1,-1,2,-1,3,2,2,1]]
personnage2 = [None,None,[1,-1,-1,-1,-1,-1,-1,-1]]
personnage3 = [None,None,[-1,4,-1,-1,3,-1,7,-1]]
dansInv = [0,3,4,2,0,0,0,0]
pnjs = None
sauvegarde = [[personnage1,personnage2,personnage3],dansInv,pnjs]
objets = [[4,"banane",100,"objet jaune\n à manger après un effort pour éviter les courbatures\nutiliser la peau contre les méchants",[None],["itemFinal2.png",0,10]] for _ in range (8)]
inventaire(sauvegarde,objets)

"""objet = [int type (ex : si c'est un équipement, un objet utilisable, etc)
string nom_objet
int valeur (pour savoir quel prix l'acheter / le vendre)
string description_objet (à afficher dans l'inventaire)
[
	[
		int id_caractéristique  (pour les objets qui ont un effet lorsqu'ils sont équipés / consommés)
		int modification
	]
]
[string nom_img, int i_lig, i_col]
]"""
#type : 1=chapeau, 2=ceinture, 3= pendentif, 4= bague, 5=arme, 6=bouclier, 7=armure