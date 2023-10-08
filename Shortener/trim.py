from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])
@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        url = request.form['url']
        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)',(url,))
        conn.commit()
        conn.close()
        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')