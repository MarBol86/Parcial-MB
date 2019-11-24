#!/usr/bin/env python
import csv
from datetime import datetime
# fecha_actual=datetime.utcnow()

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap

from forms import LoginForm, RegistrarForm, SearchCountry
import processing


app = Flask(__name__)
bootstrap = Bootstrap(app)


app.config['SECRET_KEY'] = 'un string que funcione como llave'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


# Se agrega una verificación para que no haya dos nombres de usuarios iguales
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if processing.existir(formulario.usuario.data):
            flash('El nombre de usuario ya existe, eliga otro.') #
            return render_template('registrar.html', formulario=formulario)
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+', newline='') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', formulario=formulario)


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))


@app.route('/clientes', methods=['GET']) #Muestra la tabla clientes
def secreto():
    if 'username' in session:
        filas = processing.createRows()
        CantClientes = processing.contar(filas)
        encabezados = processing.createHeaders()
        return render_template('clientes.html', CantClientes = CantClientes, filas = filas, encabezados = encabezados)
    else:
        flash('Primero debes ingresar.')
        return redirect (url_for ("ingresar"))


@app.route('/search/clientes/country', methods=['GET', 'POST'])
def porPaís():
    if 'username' in session:
        formulario = SearchCountry()
        if formulario.validate_on_submit():
            newlist = processing.searchCountry(formulario.search.data)
            if newlist == []:
                return render_template('porPaís.html', formulario=formulario, mensaje = "No se encontraron resultados")
            else:
                return render_template('porPaís.html', formulario=formulario, newlist = newlist)
        return render_template('porPaís.html', formulario=formulario)
    else:
        flash('Primero debes ingresar.')
        return redirect (url_for ("ingresar"))


@app.route('/search/clientes/country/<pais>')
def resultadoPorPaís(pais):
    if 'username' in session:
        filas = processing.rowsCountry(pais)
        CantClientes = processing.contar(filas)
        encabezados = processing.createHeaders()
        return render_template('clientes.html', filas = filas, CantClientes = CantClientes, encabezados = encabezados)
    else:
        flash('Primero debes ingresar.')
        return redirect (url_for ("ingresar"))
    

@app.errorhandler(404)
def no_encontrado(e):
    if 'username' in session:
        return render_template('404.html'), 404
    else:
        flash('Probá ingresando primero, luego vemos.')
        return redirect (url_for ("ingresar"))


@app.errorhandler(500)
def error_interno(e):
    if 'username' in session:
        return render_template('500.html'), 500
    else:
       flash('Probá ingresando primero, luego vemos.')
       return redirect (url_for ("ingresar"))

if __name__ == "__main__":
    app.run(debug=True)
