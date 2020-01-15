#!/usr/bin/env python
# Magic 8 ball program

import random
answers = ["As I see it, yes","It is certain","It is decidedly so","Most likely","Outlook good","Signs point to yes","Without a doubt","Yes","Yes definitely","You may rely on it","Reply hazy, try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","My sources say no","Outlook not so good","Very doubtful"]
input("What is your question?\n")
response = random.choice(answers)
print (response + '\n')

# Pause at end of script, hit Enter to close
input("Press ENTER to exit")
