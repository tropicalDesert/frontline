import ssl
import socket
from express import http_manager

def placeholder(none):
	return "Hello!"

global method_route
method_route={
	"GET":placeholder,
	"POST":placeholder
}

def http_socket(host,port):
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host,port))
	s.listen(5)
	return s

def https_socket(host,port,kwargs):
	s=http_socket(host,port)
	context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
	context.load_cert_chain(kwargs['certificate'],kwargs['key'])
	return context.wrap_socket(s,server_side=True)

def data_parse(query):
	data={}
	try:
		clean_query=query.split("?")[1]
	except Exception as e:
		return data
	assignments=clean_query.split("&")
	for assignment in assignments:
		try:
			key_value=assignment.split("=")
			key=key_value[0]
			value=key_value[1]
			data[key]=value
		except Exception:
			continue
	return data

def header_parse(data):
	req={}
	try:
		formatted_data=data.decode('utf-8')
	except:
		return req
	data_fields=formatted_data.split("\r\n")
	meta=data_fields[0]
	meta_cats=meta.split(" ")
	method=meta_cats[0]
	query=meta_cats[1]
	protocol=meta_cats[2]
	req['method']=method
	req['query']=query
	req['protocol']=protocol
	req['data']=data_parse(query)
	req['headers']={}
	for field in data_fields:
		fields=field.split(":")
		if(len(fields)<2):continue
		key=fields[0]
		value=fields[1]
		req['headers'][key]=value
	return req

def dish(socket):
	conn, addr=socket.accept()
	data=conn.recv(2048)
	if not data:return False
	request=header_parse(data)
	headers=http_manager.status(200)
	try:
		message=method_route[request['method']](request,conn)
	except Exception:
		message=""
	response=headers + message
	conn.send(response.encode("utf-8"))
	return True

def serve(host,port,https=False):
	if(https):
		s=https_socket(host,port,https)
	else:
		s=http_socket(host,port)
	print("Serving " + host + " on port " + str(port))
	while(True):
		dish(s)

def get(handler):
	global get_request
	method_route['GET']=handler

def post(handler):
	global post_request
	method_route['POST']=handler
