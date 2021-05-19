import os
import datetime
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage,
        TemplateSendMessage, PostbackEvent, ConfirmTemplate, 
        PostbackTemplateAction
    )

from PLUTUSnews.PLUTUSnews import PLUTUSnews
from Flex.flex import news_flex

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
    textm = event.message.text
    userid = event.source.user_id
    
    nowtime = datetime.datetime.now().strftime('%Y%m%d')
    ret = [] # 欲回傳訊息包

    try:
        tparse = datetime.datetime.strptime(textm, '%Y%m%d') # Validate input format
        
    except:
        tparse = False
        ret.append(TextSendMessage(text = "您輸入：" + textm))
        ret.append(TextSendMessage(text = "無法辨識格式，以預設替代"))
    
    query_time = textm if tparse != False else nowtime
    nn, ss = PLUTUSnews(textm, ['美吾華', '恆大'], 0.3)
    print("PLUTUS is running!")
        
    dd = nn.append(ss, ignore_index=True)
    title = list(dd["title"]); link = list(dd["link"])
    
    if len(dd) != 0:
        ret.append(news_flex(title, link))
    else:
        ret.append(TextSendMessage(text = "CKIP 編碼錯誤"))
        
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
