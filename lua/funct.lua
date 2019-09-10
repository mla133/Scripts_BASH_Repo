function getPass(checkPass)
	local pass = ""

	io.write("Please Enter a Password: ") -- io.write() is same as term.write() in CC
	pass = io.read()					  -- io.read() is the same as term.read() in CC

	if pass ~= checkPass then
		print("Wrong Password")
		return false
	else
		print("Correct...")
		return true
	end
end

print("Starting Program")

while not getPass("matt") do
	print("Please Try Again...")
end

print("Let's do stuff")

while not getPass("password") do
	print("Do it till you get it right...")
end
