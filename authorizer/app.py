import json
import uuid
from datetime import datetime
from typing import Dict, Any


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda REQUEST オーソライザ関数
    常に許可してトークンを発行する（キャッシュ無効化）
    """
    try:
        # REQUEST オーソライザのイベント形式
        method_arn = event['methodArn']
        request_context = event.get('requestContext', {})
        headers = event.get('headers', {})
        
        # デバッグ用ログ
        print(f"Request ID: {request_context.get('requestId', 'unknown')}")
        print(f"Host header: {headers.get('Host', 'unknown')}")
        
        # 常に許可する
        principal_id = "user"
        effect = "Allow"
        
        # ポリシーの生成
        policy = generate_policy(principal_id, effect, method_arn)
        
        # 新しいトークンを生成してコンテキストに含める
        new_token = generate_token()
        policy['context'] = {
            'accessToken': new_token,
            'userId': principal_id,
            'timestamp': datetime.now().isoformat(),
            'requestId': request_context.get('requestId', 'unknown')
        }
        
        return policy
        
    except Exception as e:
        print(f"オーソライザエラー: {str(e)}")
        print(f"Event: {event}")
        # エラーの場合でも許可する（トークンは生成）
        fallback_token = generate_token()
        return generate_policy("user", "Allow", event.get('methodArn', '*'), {
            'accessToken': fallback_token,
            'userId': 'user',
            'timestamp': datetime.now().isoformat(),
            'requestId': 'error-fallback'
        })


def generate_token() -> str:
    """
    新しいトークンを生成（タイムスタンプを含む）
    """
    import time
    timestamp = int(time.time() * 1000)  # ミリ秒単位のタイムスタンプ
    return f"temp-token-{timestamp}-{uuid.uuid4().hex[:8]}"


def generate_policy(principal_id: str, effect: str, resource: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    IAM ポリシーを生成
    """
    policy = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': resource
                }
            ]
        }
    }
    
    if context:
        policy['context'] = context
    
    return policy