from flask import Flask, render_template, request, url_for
import Post
from scrap_task import scrap_init
from retrieve_posts import generate_list

app = Flask(__name__, static_url_path='/static')

__global_title = 'Instagram Data Visualization'

@app.route('/')
def index():
	return render_template('index.html',
							title=__global_title)

@app.route('/posts/', methods=['POST', ])
def load():
	hashtag = request.form['hashtag']
	post_list = scrap_init(hashtag, False)

	return render_template('posts.html',
						   title=__global_title,
						   posts=post_list,
						   hashtag=hashtag)


@app.route('/insights/')
def insights():
	return render_template('insights.html',
						   title=__global_title,
						   subtitle='Insights')


app.run(debug=True)
