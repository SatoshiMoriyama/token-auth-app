import json
from datetime import datetime


def lambda_handler(event, context):   
    # シンプルなレスポンスボディを準備
    response_body = {
        "message": "リクエストが正常に処理されました",
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }
    return response_body
