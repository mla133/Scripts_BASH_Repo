print("For Loop Sample")

for i = 1, 10, 2 do
	print("Current Position: "..i)
	if i == 5 then
		break
	end
end

print("While Loop Sample")

local x = 0

while x < 10 do
	print("x= "..x)
	x = x + 1
end

print("Repeat Until Loop Example")
local y = 6

repeat
	print("Y: "..y)
until y > 5
