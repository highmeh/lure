end_text = "\033[0m"
warning_text = "\033[93m"
success_text = "\033[92m"
fail_text = "\033[91m"

def print_logo():
	print(warning_text + "\n   L U R E  |  Phishing Target Collection Automation")
	print("               jayme@blackjacknetworks.com")
	print("-----------------------------------------------------------" + end_text)
	return

def print_fail(text):
	output = fail_text + text + end_text
	print(output)
	#return output

def print_success(text):
	output = success_text + text + end_text
	print(output)

def print_warning(text):
	output = warning_text + text + end_text
	print(output)
	
