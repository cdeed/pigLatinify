import requests
import json
import sys

vowels = ['a','e','i','o','u']
url = 'https://api.hubapi.com/contacts/v1/contact/email/{email}/profile?hapikey={hapikey}'
hapikey = str(sys.argv[1])

def getConsonantCluster(word):
    letterList = list(word.lower())
    cluster = ''
    if letterList[0] in vowels:
        return ''
    else:
        for letter in letterList:
            if letter not in vowels:
                cluster += letter
            else:
                break
        return cluster

def removeCluster(word):
    return word.lower().replace(getConsonantCluster(word),'',1)

def makeSuffix(cluster):
    return cluster+"ay"

def makePigLatin(word):
    return removeCluster(word) + makeSuffix(getConsonantCluster(word))

def getContactFirstName(email):
    r = requests.get(url.format(email=email, hapikey=hapikey))
    if r.status_code == 200:
        return str(json.loads(r.text)["properties"]["firstname"]["value"])
    elif r.status_code == 404:
        print("Contact does not exist!")
        sys.exit()
    else:
        print("Something went wrong; please try again")
        sys.exit()
    r.close()

def pushNewFirstname(email, newName):
    r = requests.post(url.format(email=email, hapikey=hapikey),data=json.dumps({"properties":[{"property": "firstname","value": newName}]}))
    if r.status_code == 204:
        return "Name successfully updated to {}".format(newName)
    else:
        print(r.status_code)

email = raw_input("Enter your email: ")
print(pushNewFirstname(email, makePigLatin(getContactFirstName(email))))
