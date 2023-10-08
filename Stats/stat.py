@app.route('/stats')
def stats():
    conn = get_db_connection()
    db_urls = conn.execute('SELECT id, created, original_url, clicks FROM urls').fetchall()
    conn.close()
    urls = []
    for url in db_urls:
        url = dict(url)
        url['short_url'] = request.host_url + hashids.encode(url['id'])
        urls.append(url)
    return render_template('stats.html', urls=urls)