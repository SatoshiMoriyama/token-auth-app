import json
import uuid
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from momento import CacheClient, Configurations, CredentialProvider
from momento.responses import CacheGet, CacheSet


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda REQUEST オーソライザ関数
    Momento Cacheを使用してトークンをキャッシュする
    """
    try:
        # REQUEST オーソライザのイベント形式
        method_arn = event['methodArn']
        request_context = event.get('requestContext', {})
        headers = event.get('headers', {})
        
        # ホスト名を取得（キャッシュキーとして使用）
        host = headers.get('Host', 'unknown')
        
        # デバッグ用ログ
        print(f"Request ID: {request_context.get('requestId', 'unknown')}")
        print(f"Host header: {host}")
        
        # 常に許可する
        principal_id = "user"
        effect = "Allow"
        
        # 新しいトークンを生成
        new_token = create_token()
        
        # トークンをキャッシュに保存
        cache_success = cache_token(new_token, host)
        
        # ポリシーの生成
        policy = generate_policy(principal_id, effect, method_arn)
        policy['context'] = {
            'accessToken': new_token,
            'userId': principal_id,
            'timestamp': datetime.now().isoformat(),
            'requestId': request_context.get('requestId', 'unknown'),
            'cached': cache_success
        }
        
        return policy
        
    except Exception as e:
        print(f"オーソライザエラー: {str(e)}")
        print(f"Event: {event}")
        # エラーの場合でも許可する（新しいトークンを生成）
        fallback_token = create_token()
        return generate_policy("user", "Allow", event.get('methodArn', '*'), {
            'accessToken': fallback_token,
            'userId': 'user',
            'timestamp': datetime.now().isoformat(),
            'requestId': 'error-fallback',
            'cached': False
        })


def create_token() -> str:
    """
    新しいトークンを生成
    """
    return generate_token()


def cache_token(token: str, host: str) -> bool:
    """
    トークンをMomento Cacheに保存
    
    Args:
        token: 保存するトークン
        host: リクエスト元のホスト
    
    Returns:
        bool: キャッシュ保存成功時True、失敗時False
    """
    try:
        # トークンデータ
        token_data = {
            'token': token,
            'created_at': datetime.now().isoformat(),
            'host': host,
            'valid': True
        }
        
        # トークン自体をキーとしてキャッシュに保存
        cache_client = get_cache_client()
        cache_name = os.environ.get('MOMENTO_CACHE_NAME', 'token-cache')
        cache_key = token  # トークン自体をキーに使用
        
        ttl_seconds = int(os.environ.get('MOMENTO_TTL_SECONDS', '300'))
        set_response = cache_client.set(cache_name, cache_key, json.dumps(token_data), timedelta(seconds=ttl_seconds))
        
        if isinstance(set_response, CacheSet.Success):
            print(f"新しいトークンをキャッシュに保存: {cache_key}")
            return True
        else:
            print(f"キャッシュ保存エラー: {set_response}")
            return False
        
    except Exception as e:
        print(f"Momento Cache エラー: {str(e)}")
        return False


def get_cache_client() -> CacheClient:
    """
    Momento CacheClientを取得
    """
    # Lambda環境変数からAPI Keyを取得
    api_key = os.environ.get('MOMENTO_API_KEY')
    if not api_key:
        raise ValueError("MOMENTO_API_KEY environment variable is required")
    
    return CacheClient(
        configuration=Configurations.Laptop.v1(),
        credential_provider=CredentialProvider.from_string(api_key),
        default_ttl=timedelta(seconds=300)
    )


def generate_token() -> str:
    """
    新しいトークンを生成（タイムスタンプを含む）
    """
    import time
    timestamp = int(time.time() * 1000)  # ミリ秒単位のタイムスタンプ
    return f"{timestamp}-{uuid.uuid4().hex[:8]}"


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