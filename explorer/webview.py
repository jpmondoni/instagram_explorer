from query_posts import query_posts
from flask import Flask, render_template
import Post

app = Flask(__name__, static_url_path='/static')

#hashtag = 'sunset'
@app.route('/posts/<hashtag>')
def load_posts(hashtag):
    post_list = query_posts(hashtag)
    print(len(post_list))
    return render_template('index.html',
                           title='Instagram Posts',
                           posts=post_list,
                           hashtag=hashtag)

app.run()