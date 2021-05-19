from linebot.models import (
    FlexSendMessage
)

def news_flex(title, link):
    flex_content = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "新聞推播",
                "weight": "bold",
                "size": "xl"
                },
                {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                # news unit here
                ]
                }
            ]
        }
        }
    
    for t, l in zip(title, link):     
        news_unit = {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
                {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                    {
                    "type": "text",
                    "text": t,
                    "wrap": True,
                    "color": "#3C5C97",
                    "size": "xs",
                    "flex": 5,
                    "action": {
                        "type": "uri",
                        "label": "link",
                        "uri": l,
                        "altUri": {
                            "desktop": l
                            }
                        }
                    }
                ]
                }
                ]
            }
        
        flex_content["body"]["contents"][1]["contents"].append(news_unit)

    flex_message = FlexSendMessage(
        alt_text="新聞推播", contents=flex_content)
    
    return flex_message

# tt = news_flex(list(dd["title"]), list(dd["link"]))