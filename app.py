from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to create the database table if it doesn't exist
def create_table():
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            color TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# Route to display all cars
@app.route('/')
def index():
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars')
    cars = cursor.fetchall()
    conn.close()
    return render_template('index.html', cars=cars)

# Route to add a new car
@app.route('/add', methods=['POST'])
def add_car():
    brand = request.form['brand']
    model = request.form['model']
    color = request.form['color']

    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cars (brand, model, color) VALUES (?, ?, ?)', (brand, model, color))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to delete a car
@app.route('/delete/<int:car_id>')
def delete_car(car_id):
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cars WHERE id = ?', (car_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to edit a car (displaying the form for editing)
@app.route('/edit/<int:car_id>')
def edit_car(car_id):
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars WHERE id = ?', (car_id,))
    car = cursor.fetchone()
    conn.close()
    return render_template('edit.html', car=car)

# Route to update a car after editing
@app.route('/update/<int:car_id>', methods=['POST'])
def update_car(car_id):
    brand = request.form['brand']
    model = request.form['model']
    color = request.form['color']

    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE cars SET brand = ?, model = ?, color = ? WHERE id = ?', (brand, model, color, car_id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
