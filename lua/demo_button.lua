os.loadAPI("button")
m = peripheral.wrap("top")
m.clear()

function fillTable()
	button.setTable("Test1", test1, 10, 20, 3, 5)
	button.setTable("Test2", test2, 22, 32, 3, 5)
	button.setTable("Test3", test3, 10, 20, 8, 10)
	button.setTable("Test4", test4, 22, 32, 8, 10)
	button.screen()
end

function getClick()
	event,side,x,y = os.pullEvent("monitor touch")
	button.checkxy(x,y)
end

function test1()
	button.flash("Test1")
	print("Test1")
end

function test2()
	button.toggleButton("Test2")
	print("Test2")
end

function test3()
	print("Test3")
end

function test4()
	print("Test4")
end

fillTable()
button.heading("Demo Button Prog")
button.label(1,5,"Demo")
while true do
	getClick()
end
