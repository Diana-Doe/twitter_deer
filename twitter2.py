import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import sys

#Small introduction 
print("Hi! This program will help you to go through the JSON file.\
Firstly, you have to choose the JSON file (with your friends or followers).\
Then, enter the number of people and after choose one person from a list\
After you will see the list with available parameters, feel free to choose as many as you need,\
but be aware that you can choose each parameter only one time.\
If the parameter that you choose contains other parameters you have to continue choosing until you come to the end.\
If you finish choosing than write 'finished' or 'stop' or 'I like Rayn Gosling'\
and all the parameters that you chose will be shown.\n\n\n\t*\t*\t*")

#User choose friends/followers
f = ''
while f != 'friends' and f != 'followers': f = str(input("Who do you want to check(friends or followers): "))
if f == 'friends': TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
else: TWITTER_URL = 'https://api.twitter.com/1.1/followers/list.json'


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#If the chosen key contains a dictionary user will choose parameters until he/she gets to the last key. 
def reverse(want,lst):
    if type(want) == dict:
        ls = []
        for i in want:
            ls.append(i)
        print(ls)
        wanted = ''
        while wanted not in ls: wanted = str(input("What do you exatly want to see: "))
        if type(want[wanted]) == dict:
            lst.append(wanted)
            return reverse(want[wanted],lst)
        elif type(want[wanted]) == list:
            lst.append(wanted)
            l = -1
            for i in want[wanted]:
                if type(i) == dict:
                    l += 1
                else:
                    continue
            if l != -1:
                print('You have {} dictionary/ies in list. Choose one (print number from 0 to {})'.format(l+1,l))
                n = int(input())
                lst.append(n)
                return reverse(want[wanted][n], lst)

            else:
                lst.append(want[wanted])
                return lst
        else:
            print(want[wanted])
            lst.append(want[wanted])
            return lst
    else:
        return True

#Main loop
while True:
    print('')
    acct = input('Enter Twitter Account:')
    if (len(acct) < 1): break
    print('')
    amount = -1
    while amount > 100 and amount < 0: amount = int(input("How many users do want to see(enter number from 1 to 100): "))
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': str(amount)})

    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    followers = {}
    count = 0
    for i in js['users']:
        followers[count] = i['name']
        count +=1
    print("Choose one {} and write his/her number.\n\n".format(f[:-1]), followers,'\n')
    num = int(input("Your number: "))
    while num not in followers: print("You have entered the wrong number"); num = int(input("Your number: "))
    user = js['users'][num]['screen_name']
    lst = []
    for p in js['users'][num]:
        lst.append(p.replace('_',' '))
    lst.append('tweet')
    print("\n/users/{}/\n\t\t*** \nWhat do you want to look at?\n".format(user),lst)

    #Loop for choosing
    wants, deep_list = [], []
    while True:
        want = str(input("Choose something from the list: "))
        while (want not in lst and want.lower() != 'tweet' and want != 'finished'and want == 'stop' and want == 'I like Rayn Gosling'):
            print("It isn`t in the list.");want = str(input("Choose something from the list: "))
        if want == 'finished' or want == 'stop' or want == 'I like Rayn Gosling':
            break
        want = want.replace(' ','_').lower()
        if want != 'tweet':
            rev = reverse(js['users'][num][want],[want])
        else:
            rev == True
        if rev == True:
            if want not in wants:
                wants.append(want)
            else:
                print("You have already chosen this option")
        else:
            deep_list.append(rev)
            print("\n/users/{}/ \n".format(user), lst)

    #If user didn`t enter anything program gets upset and turn off
    if len(wants) == 0 and len(deep_list) == 0:
        sys.exit()

    #Final output
    print("\n\n\n\t***\t***\t***")
    for i in wants:
        if i == 'tweet':
            print('/users/{}/status/'.format(user))
            if 'status' not in js['users'][num]:
                print('   * No tweet found')
                continue
            s = js['users'][num]['status']['text']
            print('  ', s)
        else:
            print('/users/{}/{}/'.format(user,i) + '\n', js['users'][num][i])
    if len(deep_list) != 0:
        for i in deep_list:
            string = '/users/'+user+'/'
            for p in i:
                if p != i[-1]:
                    string += str(p) +'/'
                else:
                    print(string + '\n' + str(p))
    print("\t***\t***\t***")





        


