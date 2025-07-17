#!/usr/bin/env python3
"""
ローカルテスト用スクリプト（オーソライザ付き版）
"""
import json
import sys
import os

# パスにauthorizerとhello_worldを追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'authorizer'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'hello_world'))

from authorizer.app import lambda_handler as authorizer_handler
from hello_world.app import lambda_handler as api_handler


def test_authorizer():
    """REQUESTオーソライザのテスト（常に許可）"""
    print("=== REQUESTオーソライザのテスト ===")
    
    # REQUEST形式のイベント
    event = {
        "methodArn": "arn:aws:execute-api:us-east-1:123456789012:abcdef123/test/GET/hello",
        "requestContext": {
            "requestId": "test-request-id-123456",
            "httpMethod": "GET",
            "resourcePath": "/hello"
        },
        "headers": {
            "Host": "api.example.com",
            "Authorization": "Bearer any-token"
        }
    }
    
    result = authorizer_handler(event, None)
    print(f"オーソライザの結果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    return result


def test_api_with_context():
    """APIハンドラーのテスト（オーソライザコンテキスト付き）"""
    print("\n=== APIハンドラーのテスト ===")
    
    # オーソライザから受け取った情報をシミュレート
    event = {
        "requestContext": {
            "authorizer": {
                "accessToken": "temp-token-abc123def456",
                "userId": "user",
                "timestamp": "2024-01-01T12:00:00"
            }
        },
        "httpMethod": "GET",
        "path": "/hello"
    }
    
    result = api_handler(event, None)
    print(f"APIレスポンス（非プロキシ統合）: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    return result


def main():
    """メイン関数"""
    print("オーソライザ付きトークン生成システムのローカルテスト")
    print("=" * 60)
    
    # オーソライザのテスト
    auth_result = test_authorizer()
    
    # APIハンドラーのテスト
    api_result = test_api_with_context()
    
    print("\n=== テスト完了 ===")
    print("オーソライザは常に許可してトークンを生成します")
    print(f"生成されたトークン: {auth_result.get('context', {}).get('accessToken', 'なし')}")
    print("\n実際のAPIエンドポイントでは:")
    print("- Authorization ヘッダが必要（任意の値でOK）")
    print("- X-Access-Token ヘッダにトークンが含まれます")
    print("- レスポンスボディにもトークン情報が含まれます")


if __name__ == "__main__":
    main()