import json
from datetime import datetime


def lambda_handler(event, context):
    """
    API Gateway Lambda 非プロキシ統合用の関数
    トークン生成はAPI Gatewayの機能で実現
    バックエンドではシンプルなレスポンスのみ
    """
    
    # シンプルなレスポンスボディを準備
    response_body = {
        "message": "リクエストが正常に処理されました",
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }
    
    # 非プロキシ統合の場合、シンプルなレスポンスを返す
    return response_body
