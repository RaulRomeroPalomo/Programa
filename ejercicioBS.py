import Tkinter
# encoding: utf-8
from Ejercicio2 import *
import sqlite3
import tkMessageBox
from Tkinter import *
from bs4 import BeautifulSoup
import urllib2
import urllib


def abrirURL(url, file):
    file = urllib.urlopen(url).read()

def almacenarCategorias():
    abrir_url("http://www.delicatessin.com/es/Delicatessin", "categorias")
    tkMessageBox.showinfo("Datos Almacenados", "La BD se ha creado correctamente")
    conn = sqlite3.connect('categorias.db')
    conn.execute('''DROP TABLE IF EXISTS CATEGORIAS''')
    conn.execute('''CREATE TABLE CATEGORIAS
            (TITULO           TEXT    NOT NULL,
              LINK           TEXT    NOT NULL);''')

    with open("categorias") as f:
        soup = BeautifulSoup(f, "lxml")

    uls = soup.find("ul", {"class": ["tree", "dynamized"]})
    lis = uls.find_all("li")
    for categ in lis:
        titulo = categ.get_text()
        print titulo
        link = categ.a['href']
        print link
        conn.execute("INSERT INTO CATEGORIAS VALUES(?, ?);", (titulo, link));

    conn.commit()
    conn.close()

def almacenarProductos():
    almacenarCategorias()
    conn = sqlite3.connect('categorias.db')
    conn.execute('''DROP TABLE IF EXISTS PRODUCTOS''')
    conn.execute('''CREATE TABLE PRODUCTOS
                (CATEGORIA      TEXT    NOT NULL,
                LINK           TEXT    NOT NULL,
                PRECIO        TEXT    NOT NULL,
                REBAJA        TEXT    NOT NULL);''')

    cursor = conn.execute("SELECT * FROM CATEGORIAS")
    for row in cursor:
        link = row[1]

        abrir_url(link, "productos")

        with open("categorias") as f:
            soup = BeautifulSoup(f, "lxml")

        uls = soup.find("ul", {"class": "listpro"})
        lis = uls.find_all("li")
        for prod in lis:
            categoria = prod.find("div", {"class": "prod_name"}).get_text()
            print nombre
            link = prod.find("div", {"class": "prod_name"}).a['href']
            print link
            precio = prod.find("div", {"class": "price_home"}).get_text()
            print precio
            conn.execute("INSERT INTO PRODUCTOS VALUES(?, ?, ?);", (nombre, link, precio));

    conn.commit()
    conn.close()

top = Tkinter.Tk()

AC = Tkinter.Button(top, text="Almacenar Categorias", command = almacenarProductos)
#BC = Tkinter.Button(top, text="Buscar Categoria", command = buscarCategoria)

AC.pack(side = LEFT)
#BC.pack(side = LEFT)


top.mainloop()