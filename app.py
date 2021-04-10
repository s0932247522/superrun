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
def handle_message(event):
    msg = event.message.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='HI'))


if __name__ == "__main__":
    app.run()