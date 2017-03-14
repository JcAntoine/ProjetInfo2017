# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        dialogue
# Purpose:
#
# Author:      Jean-Christophe
#
# Created:     11/12/2016
# Copyright:   (c) Jean-Christophe 2016-2017
# Licence:     None
#-------------------------------------------------------------------------------

import pygame
import pickle
from pygame.locals import *
pygame.init()

def fondNoirTransparent(nomFenetre): #fonction pour mettre une surface noire à demi transparente sur tout l'écran
    fondNoirTransparent = pygame.Surface((800, 600)) #on définit une surface vierge, par défaut noire
    fondNoirTransparent.set_alpha(128) #on la rend semi opaque
    nomFenetre.blit(fondNoirTransparent, (0, 0)) #on l'affiche

def fondDialogue(nomFenetre, fond, nomParleur): #fonction pour afficher le fond dont on aura besoin pour notre dialogue
    nomFenetre.blit(fond, (0, 0)) #on affiche le fond
    fondNoirTransparent(nomFenetre) #sa surface transparente
    hauteurFen = nomFenetre.get_height()
    largeurFen = nomFenetre.get_width()
    fondTexte(nomFenetre) #et l'arrière-plan du texte
    nomParleurAff(nomFenetre, nomParleur) #suivi du nom du parleur et son fond

