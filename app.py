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

line_bot_api = LineBotApi('38Y1NHT1a51+j39ZR9aaUeRrzRzUGWdjLtEBjLO00IAVFY7kpZiF39SM9Ne8rGqDeXK06iiF5IHwoRcNY6Oy+PMMF69ZKNTFHNkS2L/qXnOG5UkxmA2ymJv5lW+GqzO2iBDKkocMWtki81aonxc8HQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5fd7e19c927d94092f0c6759b4e1ccf4')


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
    s = '你吃飯了嗎?'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s))


if __name__ == "__main__":
    app.run()