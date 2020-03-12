import leancloud as lc
import json

config = {}
query = None

def load_config():
    global config
    with open('server/checker/config.json', 'r') as f:
        config = json.loads(f.read())

def init():
    global query
    load_config()
    lc.init(config['app_id'], master_key=config['master_key'])
    query = lc.Query('Comment')

def delete_comment(obj_id,):
    try:
        c = query.get(obj_id)
        c.destroy()
        return True
    except:
        return False

def mark_comment(obj_id, mark_spam=False, hide=True):
    try:
        c = query.get(obj_id)
        if mark_spam:
            c.set('isSpam', True)
        else:
            c.set('isSpam', False)
        acl = lc.ACL()
        acl.set_public_read_access(not hide)
        c.set_acl(acl)
        c.save()
        return True
    except:
        return False

def main(argv):
    init()
    obj_id = argv[1]
    if argv[0] == 'delete':
        delete_comment(obj_id)
    elif argv[0] == 'hide':
        mark_comment(obj_id)
    elif argv[0] == 'markAsSpam':
        mark_comment(obj_id, True)
    elif argv[0] == 'markAsNormal':
        mark_comment(obj_id, False, False)

if __name__ == '__main__':
    main(sys.argv[1:])
