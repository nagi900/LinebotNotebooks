from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    MessageAction,
    TemplateSendMessage,
    ButtonsTemplate,
)
import os

import random
import time
#import cv2

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

now_user_id=0

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
def handle_text_message_konotanngowotsuika(event):#


    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    print (f"profileの中身を表示します！！！！中身は{profile}です!")
    print (f"あなたの名前を表示します！！あなたは{name}です！")

    subject = False

    if event.message.text.startswith("メモ") or event.message.text.startswith("めも") or event.message.text.startswith("め\n"):
        subject = "memorandum"
        subject_name = "メモ"        
 
    elif event.message.text.startswith("か\n") or event.message.text.startswith("カレンダー"):
        subject = "calender"
        subject_name = "カレンダー"
        

    if not subject:
        
        #img_thumbnail = cv2.imread(f"../img/thumbnail/{subject}.png") #subject名でサムネイル画像を取得(あんま良くないかも)
        line_bot_api.push_message(profile.user_id,TextMessage(text=f"{back_channeling} {subject_name}ね"))
        #line_bot_api.push_message(profile.user_id,
        #    TemplateSendMessage(alt_text="bottons template",
        #        template=ButtonsTemplate(
        #            thumnail_image_url=profile.picture_url,
        #            title=f"{subject_name}",
#
        #        )))

 
    line_bot_api.reply_message(event.reply_token,
                                [TextSendMessage(text=event.message.text + "\n okよ"),
                                TextMessage(text=name),
                                TextMessage(text=profile.user_id),
                                TextMessage(text=back_channeling)])
    
    time.sleep(10)

    line_bot_api.push_message(profile.user_id,TextMessage(text="プッシュできてるよ！"))
#応答は一度しかできない 配列で返せば5つまでいける

#↓これができない
#@handler.add(MessageEvent, message=TextMessage)
#def handle_text_message_konobunnshouwotsuika(event):#
##    time.sleep(20.0)
#    line_bot_api.push_message(to=,TextMessage(text=back_channeling))