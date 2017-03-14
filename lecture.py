# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        lectures
# Purpose:
#
# Author:      Philippe
#
# Created:     11/12/2016
# Copyright:   (c) Philippe 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
from pygame.locals import *
pygame.init()

def quel_caractere(key, majuscule):
    if majuscule == 1:
        if key == K_0 or key == K_KP0:
            return "0"
        elif key == K_1 or key == K_KP1:
            return "1"
        elif key == K_2 or key == K_KP2:
            return "2"
        elif key == K_3 or key == K_KP3:
            return "3"
        elif key == K_4 or key == K_KP4:
            return "4"
        elif key == K_5 or key == K_KP5:
            return "5"
        elif key == K_6 or key == K_KP6:
            return "6"
        elif key == K_7 or key == K_KP7:
            return "7"
        elif key == K_8 or key == K_KP8:
            return "8"
        elif key == K_9 or key == K_KP9:
            return "9"
        elif key == K_a:
            return "Q"
        elif key == K_b:
            return "B"
        elif key == K_c:
            return "C"
        elif key == K_d:
            return "D"
        elif key == K_e:
            return "E"
        elif key == K_f:
            return "F"
        elif key == K_g:
            return "G"
        elif key == K_h:
            return "H"
        elif key == K_i:
            return "I"
        elif key == K_j:
            return "J"
        elif key == K_k:
            return "K"
        elif key == K_l:
            return "L"
        elif key == K_SEMICOLON:
            return "M"
        elif key == K_n:
            return "N"
        elif key == K_o:
            return "O"
        elif key == K_p:
            return "P"
        elif key == K_q:
            return "A"
        elif key == K_r:
            return "R"
        elif key == K_s:
            return "S"
        elif key == K_t:
            return "T"
        elif key == K_u:
            return "U"
        elif key == K_v:
            return "V"
        elif key == K_w:
            return "Z"
        elif key == K_x:
            return "X"
        elif key == K_y:
            return "Y"
        elif key == K_z:
            return "W"
        elif key == K_COMMA:
            return "."
    else:
        if key == K_6:
            return "-"
        elif key == K_8:
            return "_"
        elif key == K_a:
            return "q"
        elif key == K_b:
            return "b"
        elif key == K_c:
            return "c"
        elif key == K_d:
            return "d"
        elif key == K_e:
            return "e"
        elif key == K_f:
            return "f"
        elif key == K_g:
            return "g"
        elif key == K_h:
            return "h"
        elif key == K_i:
            return "i"
        elif key == K_j:
            return "j"
        elif key == K_k:
            return "k"
        elif key == K_l:
            return "l"
        elif key == K_SEMICOLON:
            return "m"
        elif key == K_n:
            return "n"
        elif key == K_o:
            return "o"
        elif key == K_p:
            return "p"
        elif key == K_q:
            return "a"
        elif key == K_r:
            return "r"
        elif key == K_s:
            return "s"
        elif key == K_t:
            return "t"
        elif key == K_u:
            return "u"
        elif key == K_v:
            return "v"
        elif key == K_w:
            return "z"
        elif key == K_x:
            return "x"
        elif key == K_y:
            return "y"
        elif key == K_z:
            return "w"
    return ""

def est_compris_dedans(position, rectangle):
    if rectangle[0] <= position[0] and rectangle[0]+rectangle[2] >= position[0] and rectangle[1] <= position[1] and rectangle[1]+rectangle[3] >= position[1]:
        return True
    return False

