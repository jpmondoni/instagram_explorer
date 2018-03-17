from query_posts import query_posts
from flask import Flask, render_template
import Post

app = Flask(__name__)

@app.route('/posts')
def load_posts():
    post_list = query_posts()
    return render_template('posts.html',
                           titulo='Instagram Posts',
                           posts=post_list)

app.run()