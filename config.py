import os

CONFIG_VARIABLES = [
    'app_id',
    'master_key',
    'interval',
    'site_name',
    'site_url',
    'smtp_user',
    'smtp_mail',
    'smtp_password',
    'smtp_host',
    'smtp_port',
    'smtp_secure',
    'blogger_mail',
    'sender_name',
    'email_subject',
    'mail_template',
    'mail_template_admin',
    'akismet_key',
]

def load_config() -> dict:
    config = {}
    for variable in CONFIG_VARIABLES:
        value = os.environ[variable.upper()]
        config[variable] = value
    return config
