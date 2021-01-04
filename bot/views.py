from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)
import os

import random

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#後で送信情報からuser_idを取得できるように変更
user_id = os.environ["YOUR_USER_ID"]
#

#返事
back_channelings = ["おっけ","りょ","うい","あい","おけい","まかせな"]
back_channeling=back_channelings[random.randint(0,5)]

@csrf_exempt
def callback(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        HttpResponseForbidden()
    return HttpResponse('OK', status=200)


# オウム返し
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    
    line_bot_api.reply_message(event.reply_token,
                                [TextSendMessage(text=event.message.text + "\n okよ"),
                                TextMessage(text="相槌が二回きたらok"),
                                TextMessage(text=back_channeling)])
#応答は一度しかできない 配列で返せば5つまでいける

#↓これができない
    line_bot_api.push_message(user_id,TextMessage(text=back_channeling))