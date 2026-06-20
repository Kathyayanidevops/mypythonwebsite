from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret123'

# Movie data
movies = [
    {'id': 1, 'title': 'Dune 2', 'genre': 'Sci-Fi', 'rating': 8.7, 'image': '🎬', 'showtimes': ['10:00', '13:30', '17:00']},
    {'id': 2, 'title': 'The Batman', 'genre': 'Action', 'rating': 8.2, 'image': '🦇', 'showtimes': ['11:00', '14:30', '18:00']},
    {'id': 3, 'title': 'Interstellar', 'genre': 'Sci-Fi', 'rating': 9.0, 'image': '🚀', 'showtimes': ['12:00', '15:30', '19:00']},
    {'id': 4, 'title': 'Shawshank', 'genre': 'Drama', 'rating': 9.3, 'image': '🏛️', 'showtimes': ['10:30', '14:00', '17:30']},
    {'id': 5, 'title': 'Inception', 'genre': 'Action', 'rating': 8.8, 'image': '🌀', 'showtimes': ['11:30', '15:00', '18:30']},
]

bookings = []

@app.route('/')
def home():
    return render_template('index.html', movies=movies[:3])

@app.route('/movies')
def movie_list():
    return render_template('movies.html', movies=movies)

@app.route('/book/<int:movie_id>', methods=['GET', 'POST'])
def book(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        showtime = request.form.get('showtime')
        seats = request.form.get('seats', 1)
        
        if not all([name, email, showtime]):
            flash('Please fill all required fields', 'error')
            return render_template('book.html', movie=movie)
        
        booking = {
            'id': len(bookings) + 1,
            'movie': movie['title'],
            'name': name,
            'email': email,
            'showtime': showtime,
            'seats': seats
        }
        bookings.append(booking)
        flash(f'Booking confirmed! ID: #{booking["id"]}', 'success')
        return redirect(url_for('confirmation', booking_id=booking['id']))
    
    return render_template('book.html', movie=movie)

@app.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    booking = next((b for b in bookings if b['id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404
    return render_template('confirmation.html', booking=booking)

if __name__ == '__main__':
    app.run(debug=True)
