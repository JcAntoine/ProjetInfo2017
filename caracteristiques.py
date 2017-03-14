# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        module des caractéristiques des personnages
# Purpose:
#
# Author:      Jean-Christophe
#
# Created:     12/03/2017
# Copyright:   (c) Jean-Christophe 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import pygame
import pickle
from pygame.locals import *
if 'dialogue' in sys.modules: # note : il faudra supprimer ces deux instructions dès que le module
    del(sys.modules['lecture.dialogue']) # sera fini (plus de modifications) afin de rendre le programme plus rapide
import dialogue
pygame.init()

def displayBackground(nomFenetre, joueurSelec):
    fondCarac = pygame.image.load("Projets/images/inventaire/fond_defaut.png").convert()
    fondCarac = pygame.transform.scale(fond_inventaire,(800,600))
    nomFenetre.blit(fondCarac,(0,0))
    imagesPerso = [pygame.image.load("Projets/images/caracteristiques/adrien.png").convert(),pygame.image.load("Projets/images/caracteristiques/trinity.png").convert(),pygame.image.load("Projets/images/caracteristiques/jc.png").convert()]
    image = imagesPerso[joueurSelec]
    fenetre.blit(image,(0,0))
    pygame.display.update(pygame.Rect(0,0,155,300))

def displayCarac(nomFenetre, sauvegarde, joueurSelec):
    policeCarac = pygame.font.Font("Polices/ARBLANCA.ttf", 24)
    dialogue.afficherTexte(nomFenetre, "Points de vie :", 160, 540, 30, (150, 150, 150))
    texte = ["Points de vie : ", "Points d'attaque :", "Initiative : "]
    carac = [sauvegarde[0][joueurSelec][3][0][0], sauvegarde[0][joueurSelec][3][0][1], sauvegarde[0][joueurSelec][3][1][0], sauvegarde[0][joueurSelec][3][1][1], sauvegarde[0][joueurSelec][3][2][0], sauvegarde[0][joueurSelec][3][2][1]] #[pvbase, pvbonus, pointsbase, pointsbonus, initiativebase, initiativebonus]
    dialogue.afficherTexte(nomFenetre, str(pvBase), 160, 540, 30, (250, 250, 250))
    for i in range(3):
        dialogue.afficherTexte(nomFenetre, texte[i], 160, 540, 30+60*(i+1), (150, 150, 150))

        largeur, hauteur = policeCarac.size(texte[i])
        dialogue.afficherTexte(nomFenetre, str(carac[2*i]), 160, 540+largeur, 30+60*(i+1), (250, 50, 50))

        largeur, hauteur = policeCarac.size(texte[i]+str(carac[2*i]))
        dialogue.afficherTexte(nomFenetre, " + ", 160, 540+largeur, 30+60*(i+1), (150, 150, 150))

        largeur, hauteur = policeCarac.size(texte[i]+str(carac[2*i])+" + ")
        dialogue.afficherTexte(nomFenetre, str(carac[2*i+1]), 540+largeur, 30+60*(i+1), (50, 50, 250))

        largeur, hauteur = policeCarac.size(texte[i]+str(carac[2*i])+" + "+str(carac[2*i+1]))
        dialogue.afficherTexte(nomFenetre, " = ", 160, 540+largeur, 30+60*(i+1), (150, 150, 150))

        largeur, hauteur = policeCarac.size(texte[i]+str(carac[2*i])+" + "+str(carac[2*i+1])+" = ")
        dialogue.afficherTexte(nomFenetre, str(carac[2*i]+carac[2*i+1]), 160, 540+largeur, 30+60*(i+1), (50, 250, 50))


def displayCaracteristiques(nomFenetre, sauvegarde, listeItems):
    joueurSelec = 0 #(Adrien:0, Trinity: 1, Arthur: 2), ici c'est le joueur par défaut
    displayBackground(nomFenetre, joueurSelec)
    itemFinal = pygame.image.load("Projets/images/inventaire/itemFinal2.png")
    joueurSelec = 0 #(Adrien:0, Trinity: 1, Arthur: 2)
    displayStuff(nomFenetre, sauvegarde, joueurSelec)
    displayCarac(nomFenetre, sauvegarde, joueurSelec)
    pygame.display.flip()
    continuer = True
    pygame.event.pump()
    while continuer:
        clock.tick(100) #permet de ne pas surcharger le processeur
        event = pygame.event.poll() #prend un événement dans la queue (potentiellement aucun)
        if event.type == QUIT: #si clic sur la croix rouge en haut à gauche
            continuer = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE: #si clic sur Echap
            continuer = False

def displayStuff(nomFenetre, sauvegarde, joueurSelec, listeItems):
    stuff = sauvegarde[0][joueurSelec][2]
    for idAffichage,idObjet in enumerate(stuff) :
        if idObjet != -1 : #affichage de l'objet si il y en a un
            image =  itemFinal.subsurface(objets[idObjet][5][2]*32,objets[idObjet][5][1]*32,32,32)
            image = pygame.transform.scale(image,(64,64))
            nomFenetre.blit(image,(262+108*(idAffichage%2),48+83*(idAffichage//2)))
    pygame.display.update(pygame.Rect(259,47,181,341))


