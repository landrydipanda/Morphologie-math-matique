# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 20:25:11 2019

@author: CAUCHY
"""
import math
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def calcul_histogram(img):
    w,h=img.size
    #Convertion en niveau de gris 
    img_g=img.convert("L")
    #conversion en un tableaux de pixels 
    im=np.array(img_g)
    #tableaux d'histograme 
    tab=[0]*(256)
    #calcul d'histogramme : 
    for i in range(w):
        for j in range(h):
            k=im[i][j]
            tab[k]=tab[k]+1
    return tab
def affiche_histogram(img):
    im=calcul_histogram(img)
    #im est un tableaux à 256 elements
    for i in range(256):
        plt.plot([i,i],[0,im[i]])
    plt.figure
    plt.show()
    
#..........................Etirement d'histogramme : 
def min_pixels(img):
    w,h=img.size
    img_g=img.convert("L")
    im=np.array(img_g)
    min=255
    for i in range(w):
        for j in range(h):
            if im[i][j]<=min:
                min=im[i][j]
    return min
def max_pixels(img):
    w,h=img.size
    img_g=img.convert("L")
    im=np.array(img_g)
    max=0
    for i in range(w):
        for j in range(h):
            if im[i][j]>=max:
                max=im[i][j]
    return max

def etirement_hist(img):
    min=min_pixels(img)
    max=max_pixels(img)
    w,h=img.size
    img_g=img.convert("L")
    im=np.array(img_g)
    #creation d'une nouvelle image en RGB
    im_new_rgb=Image.new("RGB",(w,h))
    #Convertion de nouvelle image en niveau de gris
    im_new_g=im_new_rgb.convert("L")
    #convertion de la nouvelle image en tablaux de pixels : 
    im_new=np.array(im_new_g)
    #Creation de l'image etire a partir de la nouvelle image qu'on vient de creer :
    for i in range (w):
        for j in range(h):
            im_new[i][j]=(255*(im[i][j]-min))//(max-min)
    #reconversion du tableaux d'images en images de pixels 
    im_etire=Image.fromarray(im_new)
    return im_etire

#---------->Egalisateur d'histogramme : 
    #Pour ameliorer le constraste qui caracterise la repartition de lumière 
def egalisateur_hist(img):
    w,h=img.size
    img_g=img.convert("L")
    im=np.array(img_g)
    #recuperation du calcul d'histogramme : 
    hist=[0]*256
    hist=calcul_histogram(img)
    #definition et calcul de histogramme cummulée normalisée : 
    hist_cum_nor=[0]*256; #Elle va contenir notre tableau d'histogramme normaliser
    hist_cum_nor[0]=hist[0]
    hist_cum_nor[0]=hist_cum_nor[0]//256
    for i in range(1,256):
        for k in range(0,i+1):
            hist_cum_nor[i]=hist_cum_nor[i]+hist[k]
        #normalisation : 
        hist_cum_nor[i]=hist_cum_nor[i]//256 
    #creation d'un tableaux de pixels 
    im_new_rgb=Image.new("RGB",(w,h))
    #"convertion en niveaux de gris
    im_new_g=im_new_rgb.convert("L")
    im_new=np.array(im_new_g)
    #Application transformation de coordonées : 
    for i in range(w):
        for j in range(h):
            im_new[i][j]=hist_cum_nor[0]
            if im[i][j]>0:
                for k in range(1,((im[i][j])+1)):
                    im_new[i][j]=im[i][j]+hist_cum_nor[k]
        im_new[i][j]=im_new[i][j]*255
    #Transformation en image de pixel 
    im_ega=Image.fromarray(im_new)
    return im_ega

#..................................binarisation de l'image........................... 
  #Moments statique  
def moments_statique(img):
    hist=[0]*256
    hist=calcul_histogram(img)
    #calcul de la somme des pixels total dans une image 
    somme=0
    for i in range (256):
        somme=somme+hist[i]
    m=[0]*4
    for i in range(4):
        for k in range(256):
            m[i]=m[i]+math.pow(hist[k],i)
        m[i]=m[i]//256
    return m
    #coefficients de newton
def coeff_newton(img):
    m=[0]*4
    m=moments_statique(img)
    c=[0]*2
    c[1]=(m[1]*m[2]-m[0]*m[3])//(m[0]*m[2]-math.pow(m[1],2))
    c[0]=(-m[2]-c[1]*m[1])//m[0]
    return c
def determination_seuil(img):#par: coeff de Newton
    #calcul du discriminant à l'aide des coedd de newton : 
    c=[0]*2
    c=coeff_newton(img)
    d=(math.pow(c[1],2))-4*c[0]
    x1=(-c[1]-math.sqrt(d))//2
    x2=(-c[1]+math.sqrt(d))//2
    seuil=(x1+x2)//2
    return seuil

def seuillage(img):
    w,h=img.size
    im_g=img.convert("L")
    im=np.array(im_g)
    print("Comment voudriez vous effectuer votre seuillage \n?")
    print("1. De facon analytique en determinant le seuil")
    print("2. Par calcul interpolaire")
    choix=input("votre choix?")
    if choix==1:
        seuil=print("veillez entrer votre seuil")
    else:
        seuil=determination_seuil(img)
    #seuillage : :
    for i in range (w):
        for j in range (h):
            if im[i][j]<seuil:
                im[i][j]=0
            else:
                im[i][j]=255
    #on retourne l'image : 
    im_binarise=Image.fromarray(im)
    return im_binarise
                    
#......................................fin seuillage ..........................................  
    
#................Operations d'addition et se soustraction sur les images.......................... 
    #Addition de deux images
def addition_deux_images(img1,img2):
    w,h=img1.size
    #parametrage image resultant 
    img=Image.new("RGB",(w,h))
    im_g=img.convert("L")
    im=np.array(im_g)
    im1_g=img1.convert("L")
    im2_g=img2.convert("L")
    im1=np.array(im1_g)
    im2=np.array(im2_g)
    for i in range(h):
        for j in range(w):
            im[i][j]=im1[i][j]+im2[i][j]
            if im[i][j]==2:
                im[i][j]=1     
    #on retourne l'image nouvelle 
    im_add=Image.fromarray(im)
    return im_add
    #Soustraction de img1 par img2 : 
def soustraire_deux_images(img1,img2):
    w,h=img1.size
    #parametrage image resultant 
    img=Image.new("RGB",(w,h))
    im_g=img.convert("L")
    im=np.array(im_g)
    im1_g=img1.convert("L")
    im2_g=img2.convert("L")
    im1=np.array(im1_g)
    im2=np.array(im2_g)
    for i in range(h):
        for j in range(w):
            im[i][j]=im1[i][j]-im2[i][j]
            if im[i][j]<0:
                im[i][j]=0     
    #on retourne l'image nouvelle 
    im_sous=Image.fromarray(im)
    return im_sous
#.......................fin operations Addition et soustraction  .......................................
               
#........................Gestion de l'élement structurant : ........................ 
    #enregistrement de l\'element structurant par l'utilisateur : 
def element_structurant() :
    ligne_str=input("Entrer le nombre de ligne de la matrice !!  \n")
    ligne=int(ligne_str)
    colonne_str=input("Entrer le nombre de colonne de la matrice !! \n")
    colonne=int(colonne_str)
    masque=[[0]*colonne for i in range(int(ligne))] #declaration du masque 
    print("\n vous aller entrer les differents coefficients de la matrice defissant l'element structurant:\n")
    for i in range(ligne):
        for j in range(colonne):
            num=input("Entrer l'element de la matrice N° [{}][{}] : ".format(i,j))
            masque[i][j]=int(num)
    return ligne,colonne,masque
    #Recuperation du centre de l'element structurant : il est defini par N° de ligne et de colonne de sa matrice  
def centre_element_structurant():
    print("Renseigner la position du centre de l'element structurant :  !! on commence a 0 \n")
    ligne=input("Renseigner le numero de ligne de la matrice du masque \n")
    colonne=input("Renseigner le numero de colonne de la matrice du masque \n")
    centre=[0]*2
    centre[0]=int(ligne)
    centre[1]=int(colonne)
    return centre
#..............................Fin gestion de l'element structurant..................................

#.....................Parcours en profondeur de la matrice de convolution avec similitude à celle de l'image
    #on compte les et logique à 1      
#chercher à generaliser les differents parcours possible : : :
    #renvoie 0 si elle ne trouve rien, 1 si elle trouve au moins 1 elmnt et 2 si elle trouve tous les elemnts 
#ligne_im , colonne_im sont les coordonées du pixel de l'image dont on veut verifier une transformation  
def parcours_en_profondeur(img,ligne_im,colonne_im,masque,width_m,height_m,centre): 
#on recupere la taille de l'image et l'a transforme en tableaux d'images : 
    w,h=img.size #w,h largeur et hauteur de l'image
    im_g=img.convert("L")
    im=np.array(im_g)
     # nombre de pixels verifiant le et logique
    nb_pixel=0 
#Parcours en profondeur du masque sur chaque pixel de l'image : 
    for i in range(width_m):
        for j in range(height_m):
            x_image=(ligne_im-centre[0])+i
            y_image=(colonne_im-centre[1])+j
            #convolution par masque partielle : 
            if ((x_image>=0) and (x_image<h)) and ((y_image>=0) and (y_image<w)):
                #verfication du Et logique
                if(im[x_image][y_image]==masque[i][j]):     
                    nb_pixel=nb_pixel+1
    return nb_pixel

#Methode qui permet de compter le nombre de pixel à 1 d'une matrice de convolution $
    #elle va le lien entre matrice de convolution et element structurant
def nb_pixels_signi_masque(masque,width,height):
    #width, height  : nombres de lignes et le nombre de colonnes respectivement : 
    nb=0
    for i in range(width):
        for j in range(height):
            if masque[i][j]==255 or masque[i][j]==0 :
                nb=nb+1
    return nb
                
#..........................Fin parcours en profondeur.....................................................

#................Transformation fond de l'image :................................
def transforme_noir_sur_fond_blanc(img) :
    im_g=img.convert("L")
    im=np.array(im_g)
    w,h=img.size
    for i in range(h):
        for j in range(w):
            if im[i][j]==255:
                im[i][j]=0
            else:
                im[i][j]=255
    im_new=Image.fromarray(im)
    return im_new
    
# ...........Application à l'erosion,dilation,ouverture,fermeture sur une grille carrer..................

#Application à l'erosion :
def erosion_grille_carrer(img,largeur_m,hauteur_m,masque,centre):
    w,h=img.size
#On recupere le nombre de pixel à 1 de l'elemnt structurant
    nb_masque=nb_pixels_signi_masque(masque,largeur_m,hauteur_m)
    im_g=img.convert("L")
    im=np.array(im_g)
    #copie de l'image
    im_copie=im
    for i in range(h):
        for j in range(w):
            nb=parcours_en_profondeur(im_g,i,j,masque,largeur_m,hauteur_m,centre)
            if nb!=nb_masque:
                im_copie[i][j]=0
    #On retranforme notre tableaux d'images en images : 
    im_ero=Image.fromarray(im_copie)
    return im_ero
#Application à la dilatation : 
def dilatation_grille_carrer(img,largeur_m,hauteur_m,masque,centre):
    w,h=img.size
    im_g=img.convert("L")
    im=np.array(im_g)
    #copie de l'image
    im_copie=im
    for i in range(h):
        for j in range(w):
            nb=parcours_en_profondeur(im_g,i,j,masque,largeur_m,hauteur_m,centre)
            if nb>=1:
                im_copie[i][j]=255
    #On retranforme notre tableaux d'images en images : 
    im_dila=Image.fromarray(im_copie)
    return im_dila
    
#Application à l'ouverture :
def ouverture_grille_carrer(img,largeur_m,hauteur_m,masque,centre):
    w,h=img.size
    #centre de B tchet : 
    centre_tchet=[0]*2
    centre_tchet[0]=int(math.fabs(centre[0]-(largeur_m-1)))
    centre_tchet[1]=int(math.fabs(centre[1]-(hauteur_m-1)))
#Erosion 
    im_erode=erosion_grille_carrer(img,largeur_m,hauteur_m,masque,centre)
#Dilatation de l'image erode avec le B tchet :
    im_ouvert=dilatation_grille_carrer(im_erode,largeur_m,hauteur_m,masque,centre_tchet)
    return im_ouvert
#Application a la fermeture 
def fermeture_grille_carrer(img,largeur_m,hauteur_m,masque,centre):  
    w,h=img.size
    #centre de B tchet : 
    centre_tchet=[0]*2
    centre_tchet[0]=int(math.fabs(centre[0]-(largeur_m-1)))
    centre_tchet[1]=int(math.fabs(centre[1]-(hauteur_m-1)))
#Dilation 
    im_dilate=dilatation_grille_carrer(img,largeur_m,hauteur_m,masque,centre)
#Erosion de l'image dilate avec le B tchet :
    im_fer=erosion_grille_carrer(im_dilate,largeur_m,hauteur_m,masque,centre_tchet)
    return im_fer

#####......Fin gestion erosion,dilation,ouverture,fermeture sur grille carrer..........................
    
#Methode pour former un masque paire  a partir d'un masque impaire : 
def masque_paire_def(largeur_m,hauteur_m,masque_impaire):
    masque_paire=masque_impaire
    for i in range(largeur_m):
        for j in range(hauteur_m):
            if masque_impaire[i][j]==-1:
                masque_paire[i][j]=255
                masque_paire[i][int(math.fabs(j-hauteur_m+1))]=-1
    return masque_paire
#...................Gestion erosion,dilation,ouverture,fermeture sur grille Hexagonale..................
#definition erosion  grille hexagonale :    
def erosion_grille_hexagonale(img,largeur_m,hauteur_m,masque_impaire,centre):
    #On enregistre le nombre d'elements à 1 du masque :
    nb_masque=nb_pixels_signi_masque(masque_impaire,largeur_m,hauteur_m)
    print("Nb masque : " +str(nb_masque)+str("\n"))
    #on onregistre le masque paire :
    masque_paire=masque_paire_def(largeur_m,hauteur_m,masque_impaire)
    w,h=img.size
    im_g=img.convert("L")
    im=np.array(im_g)
    #copie de l'image
    im_copie=im
    for i in range(h):
        for j in range(w):
            if((i+1)%2==1):
                masque=masque_impaire
            else:
                masque=masque_paire
            nb=parcours_en_profondeur(im_g,i,j,masque,largeur_m,hauteur_m,centre)
            if(nb==7):
                print("non modifie : ok\n")
            #print("nb sur pixel :"+str(nb)+str("\n"))
            if nb!=nb_masque:
                #print(nb)
                im_copie[i][j]=0
    #On reeconvertir le tableaux de pîxel en image
    im_ero=Image.fromarray(im_copie)
    return im_ero
#definition dilation grille hexagonale : 
def dilatation_grille_hexagonale(img,largeur_m,hauteur_m,masque_impaire,centre):
    #on onregistre le masque paire :
    masque_paire=masque_paire_def(largeur_m,hauteur_m,masque_impaire)
    w,h=img.size
    im_g=img.convert("L")
    im=np.array(im_g)
    #copie de l'image
    im_copie=im
    for i in range(h):
        for j in range(w):
            if((i+1)%2==1):
                masque=masque_impaire
            else:
                masque=masque_paire
            nb=parcours_en_profondeur(im_g,i,j,masque,largeur_m,hauteur_m,centre)
            if nb>=1:
                im_copie[i][j]=255
    #On reeconvertir le tableaux de pîxel en image
    im_dil=Image.fromarray(im_copie)
    return im_dil
#Definition ouverture grille hexagonale :
def ouverture_grille_hexagonale(img,masque_impaire,largeur_m,hauteur_m,centre):
    w,h=img.size
#centre de B tchet : 
    centre_tchet=[0]*2
    centre_tchet[0]=int(math.fabs(centre[0]-(largeur_m-1)))
    centre_tchet[1]=int(math.fabs(centre[1]-(hauteur_m-1)))
#Erosion 
    im_erode=erosion_grille_hexagonale(img,largeur_m,hauteur_m,masque_impaire,centre)
#Dilatation de l'image erode avec le B tchet :
    im_ouvert=dilatation_grille_hexagonale(im_erode,largeur_m,hauteur_m,masque_impaire,centre_tchet)
    return im_ouvert
#definition de la fermeture grille hexagonale
def fermeture_grille_hexagonale(img,masque_impaire,largeur_m,hauteur_m,centre):
    w,h=img.size
    #centre de B tchet : 
    centre_tchet=[0]*2
    centre_tchet[0]=int(math.fabs(centre[0]-(largeur_m-1)))
    centre_tchet[1]=int(math.fabs(centre[1]-(hauteur_m-1)))
#Dilatation 
    im_dil=dilatation_grille_hexagonale(img,largeur_m,hauteur_m,masque_impaire,centre)
#erosion de l'image erode avec le B tchet :
    im_fermer=erosion_grille_hexagonale(im_dil,largeur_m,hauteur_m,masque_impaire,centre_tchet)
    return im_fermer  
#...............Fin gestion erosion,dilatation,fermeture sur une grille hexagonale ........................

###...........................Amincicement et apaisicement....................................

#.............Amincissement grille carrer : .........................
def amincissement_grille_carrer(img,largeur_m,hauteur_m,masque,centre):
    #On enregistre le nombre d'element du masque :
    nb_masque=nb_pixels_signi_masque(masque,largeur_m,hauteur_m)
    w,h=img.size
    im_g=img.convert("L")
    im=np.array(im_g)
    im_copie=im
    for i in range(h):
        for j in range(w):
            nb=parcours_en_profondeur(img,i,j,masque,largeur_m,hauteur_m,centre)
            if nb==nb_masque:
                im_copie[i][j]=0
    im_amin=Image.fromarray(im_copie)
    return im_amin

#.........Amincissement grille carrer :
def epaissisement_grille_carrer(img,largeur_m,hauteur_m,masque,centre):
    #On enregistre le nombre d'element du masque :
    nb_masque=nb_pixels_signi_masque(masque,largeur_m,hauteur_m)
    w,h=img.size
    im_g=img.convert("L")
    im=np.array(im_g)
    im_copie=im
    for i in range(h):
        for j in range(w):
            nb=parcours_en_profondeur(img,i,j,masque,largeur_m,hauteur_m,centre)
            if nb==nb_masque:
                im_copie[i][j]=255
    im_epai=Image.fromarray(im_copie)
    return im_epai
#....Amincissement grille hexagonale : 
#alogorithmes paralleles, faire une copie de l'image : : 
def amincissement_grille_hexagonale(img,largeur_m,hauteur_m,masque_paire,masque_impaire,centre):
    #On enregistre le nombre d'elements à 1 du masque :
    nb_masque=nb_pixels_signi_masque(masque_impaire,largeur_m,hauteur_m)
    w,h=img.size
    im_g=img.convert("L")
    im=np.array(im_g)
    #Copie du tableaux de matrice de l'image : programmation parallèles :
    im_copie=im
    for i in range(h):
        for j in range(w):
            if((i+1)%2==1):
                masque=masque_impaire
            else:
                masque=masque_paire
            nb=parcours_en_profondeur(im_g,i,j,masque,largeur_m,hauteur_m,centre)
            if nb==nb_masque:
                print(str(nb)+str("\n"))
                im_copie[i][j]=0
    #On reeconvertir le tableaux de pîxel en image
    im_amin=Image.fromarray(im_copie)
    return im_amin
#Epaissisement grille hexagonale : 
def epaississement_grille_hexagonale(img,largeur_m,hauteur_m,masque_paire,masque_impaire,centre):
    #On enregistre le nombre d'elements à 1 du masque :
    nb_masque=nb_pixels_signi_masque(masque_impaire,largeur_m,hauteur_m)
    #on onregistre le masque paire :
    w,h=img.size
    im_g=img.convert("L")
    im=np.array(im_g)
    im_copie=im
    for i in range(h):
        for j in range(w):
            if((i+1)%2==1):
                masque=masque_impaire
            else:
                masque=masque_paire
            nb=parcours_en_profondeur(im_g,i,j,masque,largeur_m,hauteur_m,centre)
            if nb==nb_masque:
                im_copie[i][j]=255
    #On reeconvertir le tableaux de pîxel en image
    im_epai=Image.fromarray(im_copie)
    return im_epai 
#......Gestion des masques pour configurations de  voisinages
#####.......................FIN GESTION AMINCISSEMENT ET EPAISSISSEMENT GRILLE CARRER ET HEXAGONALE


#Etape 2 :    
#methode qui permet de verifier si deux images sont identiques 
def egalite_entre_deux_image(img1,img2):
    result=1
    w,h=img1.size
    im1_g=img1.convert("L")
    im2_g=img2.convert("L")
    im1=np.array(im1_g)
    im2=np.array(im2_g)
    for i in range(h):
        for j in range(w):
            if im1[i][j]!=im2[i][j]:
                result=0
    return result 
        
##Gestionn Squeletisation par amincissement homotopique avec la configuration de voisinage L

#Amincissement avec la configuration de voisinage L    
def amincissement_grille_hexagonale_L(indi,img):    
    centre=[1,1]
    #Amincisssement homotopique grille hexagonale : 
#Enregistrement des 6 configurations de voisinage L : 
    L_impaire=[0]*6
    L_paire=[0]*6
#Enregistrement impaires :
    L_impaire[0]=[[255,255,-1],[-2,255,-2],[0,0,-1]]
    L_impaire[1]=[[255,-2,-1],[255,255,0],[-2,0,-1]]
    L_impaire[2]=[[-2,0,-1],[255,255,0],[255,-2,-1]]
    L_impaire[3]=[[0,0,-1],[-2,255,-2],[255,255,-1]]
    L_impaire[4]=[[0,-2,-1],[0,255,255],[-2,255,-1]]
    L_impaire[5]=[[-2,255,-1],[0,255,255],[0,-2,-1]]
#Enregistrement paire : 
    L_paire[0]=[[-1,255,255],[-2,255,-2],[-1,0,0]]
    L_paire[1]=[[-1,255,-2],[255,255,0],[-1,-2,0]]
    L_paire[2]=[[-1,-2,0],[255,255,0],[-1,255,-2]]
    L_paire[3]=[[-1,0,0],[-2,255,-2],[-1,255,255]]
    L_paire[4]=[[-1,0,-2],[0,255,255],[-1,-2,255]]
    L_paire[5]=[[-1,-2,255],[0,255,255],[-1,0,-2]]

    return amincissement_grille_hexagonale(img,3,3,L_paire[indi],L_impaire[indi],centre)
    
#Sequeletisation par amincissement homotopique avec la configurtion de voisinage L
def squeletisation_amincissement_idempotence(img):
    im_itere=[]
    im_itere.append(amincissement_grille_hexagonale_L(0,img))
    im_itere.append(amincissement_grille_hexagonale_L(1,img))
    j=1
    i=1
    while (im_itere[-1])!=(im_itere[-2]):
        j=j+1
        i=i+1
        if j==6:
            j=0
        im_itere.append(amincissement_grille_hexagonale_L(j,im_itere[i-1]))
    print("Nb total iteration : "+str(i))     
    #On retourne la derniere image
    return im_itere[-1]
    

#......................Squeletissation par la formule de lantuejoul : : : .............................
#On a bessoin de deux masques de convolution , la taille de la matrice c'est 2k+1
def def_disque_taille_k(k):
    taille_masque=2*k+1
    disque=[[0]*(taille_masque) for i in range(taille_masque)]
    #Remplissage naif : : :
    for i in range(taille_masque):
        for j in range(taille_masque):
            disque[i][j]=255
    #Gestion de la grille hexagonale :
    if taille_masque>0: 
        compt=0
        while compt<k:
            disque[compt][(taille_masque-1)-compt]=-1
            disque[(taille_masque-1)-compt][(taille_masque-1)-compt]=-1
            compt=compt+1
    return disque            
#var: k , c'est la taille du disque , elle retourne le resultat par l'image ayant subit l'iteration
def iteration_lantuejoul(img,k):
    #definition du disque de taille 1 :
    disque_unite=[[1,1,-1],[1,1,1],[1,1,-1]]
    #definition du centre du disque :
    centre_disque=[0]*2
    centre_disque[0]=k
    centre_disque[1]=k
    #definition centre du disque unite
    centre_unite=[0]*2
    centre_unite[0]=1
    centre_unite[1]=1
    #recuperation du disque :
    disque=def_disque_taille_k(k)
    #1er operation erosion par le disque de taille k 
    im_ero_disque=erosion_grille_hexagonale(img,2*k+1,2*k+1,disque,centre_disque)
    #Ouverture par le disque de taille 1 de l'image erode :  
    im_ouvert_disque_unite=ouverture_grille_hexagonale(im_ero_disque,disque_unite,3,3,centre_unite)
    # difference entre erode et l'ouvert de l'erode :
    im_result=soustraire_deux_images(im_ero_disque,im_ouvert_disque_unite)
    return im_result

#squeletissation : : :
def squeletisation_lantuejoul_idempotence(img):
    im_itere=[]
    im_itere.append(iteration_lantuejoul(img,0))
    im_itere.append(iteration_lantuejoul(img,1))
    i=1
    while (im_itere[-1])!=(im_itere[-2]):
        i=i+1
        im_itere.append(iteration_lantuejoul(im_itere[i-1],i))
    print("Nb total iteration : "+str(i))     
    #On retourne la derniere image
    return im_itere[-1]
    

# ***************************TESTS DES ALGORIHMES **********************************

morpho=Image.open("im_sq.png")
morpho_g=morpho.convert("L")
morpho_g.show()
morpho_tab=np.array(morpho_g)
w,h=morpho_g.size
for i in range(h):
    for j in range(w):
        if morpho_tab[i][j]<80:
            morpho_tab[i][j]=0
        else:
            morpho_tab[i][j]=255
for i in range(h):
    for j in range(w):
        if morpho_tab[i][j]==255:
            morpho_tab[i][j]=0
        else:
            morpho_tab[i][j]=255
morpho_new=Image.fromarray(morpho_tab)
#morpho_new.show()
morpho_sq=squeletisation_amincissement_idempotence(morpho_new)

#morpho_squelette=squeletisation_amincissement_idempotence(morpho_new)
morpho_sq.show()

"""
#on renseigne le masque et sa taille :
largeur_m,hauteur_m,masque_impaire=element_structurant()
#On renseigne le centre du masque : 
centre=centre_element_structurant()
"""

    #sera gerer dans lerosion et la dilation , on va entrer un masque , et le 2nd masque serait definir a partir 
    #du 1er , il sera differents : l'un pour les lignes paires et l'autre impaires .
#..................................................Applications..................................... 
    #Chargement de l'image : 
"""
lenna=Image.open("lenanoirsurblanc.png")
affiche_histogram(lenna)

lenna_etire=etirement_hist(lenna)
lenna_etire.show()
affiche_histogram(lenna_etire)

lenna_ega=egalisateur_hist(lenna)
lenna_ega.show()
affiche_histogram(lenna_ega)
"""

