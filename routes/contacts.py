from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.contacts import Contacts
from utils.db import db
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import send_file
from io import BytesIO
import pandas as pd

contacts=Blueprint('contacts', __name__)

@contacts.route("/")
def home():
    contacts_list=Contacts.query.all()
    return render_template('index.html', contacts_list=contacts_list)

@contacts.route('/new', methods=['GET','POST'])
def add_contacts():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']

        try:

            contacts_new=Contacts(name,email,phone)
            db.session.add(contacts_new)
            db.session.commit()

            flash('contacto guardado exitosamente :) !!')
            return redirect(url_for('contacts.home'))
        except Exception as e:
            return f'no se pudo guardar el contacto {e}'
        
        



        

    




@contacts.route("/update/<id>", methods=['GET','POST'])
def update(id):
    contact=Contacts.query.get(id)
    if request.method=='POST':
        
        contact.name=request.form['name']
        contact.email=request.form['email']
        contact.phone=request.form['phone']
        db.session.commit()
        flash('contacto actualizado exitosamente :) !!') 
        return redirect(url_for('contacts.home'))
    return render_template('update.html', contact=contact)
        

   
    


@contacts.route("/delete/<id>" )
def delete(id):
    print(id)
    contact=Contacts.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    flash('contacto eliminado exitosamente :) !!')

    
    return redirect(url_for('contacts.home'))














@contacts.route('/reporte_pdf')
def reporte_pdf():
    # Obtener los datos de la base de datos
    contacts_list = Contacts.query.all()
    
    # Crear un objeto en memoria para el PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Escribir en el PDF
    p.drawString(100, 750, "Reporte de Contactos:")
    
    y_position = 730
    for contact in contacts_list:
        p.drawString(100, y_position, f'{contact.name} - {contact.email} - {contact.phone}')
        y_position -= 20  # Decrementar la posición para la siguiente línea
    
    p.showPage()
    p.save()
    
    # Regresar el archivo PDF como respuesta
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="reporte_contactos.pdf", mimetype='application/pdf')







@contacts.route('/reporte_excel')
def reporte_excel():
    # Obtener los datos de la base de datos
    contacts_list = Contacts.query.all()
    
    # Convertir los datos a un DataFrame de Pandas
    data_dict = [{"Nombre": contact.name, "Correo": contact.email, "Teléfono": contact.phone} for contact in contacts_list]
    df = pd.DataFrame(data_dict)
    
    # Guardar el DataFrame en un archivo Excel en memoria
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    
    # Enviar el archivo Excel como respuesta
    return send_file(output, as_attachment=True, download_name="reporte_contactos.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')






@contacts.route('/reporte_txt')
def reporte_txt():
    # Obtener los datos de la base de datos
    contacts_list = Contacts.query.all()
    
    # Crear un archivo TXT en memoria
    output = BytesIO()
    for contact in contacts_list:
        output.write(f'{contact.name} - {contact.email} - {contact.phone}\n'.encode('utf-8'))
    
    output.seek(0)
    
    # Enviar el archivo TXT como respuesta
    return send_file(output, as_attachment=True, download_name="reporte_contactos.txt", mimetype='text/plain')