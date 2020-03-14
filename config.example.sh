export app_id="app-id"
export master_key="app-key"
export interval=120
export site_name="Your site name"
export site_url="https://your-site-url.com"
export smtp_user="user"
export smtp_mail="email@site.com"
export smtp_password="password"
export smtp_host="smtp.host.com"
export smtp_port=994
export smtp_secure=true
export blogger_mail="your-email@site.com, another@email.com"
export sender_name="sender's name"
export email_subject="${PARENT_NICK}，您在${SITE_NAME}里的评论有回复啦~"
export mail_template="<div style=\"font-family:-apple-system, BlinkMacSystemFont, '微软雅黑', 'Microsoft Yahei', 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; border-top:2px solid #12ADDB;box-shadow:0 1px 3px #AAAAAA;line-height:180%;padding:0 15px 12px;margin:50px auto;font-size:12px;\"><h2 style=\"border-bottom:1px solid #DDD;font-size:14px;font-weight:normal;padding:13px 0 10px 8px;\">您在<a style=\"text-decoration:none;color: #12ADDB;\" href=\"${SITE_URL}\" target=\"_blank\">            ${SITE_NAME}</a>上的评论有了新的回复</h2> ${PARENT_NICK} 同学，您曾发表评论：<div style=\"padding:0 12px 0 12px;margin-top:18px\"><div style=\"background-color: #f5f5f5;padding: 10px 15px;margin:18px 0;word-wrap:break-word;\">            ${PARENT_COMMENT}</div><p><strong>${NICK}</strong>回复说：</p><div style=\"background-color: #f5f5f5;padding: 10px 15px;margin:18px 0;word-wrap:break-word;\"> ${COMMENT}</div><p>您可以点击<a style=\"text-decoration:none; color:#12addb\" href=\"${POST_URL}\" target=\"_blank\">查看回复的完整內容</a>，欢迎再次光临<a style=\"text-decoration:none; color:#12addb\" href=\"${SITE_URL}\" target=\"_blank\">${SITE_NAME}</a>。<br></p></div></div>"
export mail_template_admin="<div style=\"font-family:-apple-system, BlinkMacSystemFont, '微软雅黑', 'Microsoft Yahei', 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; border-top:2px solid #12ADDB;box-shadow:0 1px 3px #AAAAAA;line-height:180%;padding:0 15px 12px;margin:50px auto;font-size:12px;\"> <h2 style=\"border-bottom:1px solid #DDD;font-size:14px;font-weight:normal;padding:13px 0 10px 8px;\"> 您在<a style=\"text-decoration:none;color: #12ADDB;\" href=\"${SITE_URL}\" target=\"_blank\" rel=\"noopener\"> ${SITE_NAME}</a>上的文章有了新的评论</h2> <p><strong>${NICK}</strong>回复说：</p><div style=\"background-color: #f5f5f5;padding: 10px 15px;margin:18px 0;word-wrap:break-word;\"> <p>${COMMENT}</p></div><p>您可以点击<a style=\"text-decoration:none; color:#12addb\" href=\"${POST_URL}\" target=\"_blank\" rel=\"noopener\">查看回复的完整內容</a><br></p></div>"
export akismet_key="akismet_key"