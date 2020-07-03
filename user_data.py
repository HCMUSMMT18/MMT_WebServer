#username= 'admin'
#password= 'admin'
user=[]
pw=[]
data=open("data.txt").read().splitlines()
for i in data:
    user.append(i.split("|")[0])
    pw.append(i.split("|")[1])

def login_check(self, username,password):
    for i in user:
        if(i==username):
            if(pw[user.index(i)]==password):
                return True
            else:
                return False    
    return False
