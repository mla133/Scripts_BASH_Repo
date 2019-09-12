local color1 = "blue"
local color2 = "red"
local color3 = "yellow"

local colors = {"blue", "red", "yellow", "green"}

for i = 1,4 do
	print(colors[i])
end

local colorcodes = {white = 1, orange = 2, magenta = 4}

print(colorcodes["magenta"])

for key,value in pairs(colorcodes) do
	print(key.."="..value)
end

local stuff = {"blue", {"stuff1","stuff2"}, "green"}

print (stuff[1])
print(stuff[2][1])
print(stuff[2][2])
print(stuff[3])
