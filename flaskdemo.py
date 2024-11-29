from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
app.secret_key = 'your_very_secret_key'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")

@app.route('/results')
def results():
    search_term = session['search_term']
    page = get_page(search_term)
    return render_template("results.html", title=page.title, content=page.content)

def get_page(search_term):
    try:
        page = wikipedia.page(search_term)
    except wikipedia.exceptions.PageError:
        page = wikipedia.page(wikipedia.random())
    except wikipedia.exceptions.DisambiguationError:
        page_titles = wikipedia.search(search_term)
        if page_titles[1].lower() == page_titles[0].lower():
            title = page_titles[2]
        else:
            title = page_titles[1]
        page = get_page(wikipedia.page(title))
    return page

if __name__ == '__main__':
    app.run()
