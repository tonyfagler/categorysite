# app.py

from flask import Flask, render_template, request, redirect
import mariadb
import datetime

app = Flask(__name__)

# Database connection settings
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'demo'
DB_PASSWORD = 'd3m0p4ssw0rd'
DB_DATABASE = 'contact'

# Create a database connection
conn = mariadb.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)
cursor = conn.cursor()

# Database creation script
def create_database():
    cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(DB_DATABASE))
    cursor.execute('USE {}'.format(DB_DATABASE))
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            phone_number VARCHAR(12) NOT NULL,
            topic_of_discussion VARCHAR(255) NOT NULL,
            follow_up_date DATE NOT NULL
        )
    ''')

# Database management functions
def add_contact(first_name, last_name, phone_number, topic_of_discussion, follow_up_date):
    sql = '''
        INSERT INTO contacts (first_name, last_name, phone_number, topic_of_discussion, follow_up_date)
        VALUES (?, ?, ?, ?, ?)
    '''
    cursor.execute(sql, (first_name, last_name, phone_number, topic_of_discussion, follow_up_date))
    conn.commit()

def edit_contact(contact_id, first_name, last_name, phone_number, topic_of_discussion, follow_up_date):
    sql = '''
        UPDATE contacts SET first_name=?, last_name=?, phone_number=?, topic_of_discussion=?, follow_up_date=?
        WHERE id=?
    '''
    cursor.execute(sql, (first_name, last_name, phone_number, topic_of_discussion, follow_up_date, contact_id))
    conn.commit()

def delete_contact(contact_id):
    sql = 'DELETE FROM contacts WHERE id=?'
    cursor.execute(sql, (contact_id,))
    conn.commit()

def get_contacts(search_term=''):
    sql = 'SELECT * FROM contacts WHERE first_name LIKE ? OR last_name LIKE ? ORDER BY last_name'
    cursor.execute(sql, ('%{}%'.format(search_term), '%{}%'.format(search_term)))
    return cursor.fetchall()

def export_contacts(filename):
    sql = 'SELECT * FROM contacts ORDER BY last_name'
    cursor.execute(sql)
    contacts = cursor.fetchall()

    with open(filename, 'w') as file:
        file.write('First Name,Last Name,Phone Number,Topic of Discussion,Follow-up Date\n')
        for contact in contacts:
            file.write('{},{},{},{},{}\n'.format(contact[1], contact[2], contact[3], contact[4], contact[5]))

def import_contacts(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines[1:]:
        data = line.strip().split(',')
        first_name, last_name, phone_number, topic_of_discussion, follow_up_date = data
        add_contact(first_name, last_name, phone_number, topic_of_discussion, follow_up_date)

# Routes and views
@app.route('/')
def index():
    search_term = request.args.get('search', '')
    contacts = get_contacts(search_term)
    return render_template('index.html', contacts=contacts, search_term=search_term)

@app.route('/add', methods=['GET', 'POST'])
def add_contact_page():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        topic_of_discussion = request.form['topic_of_discussion']
        follow_up_date = request.form['follow_up_date']
        add_contact(first_name, last_name, phone_number, topic_of_discussion, follow_up_date)
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact_page(contact_id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        topic_of_discussion = request.form['topic_of_discussion']
        follow_up_date = request.form['follow_up_date']
        edit_contact(contact_id, first_name, last_name, phone_number, topic_of_discussion, follow_up_date)
        return redirect('/')
    contact = get_contacts()[contact_id - 1]
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:contact_id>')
def delete_contact_route(contact_id):
    delete_contact(contact_id)
    return redirect('/')

@app.route('/export')
def export_contacts_route():
    export_contacts('contacts.csv')
    return redirect('/')

@app.route('/import')
def import_contacts_route():
    import_contacts('contacts.csv')
    return redirect('/')

# Main
if __name__ == '__main__':
    create_database()
    app.run(debug=True)
