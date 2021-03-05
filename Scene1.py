from raycaster import *

#parametre

h = 480 #on peut faire du 1080p mais c'est long
w = round( h * (16/9) ) #une image au format 16:9
fadeStrength = 3 #plus on tant vers 1 plus l'effet est puissant (fs >= 1)
fov = 70 #angle de vue en largeur (la hauteur de fov*9/16)

#objects
s1 = Sphere([10,0,3], 1, [255,255,255]) #Sphere de rayon 1, blanche de centre (10,0,3)
s2 = Sphere([20,0,0], 5, [0,120,255]) #Sphere de rayon 5, bleu(avec un peu de vert) de centre [20,0,0]
p = Plane([1,1,1], [50,0,-6], [255,0,0]) #un plan dont le vecteur normale est v(1,1,1) et contenant le point (50,0,-6)

objs = [s1,s2,p] #un tableau des objets

#lights
amb = [0.25,0.25,0.25] #lumière ambiante (pour les ombres)
l0 = Light([5,0,4]) #Source de lumière en (5,0,4)
l1 = Light([5,-5,4]) #Source de lumière en (5,-5,4)

lights = [l0] #un tableau des source de lumière (on peu en mettre plein)

#mise en place de la scène

cam = Camera([0,0,0], [1,0,0], fov, [w,h], lights, fadeStrength) #camera en (0,0,0) pointant vers (1,0,0)
scn = Scene(cam, objs, amb) #creation de la scene à générer (avec camera, objet, et luminosité ambiante)

img = scn.render() #rendu de l'image
#img.save('Scene1.png') #sauvegarde de l'image