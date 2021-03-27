import hmac, base64, struct, hashlib, time, json, os, random, string

def get_hotp_token(secret, intervals_no):
	"""This is where the magic happens."""
	key = base64.b32decode(normalize(secret), True) # True is to fold lower into uppercase
	msg = struct.pack(">Q", intervals_no)
	h = bytearray(hmac.new(key, msg, hashlib.sha1).digest())
	o = h[19] & 15
	h = str((struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000)
	return prefix0(h)


def get_totp_token(secret):
	"""The TOTP token is just a HOTP token seeded with every 30 seconds."""
	return get_hotp_token(secret, intervals_no=int(time.time())//30)


def normalize(key):
	"""Normalizes secret by removing spaces and padding with = to a multiple of 8"""
	k2 = key.strip().replace(' ','')
	# k2 = k2.upper()	# skipped b/c b32decode has a foldcase argument
	if len(k2)%8 != 0:
		k2 += '='*(8-len(k2)%8)
	return k2


def prefix0(h):
	"""Prefixes code with leading zeros if missing."""
	if len(h) < 6:
		h = '0'*(6-len(h)) + h
	return h


def get_key(username):
	rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	with open(os.path.join(rel,'secrets.json'), 'r') as json_file:
		secrets = json.load(json_file)

	return 	get_totp_token(secrets[username])


def has_2fa(username):
	rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	with open(os.path.join(rel,'secrets.json'), 'r') as json_file:
		secrets = json.load(json_file)

	for user, secret in secrets.items():
		if (user == username):
			return True
	return False

def get_secret(username):
	rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	with open(os.path.join(rel,'secrets.json'), 'r') as json_file:
		secrets = json.load(json_file)
	
	return secrets[username]


def add_2fa(username):
	key = ''.join(random.choice(string.ascii_uppercase) for i in range(16)) #https://www.educative.io/edpresso/how-to-generate-a-random-string-in-python
	print("TEST KEY", key)
	# need to update the existing file, not overwrite
	rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	with open(os.path.join(rel,'secrets.json'), 'r') as json_file:
		secrets = json.load(json_file)

	secrets.update({username: key})

	with open(os.path.join(rel,'secrets.json'), 'w') as update_json:
		json.dump(secrets, update_json)
		update_json.truncate()


def validate_input(username, input):
	key = get_key(username)

	return key == str(input)

def generate_url(user, secret):
	#https://dan.hersam.com/tools/gen-qr-code.php
	# want to use default digits = 6 and period = 30s
	url = "otpauth://totp/" + "SecFit:" + user + "?secret="+ secret + "&issuer=SecFit"

	return url

