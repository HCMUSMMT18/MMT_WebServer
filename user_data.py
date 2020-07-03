#username= 'admin'
#password= 'adin'


def login_check(username,password):
    user=[]
    pw=[]
    data=open("data.txt").read().splitlines()
    for i in data:
        user.append(i.split("|")[0])
        pw.append(i.split("|")[1])
    for i in user:
        if(i==username):
            if(pw[user.index(i)]==password):
                #print('T')
                return True
            else:
                #print('F')
                return False    
    #print('F')
    return False

#login_check(username, password)