def lire_nom_projet(fenetre, est_nouveau, erreur=False):
    fenetre.fill(pygame.Color(0, 127, 255))
    police = pygame.font.Font("./Polices/JOKERMAN.TTF", 30)
    police_suite = pygame.font.Font("./Polices/JOKERMAN.TTF", 24)
    police_sel = pygame.font.Font("./Polices/JOKERMAN.TTF", 23)
    if est_nouveau:
        titre = police.render("Création : nouveau projet", True, pygame.Color(0, 0, 0))
    else:
        titre = police.render("Continuer un projet", True, pygame.Color(0, 0, 0))
    fenetre.blit(titre, ((fenetre.get_width()-titre.get_width())/2, 10))
    police_n = pygame.font.Font("./Polices/arial.TTF", 15)
    nom_projet = police_n.render("Nom du projet :", True, pygame.Color(0, 0, 0))
    surface_ecriture = pygame.Surface((250, 20))
    surface_ecriture.fill(pygame.Color(255, 255, 255))
    fenetre.blit(nom_projet, (10, 80))
    fenetre.blit(surface_ecriture, (10+nom_projet.get_width()+10, 78))
    instruction = police_n.render("(Cliquez sur la zone de saisie blanche ou appuyez sur Echap !)", True, pygame.Color(0, 0, 0))
    instruction2 = police_n.render("Attention : ne précisez pas d'extension. Elle sera rajoutée automatiquement par la suite.", True, pygame.Color(0, 0, 0))
    fenetre.blit(instruction, (5, 100))
    fenetre.blit(instruction2, (5, 150))
    suite = police_suite.render("Suite", True, pygame.Color(0, 0, 0))
    suite_sel = police_sel.render("Suite", True, pygame.Color(240, 195, 0))
    coordonnees = (fenetre.get_width()-suite.get_width()-10, fenetre.get_height()-suite.get_height()-30)
    fenetre.blit(suite, coordonnees)
    if erreur:
        if est_nouveau:
            avertissement = police_n.render("Erreur... Un projet avec ce nom existe déjà !", True, pygame.Color(0, 0, 0))
        else:
            avertissement = police_n.render("Erreur... Ce projet n'existe pas !", True, pygame.Color(0, 0, 0))
        fenetre.blit(avertissement, (20, 200))
    pygame.display.flip()
    continuer = True
    nom = ""
    while continuer:
        event = pygame.event.poll()
        if event.type == QUIT:
            return ("", -1)
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            return ("", 0)
        elif event.type == MOUSEBUTTONDOWN and est_compris_dedans(event.pos, (20+nom_projet.get_width(), 78, surface_ecriture.get_width(), surface_ecriture.get_height())):
            (nom, ok) = lecture(fenetre, (20+nom_projet.get_width(), 78, surface_ecriture.get_width(), surface_ecriture.get_height()), nom)
            if ok == -1:
                return ("", ok)
        elif event.type == MOUSEMOTION and est_compris_dedans(event.pos, (coordonnees[0], coordonnees[1], suite.get_width(), suite.get_height())):
            fenetre.blit(suite_sel, (coordonnees[0]+((suite.get_width()-suite_sel.get_width())/2), coordonnees[1]+((suite.get_height()-suite_sel.get_height())/2)))
            pygame.display.flip()
        elif event.type == MOUSEMOTION and est_compris_dedans((event.pos[0]-event.rel[0], event.pos[1]-event.rel[1]), (coordonnees[0], coordonnees[1], suite.get_width(), suite.get_height())) and not est_compris_dedans(event.pos, (coordonnees[0], coordonnees[1], suite.get_width(), suite.get_height())):
            fenetre.fill(pygame.Color(0, 127, 255), (coordonnees[0], coordonnees[1], suite.get_width(), suite.get_height()))
            fenetre.blit(suite, coordonnees)
            pygame.display.flip()
        elif event.type == MOUSEBUTTONDOWN and est_compris_dedans(event.pos, (coordonnees[0], coordonnees[1], suite.get_width(), suite.get_height())):
            return (nom, 1)
        pygame.time.delay(10)
    return (nom, 1)

def lecture(fenetre, rectangle, nom):
    position = len(nom)
    fenetre.fill(pygame.Color(255, 255, 255), rectangle)
    police = pygame.font.Font("./Polices/arial.TTF", rectangle[3]-3)
    txt = police.render(nom, True, pygame.Color(0, 0, 0))
    fenetre.blit(txt, (rectangle[0], rectangle[1]))
    curseur = pygame.Surface((1, rectangle[3]-2))
    curseur.fill(pygame.Color(0, 0, 0))
    fenetre.blit(curseur, (rectangle[0]+txt.get_width(), rectangle[1]))
    pygame.display.flip()
    continuer = True
    majuscule = 0
    while continuer:
        reaffiche = False
        event = pygame.event.poll()
        if event.type == QUIT:
            return (nom, -1)
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            return (nom, 0)
        elif event.type == MOUSEBUTTONDOWN and (not est_compris_dedans(event.pos, rectangle)):
            return (nom, 0)
        elif event.type == KEYDOWN and (event.key == K_RSHIFT or event.key == K_LSHIFT or event.key == K_CAPSLOCK):
            majuscule = 1-majuscule
            print(majuscule)
        elif event.type == KEYUP and (event.key == K_RSHIFT or event.key == K_LSHIFT or event.key == K_CAPSLOCK):
            majuscule = 1-majuscule
        elif event.type == KEYDOWN and event.key == K_RETURN:
            continuer = False
        elif event.type == KEYDOWN and event.key == K_BACKSPACE:
            if len(nom) > 0:
                nom = nom[:position-1]+nom[position:]
                position -= 1
                reaffiche = True
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                if position < len(nom):
                    position += 1
                    reaffiche = True
            elif event.key == K_LEFT:
                if position > 0:
                    position -= 1
                    reaffiche = True
            else:
                car = quel_caractere(event.key, majuscule)
                if position != 0 and position != len(nom):
                    nom = nom[:position]+car+nom[position:]
                elif position == 0:
                    nom = car+nom
                else:
                    nom = nom+car
                if car != "":
                    position += 1
                    reaffiche = True
                    #print(nom[:position], nom[position:]) debuggage
        if reaffiche:
            fenetre.fill(pygame.Color(255, 255, 255), rectangle)
            if position != 0:
                txt1 = police.render(nom[:position], True, pygame.Color(0, 0, 0))
            else:
                txt1 = police.render("", True, pygame.Color(0, 0, 0))
            if position != len(nom):
                txt2 = police.render(nom[position:], True, pygame.Color(0, 0, 0))
            else:
                txt2 = police.render("", True, pygame.Color(0, 0, 0))
            fenetre.blit(txt1, (rectangle[0], rectangle[1]))
            fenetre.blit(curseur, (rectangle[0]+txt1.get_width(), rectangle[1]+1))
            fenetre.blit(txt2, (rectangle[0]+txt1.get_width()+curseur.get_width(), rectangle[1]))
            pygame.display.flip()
            #print("ok") debuggage
        pygame.time.delay(10)
    #print(nom) debuggage
    return (nom, 1)
