import sublime, sublime_plugin

import urllib.request, urllib.parse, urllib.error
import time
import random
import base64
import datetime
import hashlib
import http.client

from xml.etree.ElementTree import *

class HatenablogpostCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		setting = sublime.load_settings("HatenaBlogPostCommand.sublime-settings")
		window = self.view.window()
		window.run_command("show_panel", {"panel":"console"})

		hatena_id = setting.get('hatena_id')
		api_key = setting.get('api_key')
		posturl = setting.get('post_url')
		draft_mode = setting.get('draft_mode')

		region_all = sublime.Region(0, self.view.size())
		content = self.view.substr(region_all)
		title, body = content.split("\n\n", 1)

		token = self.createHeaderToken(hatena_id, api_key)
		blogbody = self.createBlogEntry(title, body, hatena_id, draft_mode)
		response = self.atomRequest(token, "POST", posturl, blogbody, "text/plain")

	def createHeaderToken(self, username, password):
		created = datetime.datetime.now().isoformat() + 'Z'
		b_nonce = hashlib.sha1(str(random.random()).encode()).digest()
		b_digest = hashlib.sha1(b_nonce + created.encode() + password.encode()).digest()
		pass64 = base64.b64encode(b_digest).decode()
		nonce64 = base64.b64encode(b_nonce).decode()

		wsse = 'UsernameToken Username="%(u)s", PasswordDigest="%(p)s", Nonce="%(n)s", Created="%(c)s"'
		value = dict(u = username, p = pass64, n = nonce64, c = created)

		return wsse % value

	def atomRequest(self, wsse, method, endpoint, body, content_type):
		header_info = {	'X-WSSE': wsse, 
						'Content-Type': content_type, 
						'Authorization': 'WSSE profile="UsernameToken',
						'User-Agent': 'Python WSSE'}

		conntypeinfo, conninfo = urllib.parse.splittype(endpoint)
		connhostinfo, conninfo = urllib.parse.splithost(conninfo)
		conn = http.client.HTTPConnection(connhostinfo)
		conn.request(method, conninfo, body, header_info)
		r = conn.getresponse()
		if r.status not in [200, 201]:
			raise Exception('login failure')
		response = dict(status = r.status,
							reason = r.reason,
							data = r.read())
		conn.close()
		return response

	def createBlogEntry(self, title, body, name, draft):
		xmlcontent = Element('entry')
		xmlcontent.set('xmlns', 'http://www.w3.org/2005/Atom')
		xmlcontent.set('xmlns:app', 'http://www.w3.org/2007/app')
		entrytitle = SubElement(xmlcontent, 'title')
		entrytitle.text = title
		entryauthor = SubElement(xmlcontent, 'author')
		authorname = SubElement(entryauthor, 'name')
		authorname.text = name
		content = SubElement(xmlcontent, 'content')
		content.set('type', 'text/plain')
		content.text = body
		app = SubElement(xmlcontent, 'app:control')
		appdraft = SubElement(app, 'app:draft')
		appdraft.text = draft

		return tostring(xmlcontent)
