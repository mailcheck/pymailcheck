'''
I will store the name of some domains in a list

'''

domains=["google.com","yahoo.com","hotmail.com","rediffmail.com","aol.com","msn.com","microsoft.com","ntlworld.com"]

user=input("Enter your email id: ")
Len=len(user)
print(Len)
list(user)
Username=[]
Index=0
Domain=[]
'''
check the username of the email id and check if its valid or not
'''
def checkuser():
    for x in range(0,Len):
        if(user[x]=='@'):
            #to find the index where the domain starts from
            Index=x+1
            break
        else:
            Username.append(user[x])

#assumming minimum length of the user to be 7
    Len2=len(UserName)
    if(Len2<7):
       print("The username you entered it too small")
#the user should have a uppercase letter and a number
    Valid=False
    for y in Username:
    #Using the ASCII code of uppercase and numbers
        if (y>=65 and y<=90) or(y>=47 and y<=56):
          Valid=True
    if(Valid==False):
    print("The username must have a uppercase character and a number.")

def checkdomain():
    #To check the domain part of the email id using the range between index and end of the list
    #index is set to a value in check user function
    for x in range(Index,len1):
        Domain.append(user[x])
    if ((Domain in domains) and (Valid==true)):
        print("Valid email id")
    if ((Valid==True) and  (Domain not in domains)):
        if(Domain[0]=='g'):
            print("Suggested domain: google.com")
        if (Domain[0] == 'y'):
            print("Suggested domain: yahoo.com")
        if (Domain[0] == 'a'):
            print("Suggested domain: aol.com")
        if (Domain[0] == 'm'):
            print("Suggested domain: msn.com")
        if (Domain[0] == 'h'):
            print("Suggested domain: hotmail.com")
        if (Domain[0] == 'r'):
            print("Suggested domain: rediffmail.com")
        if (Domain[0] == 'm'):
            print("Suggested domain: microsoft.com")
        if (Domain[0] == 'n'):
            print("Suggested domain: ntlworld.com")

checkuser()
checkdomain()

