import sqlite3
import sys
    
# args
if len(sys.argv) == 4:

    dbfile = str(sys.argv[1])
    nick = str(sys.argv[2])
    newlvl = int(sys.argv[3])

    print('DatabaseFile: %s' % dbfile)
    print('Authname: %s' % nick)
    print('NewLevel: %s' % newlvl)

    while True:
        resume = str(input('Continue? [y/n]'))
        if resume == 'y':
            db = sqlite3.connect(dbfile)
            dbcursor = db.cursor()
            dbcursor.execute('UPDATE users SET lvl=? WHERE nick=?', (newlvl, nick))
            db.commit()
            print('Success!')
            break
        elif resume == 'n':
            print('Aborted!')
            break

else:
    print('To less args!')
    print('editdatabase.py <databasefile> <nick> <newlvl>')

print('----EXIT---')