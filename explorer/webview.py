from query_posts import query_posts
from flask import Flask, render_template, request, url_for
import Post
from retrieve_posts import generate_list

app = Flask(__name__, static_url_path='/static')

__global_title = 'Instagram Data Visualization'

@app.route('/posts/', methods=['POST', ])
def load():
	#post_list = query_posts(hashtag)
	#print(len(post_list))
	hashtag = request.form['hashtag']
	post_list = generate_list(hashtag)
		
	return render_template('posts.html',
						   title=__global_title,
						   posts=post_list,
						   hashtag=hashtag)

@app.route('/')
def index():
	return render_template('index.html',
							title=__global_title)



app.run(debug=True)
