
def eastcoastplan():
	with open('/etc/sensitive_secret', 'r') as f:
	    content = f.read()
	    print(content)