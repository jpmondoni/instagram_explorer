from flask import Flask, render_template, request, url_for, make_response
import Post
import json
from scrap_task import scrap_init
from retrieve_posts import generate_list
from images_insights import image_info

app = Flask(__name__, static_url_path='/static')

__global_title = 'Instagram Data Visualization'

@app.route('/')
def index():
	return render_template('index.html',
							title=__global_title)

@app.route('/posts', methods=['POST', ])
def load():
	hashtag = request.form['hashtag']
	post_list = scrap_init(hashtag, False)
	post_parameter = post_list
	resp = make_response(render_template('posts.html',
						   title=__global_title,
						   posts=post_list,
						   hashtag=hashtag))
	for post in post_parameter:
		del post['caption']
		del post['timestamp']
		json_post = json.dumps(post, ensure_ascii=False).encode('utf8')
		resp.set_cookie('post_'+post['post_id'], json_post)

	return resp


@app.route('/insights/<hashtag>')
def render_insights(hashtag):

	cookies = request.cookies
	image_insight_list = []
	for cookie in cookies:
		if(cookie[:5] == 'post_'):
			cookie_info = request.cookies.get(cookie)
			json_cookie = json.loads(cookie_info)
			image_insight_list.append(image_info(json_cookie['picture_url']))

	return render_template('insights.html',
							title=__global_title,
							subtitle='Insights',
							hashtag=hashtag,
							img_list=image_insight_list)


app.run(debug=True)
