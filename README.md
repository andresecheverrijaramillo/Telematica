# Telematica
## Lab 6/ EMR  
En el laboratorio 6 cree el bucket y el cluster tal como indicaba la guia  
Luego de que se crearan me conecte  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/eec3a5bc-f083-44cc-ab98-c1679992ceb0)  
Y cree la coneccion para abrir el hadoop desde mi local  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/da0d336c-f575-470e-bacd-434c538e5fe7)  
Al cual tambien subi de manera correcta no solo 1 si no que dos archivos (uno fue por accidente)  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/308d3f7e-1952-4ba3-a5c5-6326b0fa6c8f)  
Luego cree la carpeta de test2 por comandos y revise que estubiera bien  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/bc2ec75b-22c1-4755-99f1-091ff32b4831)  
Luego Cree el txt2 como me indican y lo movi a local
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/16ddab4a-5dd0-4c8c-ad92-ac9a0064b386)  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/8b9c641f-46bf-4561-9e64-64364e633f4b)  
## Laboratorio/ Mapreduce con python y mrjob  
Lo primero que hare sera configurar que con el awscli de mi computador pueda crear el closter, eso lo hago de esta forma:  
Primero me aseguro instalar awscli en mi computador con el usuario que vaya a trabajar, tras esto entro a la carpeta de aws que esta en el siguiente path: C:\Users\EQUIPO\.aws  
Tras esto modifico en el archivo credentials para que tenga los datos que nos da aws al iniciar el laboratorio ej:  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/a1018253-5a5a-4578-b80b-4bbb2221127b)  
Despues se correra la siguiente linea de ssh
```ssh
aws emr create-cluster --release-label emr-6.10.0 --instance-type m4.large --instance-count 3 --log-uri s3://aecheverrj-lab-emr/logs --use-default-roles --ec2-attributes KeyName=emr-key,SubnetId=subnet-0defc3ca9705c7a23 --no-termination-protected
```
Este se encarga de crear un cluster emr de version 6.10 con instacias m4.large y va a ponerlo con la subtnet subnet-0defc3ca9705c7a23 que aparece como una de las subnets publicas de mi cuenta, y por ultimo la llave de acceso es emr-key que fue la que se uso en el lab pasado, esto nos dara la siguiente informacion  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/bf65d706-a741-439d-8de1-45e3e5ec845f)  
Aca podemos ver el id del cluster que creamos ya es esperar a que se inicie  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/5fd1cd8e-9492-47dd-9190-26824c68c414)  
Tras iniciar nos conectamos como se hizo en el anterior lab, ya para este laboratorio necesitamos instalar github porque necesitamos traer una gran cantidad de archivos entonces se hara el siguiente comando  
```ssh
sudo yum install git
```
luego clonamos el repositorio  
```ssh
git clone https://github.com/ST0263/st0263-2023-1.git
```
luego nos metemos en donde esta el codigo  
```ssh
cd st0263-2023-1/Laboratorio\ N6-MapReduce/wordcount/
```
y vamos a cambiar el codigo de wordcount con el codigo  
```ssh
sudo nano wordcount-local.py
```
Y lo vamos a cambiar por el siguiente codigo
```python3
#!/usr/bin/python

import os
import sys
import glob
import codecs

inputdir = "."

if len(sys.argv) >= 2:
    inputdir = sys.argv[1]

def processdir(dir):
    dirList = glob.glob(dir)
    wordcount = {}
    for f in dirList:
        wordcountfile(f, wordcount)
    for w in wordcount:
        print(w, wordcount[w])

def wordcountfile(f, wordcount):
    file = codecs.open(f, "r", "utf-8")
    for word in file.read().split():
        word = word.lower()  # Convert word to lowercase
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
    file.close()
    return wordcount

processdir(inputdir)
```
Se hizo este cambio dado que una de las lineas de codigo esta dando errores  
Y despues se corre el codigo
```ssh
python wordcount-local.py /home/hadoop/st0263-2023-1/datasets/gutenberg-small/*.txt | sudo tee salida-serial.txt > /dev/null more salida-serial.txt
```
Y usamos el siguiente comando para ver los resultados
```ssh
more salida-serial.txt
```
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/9bc9cca4-d867-4ea5-b2a4-2229039df5bb)
Ahora vamos a instalar python3 y MrJob
```ssh
sudo yum install python3-pip
sudo pip3 install mrjob
```
Ya vamos a testear MrJob
```
python wordcount-mr.py /home/hadoop/st0263-2023-1/datasets/gutenberg-small/*.txt
```
Ya vamos a hacer el reto de este laboratorio que es correrlo en hadoop, para esto vamos a copiar los dataset a hadoop de esta manera
```ssh
hdfs dfs -mkdir /user/admin
hdfs dfs -copyFromLocal /home/hadoop/st0263-2023-1/datasets/ /user/admin/
```
Ahi creamos la carpeta del admmin en hadoop y copiamos los dataset, despues vamos a correr el codigo con esta linea
```ssh
python wordcount-mr.py hdfs:///user/admin/datasets/gutenberg-small/*.txt -r hadoop --output-dir hdfs:///user/admin/result3 
```
Al correrlo sale esto  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/761b8113-55e6-44de-a294-0aa9fc08d15c)
Y sabemos que funciona porque si hacemos 
```ssh
hdfs dfs -cat /user/admin/result3/part-00000
```
vamos a entrar al resultado del primer txt  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/7b3a0b83-46e4-4ea8-80b5-f6f0bda22add)

