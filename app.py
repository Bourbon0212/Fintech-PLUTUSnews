import os
from flask import Flask, request, abort, jsonify, send_from_directory

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage,
        TemplateSendMessage, CarouselTemplate, PostbackEvent,
        StickerMessage, StickerSendMessage, ImagemapSendMessage,
        ImageMessage, ImageSendMessage, LocationMessage,
        ConfirmTemplate, PostbackTemplateAction
    )

app = Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False

# TOKEN
line_bot_api = LineBotApi('Fcc2xyMTJM4Zs6bPLT+DfErQ18COclbykE97QCUBTWMtI4qjpNYRPXPwaZ+FSPy4w0kqJ9wWN/6NcEWX7yYsyMaUE0NHeGRGyMEQ0kkew//YinTNGgWt/CITHEpYVppkv4jdYHlDbDqYalDT3lmu0wdB04t89/1O/w1cDnyilFU=')
# SECRET
handler = WebhookHandler('7daab4648e8e75a4208d4379d4495e2c')

""" 這是 LINE Webhook 預設要的 """
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature'] # get X-Line-Signature header value
    body = request.get_data(as_text=True) # get request body as text
    app.logger.info("Request body: " + body)

    try: # handle webhook body
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)
    return 'OK'

""" 處理文字訊息 """
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    userid = event.source.user_id

    # 決定你要讓『機器人』說甚麼話
    if text == "安安你好":
        ret1 = TextSendMessage(text = "你好挖，讓我們開始實作吧！")
        ret2 = TemplateSendMessage(
                    alt_text = 'Confirm template',
                    template = ConfirmTemplate(
                        text = "這是一個確認按鈕",
                        actions = [
                            PostbackTemplateAction(label = '左邊', text = '我按了左邊', data = 'left'),
                            PostbackTemplateAction(label = '右邊', text = '我按了右邊', data = 'right')
                        ]
                    )
                )
        ret = [ret1, ret2]
        # 讓『機器人』說出來
        line_bot_api.reply_message(event.reply_token, ret)
    else:
        ret = TextSendMessage(text = text)
        # 讓『機器人』說出來
        line_bot_api.reply_message(event.reply_token, ret)

""" 處理按鈕觸發事件 """
@handler.add(PostbackEvent)
def handle_postback(event):
    userid = event.source.user_id
    data = event.postback.data

    # 決定你要讓『機器人』說甚麼話
    if data in ['left', 'right']:
        ret = TextSendMessage(text = "我是從 Postback 進來的唷")
        # 讓『機器人』說出來
        line_bot_api.reply_message(event.reply_token, ret)
