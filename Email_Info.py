def email_info(text):
	email_addresses = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
	return email_addresses