Y con esto finalizamos este laboratorio y reto
## Reto de codigo
Ya en este reto vamos a hacer lo siguiente, primero vamos a copiar el codigo que se desarrollo en el home
```ssh
sudo git clone https://github.com/andresecheverrijaramillo/Telematica.git
```
Luego vamos a crear la carpeta de los resultados asi, agregandole un /punto# depende del punto que estemos haciendo
```ssl
hdfs dfs -mkdir /user/admin/reto3
```
A
Y vamos a correr los codigos de esta manera
```ssh
python A.py hdfs:///user/admin/datasets/otros/dataempleados.txt -r hadoop --output-dir hdfs:////user/admin/reto3/punto1/parteA
```
Si nos metemos a la carpeta user/admin/reto3/Dane-1 e inspeccionampos las partes con esto
```ssh
hdfs dfs -cat /user/admin/reto3/punto1/parteA/part-00000
hdfs dfs -cat /user/admin/reto3/punto1/parteA/part-00001
hdfs dfs -cat /user/admin/reto3/punto1/parteA/part-00002
```
Y nos debe dar esto  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/87bf325d-f9a6-4567-b265-badc4f0b8a83)
B
```ssh
python B.py hdfs:///user/admin/datasets/otros/dataempleados.txt -r hadoop --output-dir hdfs:////user/admin/reto3/punto1/parteB
```
Si nos metemos a la carpeta user/admin/reto3/Dane-1 e inspeccionampos las partes con esto
```ssh
hdfs dfs -cat /user/admin/reto3/punto1/parteB/part-00000
hdfs dfs -cat /user/admin/reto3/punto1/parteB/part-00001
hdfs dfs -cat /user/admin/reto3/punto1/parteB/part-00002
```
Y nos debe dar esto  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/a3a06065-4f99-4228-b99c-38b5399ed0bb)
C
```ssh
python C.py hdfs:///user/admin/datasets/otros/dataempleados.txt -r hadoop --output-dir hdfs:////user/admin/reto3/punto1/parteC
```
Si nos metemos a la carpeta user/admin/reto3/Dane-1 e inspeccionampos las partes con esto
```ssh
hdfs dfs -cat /user/admin/reto3/punto1/parteC/part-00000
hdfs dfs -cat /user/admin/reto3/punto1/parteC/part-00001
hdfs dfs -cat /user/admin/reto3/punto1/parteC/part-00002
```
Y nos debe dar esto  
![image](https://github.com/andresecheverrijaramillo/Telematica/assets/68928458/1847b4f3-6752-4cc3-90e0-728921fc664f)
