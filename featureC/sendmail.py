"""
Send E-Mail with GMail.

Usage:
  sendmail.py  <to>  [--road_attach_file_path=<file_path>][--dirty_attach_file_path=<file_path>] [--cc=<cc>]
  sendmail.py -h | --help
  sendmail.py --version

Options:
  -h --help     Show this screen.
  --version     Show version. 
  --road_attach_file_path=<file_path>     Path of file attached to message.
  --dirty_attach_file_path=<file_path>     Path of file attached to message.
  --cc=<cc>     cc email address list(separated by ','). Default None.
"""
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from pathlib import Path

from email.mime.multipart import MIMEMultipart
import mimetypes
from apiclient import errors
from .gmail_credential import get_credential
from docopt import docopt
import logging

logger = logging.getLogger(__name__)


def create_message(sender, to, subject, message_text, cc=None):
    """
    MIMEText を base64 エンコードする
    """
    enc = "utf-8"
    message = MIMEText(message_text.encode(enc), _charset=enc)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    if cc:
        message["Cc"] = cc
    encode_message = base64.urlsafe_b64encode(message.as_bytes())
    return {"raw": encode_message.decode()}


def create_message_with_attachment(
    sender:str, to:str, subject:str, message_text:str, file_path_list:list[str], cc:str | None=None
):
    """
    添付ファイルつきのMIMEText を base64 エンコードする
    """
    message = MIMEMultipart()
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    if cc:
        message["Cc"] = cc
    # attach message text
    enc = "utf-8"
    #pdfが存在しない場合
    for i,file in enumerate(file_path_list):
        if i%2!=0:
            if not os.path.exists(file):
                with open('featureC/error.txt', "r", encoding="utf-8") as fp:
                    msg = MIMEText(fp.read(), _subtype= 'plain')
                    message.attach(msg)
                    print("pdfがないよ-")
            else :
                    message.attach(message_text)
                    print("pdfあったよ-")
            
            content_type, encoding = mimetypes.guess_type(file)

            if content_type is None or encoding is not None:
                content_type = "application/octet-stream"
                
            main_type, sub_type = content_type.split("/", 1)
            if main_type == "text":
                with open(file, "rb") as fp:
                    msg = MIMEText(fp.read(), _subtype=sub_type)
            elif main_type == "image":
                with open(file, "rb") as fp:
                    msg = MIMEImage(fp.read(), _subtype=sub_type)
            elif main_type == "audio":
                with open(file, "rb") as fp:
                    msg = MIMEAudio(fp.read(), _subtype=sub_type)
            elif main_type == "application":
                with open(file, "rb") as fp:
                    msg = MIMEApplication(fp.read(), _subtype=sub_type)
            else:
                if os.path.exists(file):
                    with open(file, "rb") as fp:
                        msg = MIMEBase(main_type, sub_type)
                        msg.set_payload(fp.read())
                        print("できたぞー")
                else : 
                    print("失敗")
                    
            p = Path(file)
            msg.add_header("Content-Disposition", "attachment", filename=p.name)
            message.attach(msg)
#
    encode_message = base64.urlsafe_b64encode(message.as_bytes())
    return {"raw": encode_message.decode()}


def send_message(service, user_id, message):
    """
    メールを送信する

    Parameters
    ----------
    service : googleapiclient.discovery.Resource
        Gmail と通信するためのリソース
    user_id : str
        利用者のID
    message : dict
        "raw" を key, base64 エンコーディングされた MIME Object を value とした dict

    Returns
    ----------
    なし
    """
    try:
        sent_message = (
            service.users().messages().send(userId=user_id, body=message).execute()
        )
        logger.info("Message Id: %s" % sent_message["id"])
        return None
    except errors.HttpError as error:
        logger.info("An error occurred: %s" % error)
        raise error


#  メイン処理
# pdf_info_list = 一次元配列[road_path,road_flg,dirty_path,dirty_flg]
def main_C(to,  pdf_info_list):
    # アクセストークンの取得とサービスの構築
    sender = "yutakil0414@gmail.com"#送り主
    subject = "取得結果"#件名
    cc = ""
    with open('featureC/mainText.txt', "r", encoding="utf-8") as fp:#本文
             msg = MIMEText(fp.read(), _subtype= 'plain')
             message_text = msg
             print(msg)
    creds = get_credential()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    if pdf_info_list[0]:#road
        if pdf_info_list[2]:#dirty
            # メール本文の作成
            message = create_message_with_attachment(
                sender, to, subject, message_text, pdf_info_list, cc=cc
            )
    else:
        message = create_message(
            sender, to, subject, message_text, cc=cc
        )
    
    # メール送信
    #if len==count:
    send_message(service, "me", message)


# プログラム実行部分

# if __name__ == "__main__":
#     arguments = [['該当する情報はありません。', False, '該当する情報はありません。', False], ['image_path大門町2丁目1-1.pdf', True, 'image_duty大門町2丁目1-1.pdf', True], ['image_path沼影１丁目２０番地１号.pdf', True, 'image_duty沼影１丁目２０番地１号.pdf', True]]
#     #ユーザー様のメールアドレス（送り先）
#     to = "yutakil0414@gmail.com" 
    
    
#     logging.basicConfig(level=logging.DEBUG)

#     for args in arguments:

#         main_C(
#             to=to,
#             pdf_info_list=args,
#         )