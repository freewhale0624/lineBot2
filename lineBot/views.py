from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from lineBot.models import LineChat, PhotoAlbum, ChannelInfo

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,  ImageSendMessage
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
import tempfile, os

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
client = ImgurClient(settings.IMGUR_CLIENT_ID, settings.IMGUR_CLIENT_SECRET, settings.IMGUR_ACCESS_TOKEN, settings.IMGUR_REFRESH_TOKEN)
def hello_world(request):
    return HttpResponse("Hello World!")

# 忽略CSRF檢查
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)  # 傳入的事件
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            #如果事件為訊息
            if isinstance(event, MessageEvent):
                if event.message.type=='text':
                    text_logic(event)
                elif event.message.type=='image':
                    upload_to_imgur(0, event)                    
                elif event.message.type=='location':
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=str(event))
                    )
                elif event.message.type=='video':
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=str(event))
                    )
                elif event.message.type=='sticker':
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=str(event))
                    )
                elif event.message.type=='audio':
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=str(event))
                    )
                elif event.message.type=='file':
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=str(event))
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def text_logic(event):
    add_chat_logs(event)
    groupId, userId, text, photoId = get_event_info(event)
    if text == '給我一張圖片':
        #寫死圖片供測試
        give_me_a_picture(event.reply_token)
    elif text[:8] == '貼貼 我的相簿叫':
        channel = get_channel(groupId)
        alias = text[8:]
        if channel.imgurAlbum:
            client.update_album(
                channel.imgurAlbum,
                { 'ids': None, 'title': alias, } )
        update_channel(groupId, None, alias)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='好喔, 幫你把群組相簿改名為' + alias)
        )
    elif event.message.text[:7] == '貼貼 刪掉資料':
        del_channel(groupId)
        line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            TextSendMessage(text='Channel資料刪掉囉')
        )
    # message關鍵字邏輯
    else:
        line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            TextSendMessage(text=str(event))
        )

#獨立function處理, 程式會比較容易閱讀
def give_me_a_picture(token):
    photo = PhotoAlbum.objects.first()
    line_bot_api.reply_message(  # 回復傳入的訊息文字
        token,
        ImageSendMessage(
            original_content_url=photo.imageUrl,
            preview_image_url=photo.imageUrl,
        )
    )

def get_event_info(event):
    groupId = event.source.group_id if event.source.type == 'group' else event.source.user_id
    userId = event.source.user_id
    text = event.message.text if event.message.type == 'text' else ''
    photoId =  event.message.id if event.message.type == 'image' else ''
    return groupId, userId, text, photoId
    
def add_chat_logs(event):
    groupId, userId, text, photoId = get_event_info(event)
    LineChat.objects.create(
        groupId = groupId,
        userId = userId,
        type = event.message.type,
        text = text,
        photoid = photoId,
    )

def get_channel(groupId):
    channel = ChannelInfo.objects.get_or_create(
        groupId= groupId,
    )[0]
    return channel

def update_channel(groupId, imgurAlbum, alias):
    channel = ChannelInfo.objects.get_or_create(
        groupId= groupId,
    )[0]
    if imgurAlbum:
        print('update_channel imgurAlbum:', imgurAlbum)
        channel.imgurAlbum = imgurAlbum
    if alias:
        print('update_channel alias:', alias)
        channel.alias = alias
    channel.save()

def del_channel(groupId):
    ChannelInfo.objects.filter(groupId=groupId).delete()

def create_album(alias, ids):    
    try:
        album = client.create_album({'ids': ids, 'title': alias })
        return album['id']
    except ImgurClientError as e:
        print(e.error_message)
        print(e.status_code)
        return ''

def upload_to_imgur(retry, event):
    groupId, userId, text, photoId = get_event_info(event)
    message_content = line_bot_api.get_message_content(photoId)
    channel = get_channel(groupId)
    ext = 'jpg'
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name
    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)
    try:
        config = {
            'album': channel.imgurAlbum,
            'name': None,
            'title': None,
            'description': None
        }
        print(config)
        path = os.path.join('lineBot', 'static', 'tmp', dist_name)
        image = client.upload_from_path(path, config=config, anon=False)
        print(image)
        os.remove(path)
        if channel.imgurAlbum == '':
            print('alias:', channel.alias)
            alias = channel.alias if channel.alias > '' else groupId
            print('alias:', alias)
            imgurAlbum = create_album(alias, image['id'])
            print('imgurAlbum:', imgurAlbum)
            update_channel(groupId, imgurAlbum, alias)
        print('-----2 image')
        # PhotoAlbum.objects.create(
        #     groupId = groupId,
        #     userId = userId,
        #     type = event.message.type,
        #     text = text,
        #     photoid = photoId,
        # )
        line_bot_api.reply_message(
            event.reply_token,
                TextSendMessage(text='上傳成功'))
    except ImgurClientError as e:
        retry += 1
        print('retry: ', retry)
        print(e.error_message)
        print(e.status_code)
        os.remove(path)
        if retry < 3:
            upload_to_imgur(retry, event)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳失敗'))
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='上傳失敗'))
