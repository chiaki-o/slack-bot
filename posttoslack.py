# coding: UTF-8

import slackweb
import sys
import time
import daemon
import os
from pathlib import Path
from getjobinfo import scraping
from database import db_connect, db_close

basPath  = "/Users/chiaki/Desktop/SlackBot"
filePath = "/tmp/"
fileName = "lockfile"
mode = sys.argv[1]

def post_slack():
    while True:
        if os.path.isfile(basPath + filePath + fileName):
            jobList = scraping()
            con, cur = db_connect()
            slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
        for jobInfo in jobList:
            sql = "SELECT id FROM job_info where url = %s"
            cur.execute(sql, (jobInfo[3],)) 
            cur.fetchone()
            row = cur.rowcount
            if row > 0:
                print('重複')
            else:
                message = "【会社名】" + "\n" + jobInfo[0] + "\n\n" + "【求人タイトル】" + "\n" + jobInfo[1] + "\n\n""【求人内容】" + "\n" + jobInfo[2] + "\n\n" + jobInfo[3]
                slack.notify(text=message)
                sql = "INSERT INTO job_info (company_name, title, summary, url, created_at) VALUES (%s, %s, %s, %s, now())"
                cur.execute(sql, (jobInfo[0],jobInfo[1],jobInfo[2],jobInfo[3],))
                con.commit()
            db_close(con, cur)
            time.sleep(3600)
        else:
            break

if mode == 'start':
    if os.path.isfile(basPath + filePath + fileName):
        print('起動中です')
    else:
        print('起動します')
        Path(basPath + filePath + fileName).touch()
    #標準出力あり
        with daemon.DaemonContext(stdout=sys.stdout):
    #with daemon.DaemonContext():
            post_slack()
elif mode == 'stop':
    os.remove(basPath + filePath + fileName)
