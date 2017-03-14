# -*- coding: UTF-8 -*-
#test projet info

# format d'un projet :
# 0. 0. nombre de maps associées
# 0. 1. tableau des noms des maps associées

import sys
import pickle
import pygame
from pygame.locals import *
pygame.init()
if 'lecture.lecture' in sys.modules: # note : il faudra supprimer ces deux instructions dès que le module
    del(sys.modules['lecture.lecture']) # sera fini (plus de modifications) afin de rendre le programme plus rapide
if 'mappy.sprite' in sys.modules:
    del(sys.modules['mappy.sprite'])
if 'mappy.c_map' in sys.modules:
    del(sys.modules['mappy.c_map'])
if 'mappy.j_map' in sys.modules:
    del(sys.modules['mappy.j_map'])
import lecture.lecture
import mappy.sprite
import mappy.c_map
import mappy.j_map

def continuer_projet(fenetre, nom_fichier, projet_actuel):
    largeur = fenetre.get_width()
    hauteur = fenetre.get_width()
    fenetre.fill(pygame.Color(0, 127, 255))
    police_t = pygame.font.Font("Polices/JOKERMAN.TTF", (60*hauteur)//720)
    police_option = pygame.font.Font("Polices/JOKERMAN.TTF", (40*hauteur)//720)
    police_sel = pygame.font.Font("Polices/arial.TTF", (30*hauteur)//720)
    police_sousoption = pygame.font.Font("Polices/arial.TTF", (30*hauteur)//720)
    #création des textes :
    titre = police_t.render(nom_fichier[:len(nom_fichier)-4], True, pygame.Color(0, 0, 0))
    txt_sprite = police_option.render("Sprite", True, pygame.Color(0, 0, 0))
    txt_creer = police_sousoption.render("Créer", True, pygame.Color(0, 0, 0))
    txt_creersel = police_sel.render("Créer", True, pygame.Color(240, 195, 0))
    txt_modifier = police_sousoption.render("Modifier", True, pygame.Color(0, 0, 0))
    txt_modifiersel = police_sel.render("Modifier", True, pygame.Color(240, 195, 0))
    txt_map = police_option.render("Map", True, pygame.Color(0, 0, 0))
    txt_retour = police_sousoption.render("Retour", True, pygame.Color(0, 0, 0))
    txt_retoursel = police_sousoption.render("Retour", True, pygame.Color(240, 195, 0))
    #blits :
    ordonnees = [0]*7
    ordonnees[0] = (20*hauteur)//720
    ordonnees[1] = ordonnees[0]+titre.get_height()+((20*hauteur)//720)
    ordonnees[2] = ordonnees[1]+txt_sprite.get_height()+((5*hauteur)//720)
    ordonnees[3] = ordonnees[2]+txt_creer.get_height()+((5*hauteur)//720)
    ordonnees[4] = ordonnees[3]+txt_modifier.get_height()+((10*hauteur)//720)
    ordonnees[5] = ordonnees[4]+txt_map.get_height()+((5*hauteur)//720)
    ordonnees[6] = ordonnees[5]+txt_creer.get_height()+((5*hauteur)//720)
    fenetre.blit(titre, ((largeur-titre.get_width())/2, ordonnees[0]))
    fenetre.blit(txt_sprite, (50, ordonnees[1]))
    fenetre.blit(txt_creer, (100, ordonnees[2]))
    fenetre.blit(txt_modifier, (100, ordonnees[3]))
    fenetre.blit(txt_map, (50, ordonnees[4]))
    fenetre.blit(txt_creer, (100, ordonnees[5]))
    fenetre.blit(txt_modifier, (100, ordonnees[6]))
    fenetre.blit(txt_retour, (largeur-txt_retour.get_width()-10, hauteur-txt_retour.get_height()-10))
    pygame.display.flip()
    horloge = pygame.time.Clock()
    continuer = True
    reaffiche = False
    while continuer:
        horloge.tick(20)
        event = pygame.event.poll()
        if event.type == QUIT:
            return QUIT
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            return 0
        elif event.type == MOUSEMOTION:
            fenetre.fill(pygame.Color(0, 127, 255))
            fenetre.blit(titre, ((largeur-titre.get_width())/2, ordonnees[0]))
            fenetre.blit(txt_sprite, (50, ordonnees[1]))
            fenetre.blit(txt_creer, (100, ordonnees[2]))
            fenetre.blit(txt_modifier, (100, ordonnees[3]))
            fenetre.blit(txt_map, (50, ordonnees[4]))
            fenetre.blit(txt_creer, (100, ordonnees[5]))
            fenetre.blit(txt_modifier, (100, ordonnees[6]))
            fenetre.blit(txt_retour, (largeur-txt_retour.get_width()-10, hauteur-txt_retour.get_height()-10))
            if event.pos[1] <= ordonnees[3] and event.pos[1] >= ordonnees[2]:
                fenetre.blit(txt_creersel, (100, ordonnees[2]))
            elif event.pos[1] <= ordonnees[4] and event.pos[1] >= ordonnees[3]:
                fenetre.blit(txt_modifiersel, (100, ordonnees[3]))
            elif event.pos[1] <= ordonnees[6] and event.pos[1] >= ordonnees[5]:
                fenetre.blit(txt_creersel, (100, ordonnees[5]))
            elif event.pos[1] <= ordonnees[6]+txt_modifier.get_height() and event.pos[1] >= ordonnees[6]:
                fenetre.blit(txt_modifiersel, (100, ordonnees[6]))
            elif lecture.lecture.est_compris_dedans(event.pos, (largeur-txt_retour.get_width()-10, hauteur-txt_retour.get_height()-10, txt_retour.get_width(), txt_retour.get_height())):
                fenetre.blit(txt_retoursel, (largeur-txt_retour.get_width()-10, hauteur-txt_retour.get_height()-10))
            pygame.display.flip()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1: #clic gauche
            if event.pos[1] <= ordonnees[3] and event.pos[1] >= ordonnees[2]: #créer sprite
                (nom_sprite, ok) = lecture.lecture.lire_nom_sprite(fenetre, True)
                if ok == -1:
                    return QUIT
                if ok == 0:
                    reaffiche = True
                elif ok == 1:
                    while ok == 1:
                        try:
                            if nom_sprite != "":
                                new_sprite = open("Projets/sprites/"+nom_sprite+".spr", "rb")
                                new_sprite.close()
                            (nom_sprite, ok) = lecture.lecture.lire_nom_sprite(fenetre, True, True)
                        except:
                            try:
                                surf_sprite = pygame.image.load("Projets/images/"+nom_sprite)
                                new_sprite = open("Projets/sprites/"+nom_sprite+".spr", "wb")
                                sprite = (nom_sprite, [False, 0, 0, 0], (surf_sprite.get_width(), surf_sprite.get_height()), [1, 1], [surf_sprite.get_width(), surf_sprite.get_height()], [[[False, False, False, False]]], [[0]]) #cf format d'une sprite
                                sprite_pickle = pickle.Pickler(new_sprite)
                                sprite_pickle.dump(sprite)
                                new_sprite.close()
                                ok = 2 #sortie de la boucle
                            except:
                                (nom_sprite, ok) = lecture.lecture.lire_nom_sprite(fenetre, True, True)
                    if ok == -1:
                        return QUIT
                    if ok == 2:
                        if(mappy.sprite.continuer_sprite(fenetre, sprite) == QUIT):
                            return QUIT
                        reaffiche = True
            elif event.pos[1] <= ordonnees[4] and event.pos[1] >= ordonnees[3]: #continuer sprite
                (nom_sprite, ok) = lecture.lecture.lire_nom_sprite(fenetre, False)
                if ok == -1:
                    return QUIT
                if ok == 0:
                    reaffiche = True
                elif ok == 1:
                    while ok == 1:
                        try:
                            new_sprite = open("Projets/sprites/"+nom_sprite+".spr", "rb")
                            sprite_depickle = pickle.Unpickler(new_sprite)
                            sprite = sprite_depickle.load()
                            new_sprite.close()
                            ok = 2
                        except:
                            (nom_sprite, ok) = lecture.lecture.lire_nom_sprite(fenetre, False, True)
                    if ok == -1:
                        return QUIT
                    if ok == 2:
                        if(mappy.sprite.continuer_sprite(fenetre, sprite) == QUIT):
                            return QUIT
                        reaffiche = True
            elif event.pos[1] <= ordonnees[6] and event.pos[1] >= ordonnees[5]: # nouvelle map
                if(mappy.c_map.recupere_nom_new_map(fenetre) == QUIT):
                    return QUIT
                reaffiche = True
            elif event.pos[1] <= ordonnees[6]+txt_modifier.get_height() and event.pos[1] >= ordonnees[6]: # continuer map
                if(mappy.c_map.recupere_nom_map(fenetre) == QUIT):
                    return QUIT
                reaffiche = True
            elif lecture.lecture.est_compris_dedans(event.pos, (largeur-txt_retour.get_width()-10, hauteur-txt_retour.get_height()-10, txt_retour.get_width(), txt_retour.get_height())):
                return 0
            if reaffiche:
                reaffiche = False
                fenetre.fill(pygame.Color(0, 127, 255))
                fenetre.blit(titre, ((largeur-titre.get_width())/2, ordonnees[0]))
                fenetre.blit(txt_sprite, (50, ordonnees[1]))
                fenetre.blit(txt_creer, (100, ordonnees[2]))
                fenetre.blit(txt_modifier, (100, ordonnees[3]))
                fenetre.blit(txt_map, (50, ordonnees[4]))
                fenetre.blit(txt_creer, (100, ordonnees[5]))
                fenetre.blit(txt_modifier, (100, ordonnees[6]))
                fenetre.blit(txt_retour, (largeur-txt_retour.get_width()-10, hauteur-txt_retour.get_height()-10))
    return 0

def main_jouer(fenetre, fond_menu, polices):
    pass #idéalement: appelle le module lecture pour avoir accès au nom du projet puis lancement du jeu

def main_creer(fenetre, fond_menu, polices): #on garde les polices pour un nouveau menu de sélection
    #actualisation de l'image à l'écran, même processus que précédemment
    largeur = fenetre.get_width()
    hauteur = fenetre.get_height()
    fenetre.blit(fond_menu, (0, 0))
    titre_creer = polices[0].render("Créer", True, pygame.Color(0, 0, 0))
    fenetre.blit(titre_creer, ((largeur-titre_creer.get_width())/2, (20*hauteur)//720))
    nouveau_titre = polices[1].render("Nouveau", True, pygame.Color(0, 0, 0))
    nouveau_selection = polices[2].render("Nouveau", True, pygame.Color(240, 195, 0))
    fenetre.blit(nouveau_titre, ((largeur-nouveau_titre.get_width())/2, (300*hauteur)//720))
    continuer_titre = polices[1].render("Continuer", True, pygame.Color(0, 0, 0))
    continuer_selection = polices[2].render("Continuer", True, pygame.Color(240, 195, 0))
    fenetre.blit(continuer_titre, ((largeur-continuer_titre.get_width())/2, (440*hauteur)//720))
    retour_titre = polices[1].render("Retour", True, pygame.Color(0, 0, 0))
    retour_selection = polices[2].render("Retour", True, pygame.Color(240, 195, 0))
    fenetre.blit(retour_titre, ((largeur-retour_titre.get_width())/2, (580*hauteur)//720))
    pygame.display.flip()
    horloge = pygame.time.Clock()
    continuer = True
    position = 0
    while continuer:
        horloge.tick()
        event = pygame.event.poll()
        if event.type == QUIT: #sera interprété comme quitter le programme entier
            return QUIT
        elif event.type == KEYDOWN and event.key == K_ESCAPE: #aussi
            return QUIT
        elif event.type == MOUSEMOTION: #de même qu'avant, permet surlignage
            nouvelle_position = ((720*event.pos[1])-(130*hauteur))//(140*hauteur)
            if nouvelle_position != position:
                fenetre.blit(fond_menu, (0, 0))
                fenetre.blit(titre_creer, ((largeur-titre_creer.get_width())//2, (hauteur*20)//720))
                fenetre.blit(nouveau_titre, ((largeur-nouveau_titre.get_width())//2, (300*hauteur)//720))
                fenetre.blit(continuer_titre, ((largeur-continuer_titre.get_width())//2, (440*hauteur)//720))
                fenetre.blit(retour_titre, ((largeur-retour_titre.get_width())//2, (580*hauteur)//720))
                if nouvelle_position == 1:
                    fenetre.blit(nouveau_selection, ((largeur-nouveau_selection.get_width())//2, 1+((300*hauteur)//720)))
                elif nouvelle_position == 2:
                    fenetre.blit(continuer_selection, ((largeur-continuer_selection.get_width())//2, 1+((440*hauteur)//720)))
                elif nouvelle_position == 3:
                    fenetre.blit(retour_selection, ((largeur-retour_selection.get_width())//2, 1+((580*hauteur)//720)))
                pygame.display.flip()
                position = nouvelle_position
        elif event.type == MOUSEBUTTONDOWN and event.button == 1: #selon position du clic gauche
            if position == 1: #correspond à créer nouveau projet
                (nom_projet, ok) = lecture.lecture.lire_nom_projet(fenetre, True)
                if ok == -1:
                    return QUIT
                if ok == 0:
                    fenetre.blit(fond_menu, (0, 0))
                    fenetre.blit(titre_creer, ((largeur-titre_creer.get_width())//2, (hauteur*20)//720))
                    fenetre.blit(nouveau_titre, ((largeur-nouveau_titre.get_width())//2, (300*hauteur)//720))
                    fenetre.blit(continuer_titre, ((largeur-continuer_titre.get_width())//2, (440*hauteur)//720))
                    fenetre.blit(retour_titre, ((largeur-retour_titre.get_width())//2, (580*hauteur)//720))
                    pygame.display.flip()
                elif ok == 1:
                    while ok == 1:
                        try:
                            if nom_projet != "":
                                new_projet = open("Projets/"+nom_projet+".prj", "rb")
                            (nom_projet, ok) = lecture.lecture.lire_nom_projet(fenetre, True, True)
                        except:
                            with open("Projets/"+nom_projet+".prj", "wb") as new_project:
                                projet = [[0, []]]
                                prj_pi = pickle.Pickler(new_project)
                                prj_pi.dump(projet)
                            ok = 2 #sortie de la boucle
                    if ok == QUIT:
                        return QUIT
                    if ok == 2:
                        if(continuer_projet(fenetre, nom_projet+".prj", projet) == QUIT):
                            return QUIT
            elif position == 2: #correspond à continuer un projet
                (nom_projet, ok) = lecture.lecture.lire_nom_projet(fenetre, False)
                if ok == -1:
                    return QUIT
                if ok == 0:
                    fenetre.blit(fond_menu, (0, 0))
                    fenetre.blit(titre_creer, ((largeur-titre_creer.get_width())//2, (hauteur*20)//720))
                    fenetre.blit(nouveau_titre, ((largeur-nouveau_titre.get_width())//2, (300*hauteur)//720))
                    fenetre.blit(continuer_titre, ((largeur-continuer_titre.get_width())//2, (440*hauteur)//720))
                    fenetre.blit(retour_titre, ((largeur-retour_titre.get_width())//2, (580*hauteur)//720))
                    pygame.display.flip()
                elif ok == 1:
                    while ok == 1:
                        try:
                            with open("Projets/"+nom_projet+".prj", "rb") as new_projet:
                                prj_pi = pickle.Unpickler(new_projet)
                                projet = prj_pi.load()
                            ok = 2 #sortie de la boucle
                        except:
                            (nom_projet, ok) = lecture.lecture.lire_nom_projet(fenetre, False, True)
                    if ok == QUIT:
                        return QUIT
                    if ok == 2:
                        if(continuer_projet(fenetre, nom_projet+".prj", projet) == QUIT):
                            return QUIT
            elif position == 3: #correspond à retour en arrière
                return 0
    print("Erreur...")
    return QUIT #en principe, on n'arrive jamais ici mais au cas où

def main_tutos(fenetre, fond_menu, polices):
    pass #idéalement : dans un module spécifique, pas de fonction dédiée dans ce script main

def main_menu():
    #initialisations
    pygame.init()
    pygame.display.init()
    pygame.font.init()
    #création fenêtre
    hauteur = 600
    largeur = 800
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Projet info - JC, Adrien, Philippe")
    #création fond
    fond_menu = pygame.image.load("fond_menu_grand.jpg").convert()
    fenetre.blit(fond_menu, (0, 0))
    #création polices
    policet = pygame.font.Font("Polices/JOKERMAN.TTF", (60*hauteur)//720)
    police = pygame.font.Font("Polices/JOKERMAN.TTF", (46*hauteur)//720)
    polices = pygame.font.Font("Polices/JOKERMAN.TTF", (44*hauteur)//720)
    #création titre
    titre = policet.render("New game", True, pygame.Color(0, 0, 0))
    fenetre.blit(titre, ((largeur-titre.get_width())//2, (20*hauteur)//720))
    #création titre jouer
    jouer_titre = police.render("Jouer", True, pygame.Color(0, 0, 0))
    jouer_selection = polices.render("Jouer", True, pygame.Color(240, 195, 0))
    fenetre.blit(jouer_titre, ((largeur-jouer_titre.get_width())//2, (300*hauteur)//720))
    #création titre créer
    creer_titre = police.render("Créer", True, pygame.Color(0, 0, 0))
    creer_selection = polices.render("Créer", True, pygame.Color(240, 195, 0))
    fenetre.blit(creer_titre, ((largeur-creer_titre.get_width())//2, (440*hauteur)//720))
    #création titre tutos
    tutos_titre = police.render("Tutoriels", True, pygame.Color(0, 0, 0))
    tutos_selection = polices.render("Tutoriels", True, pygame.Color(240, 195, 0))
    fenetre.blit(tutos_titre, ((largeur-tutos_titre.get_width())//2, (580*hauteur)//720))
    #événements :
    pygame.display.flip()
    horloge = pygame.time.Clock()
    continuer = True
    position = 0
    pygame.event.pump()
    while continuer:
        horloge.tick(20) #permet de ne pas surcharger le processeur, pas plus de 1 tour de boucle par 20 ms
        event = pygame.event.poll() #prend un événement dans la queue (potentiellement aucun)
        if event.type == QUIT: #si clic sur la croix rouge en haut à gauche
            continuer = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE: #si clic sur Echap
            continuer = False
        elif event.type == MOUSEMOTION: #mouvement de la souris
            nouvelle_position = ((720*event.pos[1])-(130*hauteur))//(140*hauteur)
            if nouvelle_position != position: #si c'est une nouvelle position du curseur, on actualise l'image à l'écran
                fenetre.blit(fond_menu, (0, 0))
                fenetre.blit(titre, ((largeur-titre.get_width())//2, (20*hauteur)//720))
                fenetre.blit(jouer_titre, ((largeur-jouer_titre.get_width())//2, (300*hauteur)//720))
                fenetre.blit(creer_titre, ((largeur-creer_titre.get_width())//2, (440*hauteur)//720))
                fenetre.blit(tutos_titre, ((largeur-tutos_titre.get_width())//2, (580*hauteur)//720))
                if nouvelle_position == 1: #selon la position, on surligne l'option clicable
                    fenetre.blit(jouer_selection, ((largeur-jouer_selection.get_width())//2, 1+((300*hauteur)//720)))
                elif nouvelle_position == 2:
                    fenetre.blit(creer_selection, ((largeur-creer_selection.get_width())//2, 1+((440*hauteur)//720)))
                elif nouvelle_position == 3:
                    fenetre.blit(tutos_selection, ((largeur-tutos_selection.get_width())//2, 1+((580*hauteur)//720)))
                pygame.display.flip()
                position = nouvelle_position
        elif event.type == MOUSEBUTTONDOWN and event.button == 1: #si clic gauche
            if position == 1:
               if(main_jouer(fenetre, fond_menu, (policet, police, polices)) == QUIT):
                    continuer = False
            elif position == 2:
                if(main_creer(fenetre, fond_menu, (policet, police, polices)) == QUIT):
                    continuer = False
            elif position == 3:
                if(main_tutos(fenetre, fond_menu, (policet, police, polices)) == QUIT):
                    continuer = False
    #lecture.lecture.lire_nom_projet(fenetre, True) #test de la lecture
    pygame.font.quit()
    pygame.quit()
    return

def test_j_map():
    mappy.j_map.main_test()

if __name__ == '__main__':
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    test_j_map()
    #main_menu()