def fondTexte(nomFenetre):
    hauteurFen = nomFenetre.get_height()
    largeurFen = nomFenetre.get_width()
    fondTexte = pygame.image.load("images/Dialogue/fond.png").convert_alpha()
    nomFenetre.blit(fondTexte, ((largeurFen-fondTexte.get_width())//2, hauteurFen-fondTexte.get_height()-16))

def nomParleurAff(nomFenetre, nomParleur): #fonction pour afficher le nom du parleur sur sa banderolle rouge
    hauteurFen = nomFenetre.get_height()
    largeurFen = nomFenetre.get_width()
    fondNom = pygame.image.load("images/Dialogue/fondNomPerso.png").convert_alpha()
    nomFenetre.blit(fondNom, (((largeurFen-612)//2)-14, hauteurFen-181-21)) #612 et 181 sont les dimensions de l'image de fond
    policeNom = pygame.font.Font("Polices/OfenbacherSchwabCAT.ttf", 18)
    nom = policeNom.render(nomParleur, True, pygame.Color(50, 50, 50))
    nomFenetre.blit(nom, (((largeurFen-612)//2)+25, hauteurFen-181+2)) #612 et 199 sont les dimensions de l'image de fond, les autres nombres sont des ajustements graphiques

def afficherRepliqueFrequence(nomFenetre, nomParleur, texte, fond): #fonction pour afficher une réplique lettre par lettre
    policeReplique = pygame.font.Font("Polices/ARBLANCA.ttf", 24)
    delai = 10 #délai entre les lettres (millisecondes)
    #on va split le texte en lignes pour ne pas déborder
    if nomParleur != "Choix":
        lignes = decompTexte(texte, 588) #on décompose le texte en lignes, lignes étant des listes contenant les mots
    else:
        lignes = texte
    nbLignes = len(lignes)
    horloge = pygame.time.Clock() #nous permettra de définir la rapidité de défilement plus tard
    i = 0 #correspond à la ligne traitée
    while i < nbLignes: #on traite ligne par ligne
        nb_caracteres = len(lignes[i])
        j = 1 #correspond au caractère traité
        while j < nb_caracteres: #pour chaque lettre de la ligne
            fondDialogue(nomFenetre, fond, nomParleur) #on affiche le fond, pour effacer la réplique d'avant
            if nomParleur !="Choix":
                #affiche_expression(nomFenetre, spritePersonnage, idExpression)
                pass
            #on reaffiche les lignes déjà affichées (obligation de tout réafficher, car la gestion de l'affichage n'est pas esthétique sinon, cf dossier)
            for k in range(i):
                afficherReplique(nomFenetre, str("".join(lignes[k])), 104, 452+k*24) #fonction qui affiche le texte instantannément des lignes précédentes
            afficherReplique(nomFenetre, str("".join(lignes[i][:j])), 104, 452+i*24) #on affiche le texte de la ligne en cours qui était censé être affiché et qui a été effacé par le réaffichage du fond avec la nouvelle lettre(on a déjà réaffiché les lignes précédentes)
            pygame.display.flip() #on actualise l'affichage
            horloge.tick(1000//delai) # car pygame fonctionne en ms
            event = pygame.event.poll() #on récupère les évènements
            while event.type != NOEVENT:
                if event.type == KEYDOWN and event.key == K_RETURN: #quand l'évènement est l'appuie sur la touche entrée, on quitte la boucle
                    i = nbLignes
                    j = nb_caracteres
                    pygame.event.clear()
                event = pygame.event.poll()
            j += 1
        i += 1
    fondDialogue(nomFenetre, fond, nomParleur)
    for i in range(nbLignes):
        afficherReplique(nomFenetre, lignes[i], 104, 452+i*24)
    pygame.display.flip()
    event = pygame.event.poll()
    if nomParleur == "Choix":
        #fleche_selection = pygame.Surface((10, 10))
        #fleche_selection.fill(pygame.Color(255, 0, 0))
        afficherTexte(nomFenetre, lignes[0], 592, 104, 452, (255, 50, 50))
        pygame.display.flip()
        idLigneAColorer = 0
        while event.type != KEYDOWN or event.key != K_RETURN:
            if event.type == KEYDOWN and (event.key == K_UP or event.key == K_DOWN):
                if event.key == K_DOWN:
                    idLigneAColorer += 1
                    if idLigneAColorer >= nbLignes:
                        idLigneAColorer = nbLignes-1
                else:
                    idLigneAColorer -= 1
                    if idLigneAColorer < 0:
                        idLigneAColorer = 0
                fondDialogue(nomFenetre, fond, "Choix")
                for i in range(nbLignes):
                    couleur = (50, 50, 50)
                    if i == idLigneAColorer:
                        couleur = (255, 0, 0)
                    afficherTexte(nomFenetre, lignes[i], 592, 104, 452+24*i, couleur)
                    pygame.display.flip()
            event = pygame.event.poll()
        return idLigneAColorer
    else:
        while event.type != KEYDOWN or event.key != K_RETURN:
            horloge.tick(50)   # en principe, il n'y a pas plus de 50 événements à la seconde (certains ont déjà été bloqués)
            event = pygame.event.poll()
    return

def afficherReplique(nomFenetre, texte, x, y, color=(50, 50, 50), policeReplique = pygame.font.Font("Polices/ARBLANCA.ttf", 24)): #fonction pour afficher tout d'un coup
    surfaceTexte = policeReplique.render(texte, True, color)
    nomFenetre.blit(surfaceTexte, (x, y))
    return

def decompTexte(texte, largeurMax, policeReplique = pygame.font.Font("Polices/ARBLANCA.ttf", 24)):
    texte = texte.split() #on décompose notre chaîne de caractère en une liste de mots
    nbMots = len(texte)
    lignes = [""] #chaque élément de la liste sera le texte à afficher sur chaque ligne
    nbLignes = 1 #correspond à la ligne traitée au moment de l'affichage
    for i in range(nbMots): #pour chaque mot du texte :
        try:
            largeur, hauteur = policeReplique.size(lignes[nbLignes-1]+" "+texte[i]) #on extrait sa largeur pour avoir si on débordera
        except:
            print(pygame.get_error())
        if largeur > largeurMax and not(texte[i] in ["?", "!", ";", ")", "]"]) : #largeurMax correspond à la largeur qu'on ne veut pas déborder, donc si on déborderait ou si le nouveau mot est un élément de ponctuation :
            lignes.append(texte[i]) #on a besoin d'une nouvelle ligne
            nbLignes += 1 #comme on a fini avec la taille de la ligne actuelle, on traite la ligne suivante
        else:
            if lignes[nbLignes-1] != "":
                lignes[nbLignes-1] = lignes[nbLignes-1]+" "+texte[i] #sinon on rajoute le mot à la ligne, avec un espace
            else:
                lignes[nbLignes-1] = texte[i]
    return lignes

def afficherTexte(nomFenetre, texte, largeurMax, x, y, color=(50, 50, 50), policeReplique = pygame.font.Font("Polices/ARBLANCA.ttf", 24), taillePolice = 24):
    lignes = decompTexte(texte, largeurMax, policeReplique)
    nbLignes = len(lignes)
    for i in range(nbLignes):
        afficherReplique(nomFenetre, lignes[i], x, y+taillePolice*i, color, policeReplique)

def faire_dialogue(nomFenetre, fond, nom_fichier_dialogue, sauvegarde, nom_projet):
    dialogue_actuel = charger_fichier(nom_fichier_dialogue)
    ensemble_sprites = charger_fichier(nom_projet)    # pour chaque id_pnj : [nom_sprite, nom_personnage]
    continuer = True
    while continuer:
        dlg_select = dialogue_actuel[1][sauvegarde[2][dialogue_actuel[0]]]
        for ind, txt in enumerate(dlg_select[:-2]):
            afficherRepliqueFrequence(nomFenetre, ensemble_sprites[txt[2]][1], txt[0], fond)
        for ind, modif in enumerate(dlg_select[-2][0]):   # en principe, le tableau est assez grand !
            sauvegarde[2][modif[0]] = modif[1]
        if dlg_select[-1][0]: #si il y a une option
            fondDialogue(nomFenetre, fond, "Choix") #on réaffiche le fond
            option = dialogue_actuel[2][dlg_select[-1][1]][0]
            idValeur= dialogue_actuel[2][dlg_select[-1][1]][1]
            nbOption = len(option)
            nbOptionsRespectees = 0
            listeOptionsRespectees = []
            listeIdOptionsRespectees = []
            for idOption in range(nbOption): #pour chaque choix possible :
                nbCondition = len(option[idOption][1])
                respect = True #présomption d'innoncence
                for idCondition in range(nbCondition): #on vérifie que les conditions sont toutes respectées
                    idObjet = option[idOption][1][idCondition][0]
                    quantiteMin = option[idOption][1][idCondition][1]
                    if sauvegarde[1][idObjet] < quantiteMin:
                        respect = False
                if respect: #on enregistre les conditions respectées
                    nbOptionsRespectees += 1
                    listeOptionsRespectees.append(option[idOption][0]) #on ajoute le texte de l'option à afficher
                    listeIdOptionsRespectees.append(idValeur[idOption])
            numeroOptionChoisie = afficherRepliqueFrequence(nomFenetre, "Choix", listeOptionsRespectees, fond) #il faut faire attention à ce que la longueur du texte de l'option ne soit pas trop grande ou alors mettre l'option la plus longue en dernier.
            optionChoisie = listeIdOptionsRespectees[numeroOptionChoisie]
            sauvegarde[2][dialogue_actuel[0]] = optionChoisie
            pygame.time.delay(1000)
        else:
            continuer = False
    return

def charger_fichier(nom_fichier):
    with open("./Projets/dialogues/"+nom_fichier+".dlg", "rb") as fichier:
        depi = pickle.Unpickler(fichier)
        fichier_actuel = depi.load()
    return fichier_actuel

def affiche_expression(nomFenetre, spritePersonnage, idExpression):
    return



"""Rappel : un fichier dialogue se décrit comme suit :

id_valeur
[
	[
		[txt1, i_expression, i_personnage],
		[txt2, i_expression, i_personnage],
		[txt3, i_expression, i_personnage], etc,
		[[
			[id_valeur1, valeur_nouvelle]
			, etc
		]],
		[est_choix, i_choix]
	],
	[],
	etc
]

[
	[
        [
		  [txt_option1, [[id_objet1, quantite_min], [id_objet2, quantite_min], etc]],
		  [txt_option2, [[id_objet1, quantite_min], [id_objet2, quantite_min], etc]]
        ],
        [id_valeur_option1, id_valeur_option2, etc]
	]
	[[textsOption], [id_valeurs]],
	etc,
]


id_valeur prend None quand cela ne change pas le dialogue à afficher par la suite"""
