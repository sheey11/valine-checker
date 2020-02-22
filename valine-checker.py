import leancloud as lc
import json, time, threading, smtplib, asyncio
from smtplib import SMTPHeloError, SMTPAuthenticationError
from email.mime.text import MIMEText
from email.utils import formataddr
from logger import logging
import akismet

config = {}
query = None
server = None
user = None
akismet_enabled = False

async def check_new_comments() -> list:
    query.not_equal_to('isNotified', True)
    unnotified_list = query.find()
    await logging('检查新评论，查询到 %d 个新评论。' % len(unnotified_list), prnt = True)
    return unnotified_list

def login_to_smtp() -> str:
    global server
    try:
        if config['smtp_secure']:
            server = smtplib.SMTP_SSL(config['smtp_host'], config['smtp_port'])
        else:
            server = smtplib.SMTP(config['smtp_host'], config['smtp_port'])
    except:
        return "无法连接到服务器，请检查设置"
    # server.set_debuglevel(1)
    try:
        server.login(config['smtp_user'], config['smtp_password'])
    except SMTPHeloError:
        return "无法连接到服务器，请检查设置"
    except SMTPAuthenticationError:
        return "用户名或密码错误，无法登陆 SMTP 服务器"
    return ''

def send_email(content: str, frm: str, to: list, subject: str, sender_name: str, receiver_name: str = '') -> bool:
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = formataddr([sender_name, frm])
    msg['To'] = ','.join([formataddr([receiver_name, t]) for t in to])
    try:
        server.sendmail(frm, to, msg.as_string())
        return True
    except:
        return False

def send_replay_email(comment) -> bool:
    parent_comment = query.get(comment.get('rid'))
    if(parent_comment.get('email') == None):
        return True
    mail_template = config['mail_template']
    mail_template = mail_template.replace('${SITE_NAME}', config['site_name'])
    mail_template = mail_template.replace('${SITE_URL}', config['site_url'])
    mail_template = mail_template.replace('${PARENT_NICK}', parent_comment.get('nick'))
    mail_template = mail_template.replace('${PARENT_COMMENT}', parent_comment.get('comment'))
    mail_template = mail_template.replace('${NICK}', comment.get('comment'))
    mail_template = mail_template.replace('${COMMENT}', comment.get('comment'))
    mail_template = mail_template.replace('${POST_URL}', config['site_url'] + comment.get('url') + '#' + comment.get('objectId'))
    subject = config['email_subject']
    subject = subject.replace('${PARENT_NICK}', parent_comment.get('nick'))
    subject = subject.replace('${SITE_NAME}', config['site_name'])
    return send_email(mail_template, config['smtp_mail'], comment.get['mail'], subject, config['sender_name'], comment.get('nick'))


def send_admin_email(comment) -> bool:
    mail_template = config['mail_template_admin']
    mail_template = mail_template.replace(r'${SITE_NAME}', config['site_name'])
    mail_template = mail_template.replace(r'${SITE_URL}', config['site_url'])
    mail_template = mail_template.replace(r'${NICK}', comment.get('nick'))
    mail_template = mail_template.replace(r'${COMMENT}', comment.get('comment'))
    mail_template = mail_template.replace(r'${POST_URL}', config['site_url'] + comment.get('url') + '#' + comment.get('objectId'))
    subject = config['site_name'] + '上有新评论了'
    return send_email(mail_template, config['smtp_mail'], config['blogger_mail'], subject, config['site_name'])

async def send_emails(lst):
    for c in lst:
        if akismet_enabled:
            await logging('正在通过 akismet 验证垃圾评论: %s' % c.get('comment'))
            if not akismet.check(config['site_url'], c.get('ip'), c.get('ua'), config['site_url'] + c.get('url'), c.get('comment'), c.get('nick'), c.get('mail'), c.get('link')):
                await logging('检测到垃圾评论，跳过发送邮件')
                acl = lc.ACL()
                acl.set_public_read_access(False)
                c.set_acl(acl)
                c.set('isSpam', True)
                c.save()
                continue

        await logging('正在发送邮件： objectId = %s' % c.id)
        if c.get('rid') == None:
            # notify the blogger
            func = send_admin_email
        else:
            # notify the author of the comment be replied
            func = send_replay_email
        if func(c):
            await logging('邮件发送成功！')
            c.set('isNotified', True)
            c.save()
        else:
            await logging('邮件发送失败！', level = 'error', prnt = True)
            exit(1)


def load_config():
    global config
    with open('config.json', 'r') as f:
        config = json.loads(f.read())

async def init():
    global query, user, akismet_enabled
    await logging('加载配置文件...', prnt = True)
    load_config()
    lc.init(config['app_id'], master_key=config['master_key'])
    if config['akismet_key'] != '':
        await logging('验证 akismet key...', prnt = True)
        if not akismet.init(config['akismet_key'], config['site_url']):
            await logging('akismet key 验证失败，请检查你的 akismet key', level='error', prnt = True)
            exit(1)
        akismet_enabled = True
    query = lc.Query('Comment')

async def main():
    await logging('Valine-Cheker 开始初始化。', prnt = True)
    await init()
    await logging('正在登陆 SMTP 服务器...', prnt = True)
    m = login_to_smtp()
    if m != '':
        await logging(m, level = 'error', prnt = True)
        exit(1)
    while True:
        lst = await check_new_comments()
        await send_emails(lst)
        await logging('等待 %d 秒...' % config['interval'])
        await asyncio.sleep(config['interval'])

if __name__ == '__main__':
    asyncio.run(main())