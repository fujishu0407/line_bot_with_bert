#"NcSKlH2/i1Gvv2eW38+VMRSSPuKgxY+vMtqUWcU5GzmpwWJYv6QiIuI+LtWLV2eIaSLiAv/egHlpnVM0ha3cDDUTHZeIqhzhqZiz8ve8FDlFYGB956+E9ZKUwdvXYc9oRJnKVfAF4cfxPHiLTl/+jwdB04t89/1O/w1cDnyilFU="
#"3b6a26385dfd37f84997ed2394f6def8"
from flask import Flask, request, abort
import os
import subprocess
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from bert_ebdm_system import BertEbdmSystem


app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = "NcSKlH2/i1Gvv2eW38+VMRSSPuKgxY+vMtqUWcU5GzmpwWJYv6QiIuI+LtWLV2eIaSLiAv/egHlpnVM0ha3cDDUTHZeIqhzhqZiz8ve8FDlFYGB956+E9ZKUwdvXYc9oRJnKVfAF4cfxPHiLTl/+jwdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "3b6a26385dfd37f84997ed2394f6def8"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
        abort(200)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    output_message = system.reply(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=output_message["utt"]))


if __name__ == "__main__":
#    app.run()
    subprocess.call(["elasticsearch/bin/elasticsearch", "-d", "-p", "pid"])
    port = int(os.environ.get("PORT", 5000))
    print(port)
    system = BertEbdmSystem()
    app.run(host="0.0.0.0", port=port)
