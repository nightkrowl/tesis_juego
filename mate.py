import random
import operator

nivel = 1
vidas = 3
bien = 0
timepo = 0
aumento = 0
operadores = random.choice([operator.add, operator.sub, operator.mul, operator.div])

a=random.randint(1,10)
b=random.randint(1,10)

resultado = operadores(a,b)

if operadores == operator.add:
    operadores = "+"
    tiempo = 10
elif operadores == operator.sub:
    operadores = "-"
    tiempo = 10
elif operadores == operator.mul:
    operadores = "*"
    tiempo = 20
elif operadores == operator.div:
    operadores = "/"
    tiempo = 20

#nivel
#vidas

print "La operacion es:", a, operadores, b, "="

usuario = input("El resultado es? :")

if resultado == usuario:
    print "Bien!"
    print "El resultado es: ", resultado
    #bien += 1
    #aumento += 1
else:
    print "Incorrecto :("
    print "La respuesta era: ", resultado
    #vidas -= 1
    #break

    
while tiempo > 0:  
    tiempo -= 1 

    print tiempo
    if tiempo == 0:
        break

#if aumento == 5:
    #operadores.append(operator.mul)


#if aumento == 10:
    #operadores.append(operator.div)


#if bien == 5:
    #nivel += 1
    #vidas += 1

#if vidas == 0:
    #main()