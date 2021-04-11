from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import pygsheets
# 匯入憑證碼的json檔
app = Flask(__name__)

line_bot_api = LineBotApi('IOmxiatB18j0urE8jbRQGxi4Kbrf7ZjVpfVk2svFCh+JoRF45vRe9/wanzNb4j54T8TuCICf7rhl7OPypV2qnCpa6l8PrSUUzoR4O4nSEOXbdyGIoN+Isn5ezMtcn7GkYUJjNQjqDVv+Fc34fTVUVgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('92f35de5943c5deeb8b57bff35e1b3b0')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'




@handler.add(MessageEvent, message=TextMessage)
def week_grades(week):
    if week == '1':
        week_find = 'week1_find'
    elif week == '2':
        week_find = 'week2_find'
    elif week == '3':
        week_find = 'week3_find'
    elif week == '4':
        week_find = 'week4_find'
    elif week == '5':
        week_find = 'week5_find'
    elif week == '6':
        week_find = 'week6_find'
    else:
        week_find = 'week1_find'

    return week_find

def personal(name):
    for cell in range(2,56):
        cel = 'B' + str(cell)
        if ws.get_value(cel)[11:] == name:
            goal = ws.get_value('C' + str(cell))
            now = ws.get_value('D' + str(cell))
            achieve = ws.get_value('E' + str(cell))
            disparity = ws.get_value('F' + str(cell))
            return goal, now, achieve, disparity

def handle_message(event):
    msg = event.message.text
    
    if '超跑隊' in msg:
        gc = pygsheets.authorize(service_account_file='superrun.json')
        # 輸入要更改的Googles Sheets網址（也可直接用 Google Sheets 的 ID ）
        gs_url = 'https://docs.google.com/spreadsheets/d/1mk9luUpS0h2XHZ1p2gKECADIMc-hdAjXQlxPM-9F40U/edit#gid=0'
        # 開啟該Google sheets
        sh = gc.open_by_url(gs_url)
        msg_week = msg[-1:]
        ws = sh.worksheet_by_title(week_grades(msg_week))
        msg_name = msg[3:-1]
        g, n, a, d = personal(msg_name)
        rate = round(int(n) / int(g) * 100, 2)
        # print(msg[3:-1], g, n, a, d)
        val = msg[3:-1] + '\n目標步數：' + g + '\n當前步數：' + n + '\n是否達成：' + a + '\n還差幾步：' + d + + '\n達成率為：' + rate 


    


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=val))


if __name__ == "__main__":
    app.run()