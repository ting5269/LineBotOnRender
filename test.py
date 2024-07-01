from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, AudioSendMessage
from linebot.models import FlexSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('gqHpZtd1vx5rrSoMSv12HUSx+fFw9lTKfAAuDgQDDdcNMOpA3jKEbC/gAquc4JGBvWomMnloLp8/40rNFdCQkm4f6v1kte5s1+76wS+9kQ/uPaQGTvyUAVehqo+BtanPV4GGasN+ICKchMKhpUoPlAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9a31037c985e085e319ec091700885c8')

# 用于存储每个用户的累积次数
user_counts = {}

# 勋章目标
milestones = [5, 10, 15, 20]

# 勋章图片 URL
milestone_images = {
    5: "https://i.imgur.com/4QfKuz1.png",
    10: "https://i.imgur.com/4QfKuz1.png",
    15: "https://i.imgur.com/4QfKuz1.png",
    20: "https://i.imgur.com/4QfKuz1.png"
}



# 回调函数
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 处理消息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_input = event.message.text

    if user_input == "你好":
        reply_text = "你好"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    elif user_input == "@+1":
        # 获取当前用户的累积次数，如果没有则初始化为0
        count = user_counts.get(user_id, 0) + 1
        user_counts[user_id] = count
        reply_text = "你好厲害"

        messages = [TextSendMessage(text=reply_text)]

        if count in milestones:
            # 发送对应勋章图片
            image_url = milestone_images[count]
            messages.append(ImageSendMessage(
                original_content_url=image_url,
                preview_image_url=image_url
            ))

        line_bot_api.reply_message(
            event.reply_token,
            messages
        )
    elif user_input == "@目前累積":
        # 获取当前用户的累积次数，如果没有则初始化为0
        count = user_counts.get(user_id, 0)
        next_milestone = next((m for m in milestones if m > count), None)
        if next_milestone:
            difference = next_milestone - count
            reply_text = f"目前累積次數為: {count}，還差 {difference} 次達到下一個勳章 ({next_milestone} 次)。"
        else:
            reply_text = f"目前累積次數為: {count}，已經達到所有勳章！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    elif user_input == "@重新計算":
        # 重置当前用户的累积次数为0
        user_counts[user_id] = 0
        reply_text = "累積次數已歸零。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    elif user_input == '五骨':
        try:
            message = ImageSendMessage(
                original_content_url = "https://i.imgur.com/BfLKgK8.png",
                preview_image_url = "https://i.imgur.com/BfLKgK8.png"
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    
    elif user_input == "五條老師":
        flex_message = FlexSendMessage(
            alt_text="69",
            contents={
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Flex Message Corp",
                            "color": "#FFFFFF",
                            "weight": "bold"
                        }
                    ]
                },
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/BfLKgK8.png",
                    "size": "xl"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Gojo Satoru",
                            "weight": "bold",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "Jujutsu Kaisen",
                            "align": "center"
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "Visit our website",
                                "uri": "https://youtu.be/4Wl8Lj53pEU?si=99GCqILY3CDlzza8"
                            }
                        }
                    ]
                },
                "styles": {
                    "header": {
                        "backgroundColor": "#00FFFF"
                    }
                }
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="收到訊息！")
        )
    

if __name__ == "__main__":
    app.run()
