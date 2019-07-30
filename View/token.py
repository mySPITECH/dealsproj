import random
import string

class RandomToken(object):
    def __init__(self):
        pass


    def randomString(self):
        """Generate a random string with the combination of lowercase and uppercase letters """
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(12))
    print("Random String with the combination of lowercase and uppercase letters")
    print ("First Random String is ", randomString(12) )
