# -*- coding:utf-8 -*-
import csv

# Login information to the tactical system
username = ''
password = ''
website = ''

# lockfile, if it exists, do not run the update
LOCKFILE = ''

# Name of the group
coterie = ''

# time to wait between 2 requests
sleep_time = 6

# dictionary containing the trolls of the group
# dict must be like this :
# { id  : {'nom' : 'name of the troll'},
#   id2 : {'nom' : 'name of the troll'} }

trolls = {}

FROM_CSV = False

if FROM_CSV:
    # fichier csv de la forme:
    # uid|nom|actif   
    # avec actif etant True ou False
    filename = 'trolls.csv'

    try:
        fd = open(filename)
        spamReader = csv.reader(fd, delimiter='|')
        for uid, nom, actif in spamReader:
            if eval(actif):
                trolls[uid] = {'nom': nom}
    except:
        pass
    finally:
        fd.close()
