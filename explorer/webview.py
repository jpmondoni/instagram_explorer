from query_posts import query_posts
from flask import Flask, render_template

app = Flask(__name__)

class Post:
    def __init__(self, post_id, caption, img_url, hahstag):
        self.post_id = post_id
        self.caption = caption
        self.hashtag = hashtag
        self.pciture_url = pciture_url


@app.route('/posts')
def load_posts():
    post_list = query_posts()
    return render_template('posts.html',
                           titulo='Instagram Posts',
                           posts=post_list)

app.run()