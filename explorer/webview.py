from flask import Flask, session, render_template, request, url_for, make_response
import Post
import json
from scrap_task import scrap_init
from retrieve_posts import generate_list
from images_insights import image_info
from save_insights_analysis import check_existence

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'this is a secret!'

__global_title = 'Instagram Data Visualization'

@app.route('/')
def index():
	session.clear()
	return render_template('index.html',
							title=__global_title)

@app.route('/posts', methods=['POST', ])
def load():
	hashtag = request.form['hashtag']
	post_list = scrap_init(hashtag, True)
	post_parameter = post_list
	resp = make_response(render_template('posts.html',
						   title=__global_title,
						   posts=post_list,
						   hashtag=hashtag))

	for post in post_parameter:
		del post['caption']
		del post['timestamp']
		json_post = json.dumps(post, ensure_ascii=False).encode('utf8')
		post_id = post['post_id']
		session[post_id] = json_post

	return resp


@app.route('/insights/<hashtag>')
def render_insights(hashtag):

	image_insight_list = []
	for key in session.keys():
		json_cookie = json.loads(session[key])
		post_id = key
		post_exists = check_existence(post_id)
		pict_url = ""
		print(post_exists)
		if(post_exists[0]):
			for picture_url in post_exists[1]:
				pict_url = picture_url
			image_insight_list.append(post_id, picture_url)

		img_obj = image_info(post_id, json_cookie['picture_url'])
		image_insight_list.append(img_obj)

	return render_template('insights.html',
							title=__global_title,
							subtitle='Insights',
							hashtag=hashtag,
							img_list=image_insight_list)


app.run(debug=True,host= '0.0.0.0')
