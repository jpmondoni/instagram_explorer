# pack of functions and utilities used across the project.
from hashlib import md5

def hex_md5_digest(image_url):
	url_md5 = md5()
	url_md5.update(image_url.encode())
	return url_md5.hexdigest()

