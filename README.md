# Token Auth App

## システム概要

このプロジェクトは、AWS API Gateway の機能を使用してトークンを生成・配布するサーバーレスアプリケーションです。認証機能は含まず、シンプルにトークンを発行することに特化しています。

### 主な特徴

- **認証不要**: 誰でもアクセス可能なパブリックAPI
- **API Gateway主導**: トークン生成とヘッダマッピングをAPI Gatewayの機能で実現
- **バックエンド最小化**: Lambda関数は基本的なレスポンスのみを返却
- **非永続化**: トークンは永続化されません（一時的な利用のみ）

### アーキテクチャ

1. **GET /hello** エンドポイントへのリクエスト
2. **Lambda関数** が基本的なレスポンスを返却
3. **API Gateway** がマッピングテンプレートでトークンを生成
4. **レスポンス** にトークンがヘッダ (`X-Access-Token`) とボディに含まれる

### 生成されるトークン

- フォーマット: `temp-token-{requestId}`
- 例: `temp-token-12345678-1234-1234-1234-123456789012`
- リクエストごとにユニークなトークンが生成されます

### プロジェクト構成

- `hello_world/` - Lambda関数のコード
- `template.yaml` - AWS SAMテンプレート（API Gateway設定含む）
- `test_local.py` - ローカルテスト用スクリプト
- `events/` - 関数呼び出し用イベントデータ
- `tests/` - ユニットテスト

### API仕様

#### エンドポイント
- **URL**: `/hello`
- **メソッド**: GET
- **認証**: 不要

#### レスポンス
- **ステータス**: 200 OK
- **ヘッダ**: 
  - `X-Access-Token`: 生成されたアクセストークン
  - `Access-Control-Allow-Origin`: *
  - `Access-Control-Expose-Headers`: X-Access-Token
- **ボディ**: JSON形式でトークン情報を含む

```json
{
  "message": "リクエストが正常に処理されました",
  "timestamp": "2025-07-17T04:57:10.538062",
  "status": "success",
  "newToken": "temp-token-12345678-1234-1234-1234-123456789012",
  "hasNewToken": true,
  "note": "トークンはAPI Gatewayで生成されました",
  "requestId": "12345678-1234-1234-1234-123456789012"
}
```

## 使用方法

### ローカルテスト

```bash
# Lambda関数のテスト
python3 test_local.py
```

### ビルドとデプロイ

```bash
# ビルド
sam build

# デプロイ
sam deploy --guided
```

### APIの呼び出し

```bash
# デプロイ後のエンドポイント例
curl -X GET https://your-api-id.execute-api.region.amazonaws.com/Prod/hello

# レスポンス例
HTTP/1.1 200 OK
X-Access-Token: temp-token-12345678-1234-1234-1234-123456789012
Access-Control-Allow-Origin: *
Access-Control-Expose-Headers: X-Access-Token
Content-Type: application/json

{
  "message": "リクエストが正常に処理されました",
  "timestamp": "2025-07-17T04:57:10.538062",
  "status": "success",
  "newToken": "temp-token-12345678-1234-1234-1234-123456789012",
  "hasNewToken": true,
  "note": "トークンはAPI Gatewayで生成されました",
  "requestId": "12345678-1234-1234-1234-123456789012"
}
```

## 技術仕様

- **AWS SAM**: サーバーレスアプリケーションフレームワーク
- **AWS Lambda**: Python 3.9 ランタイム
- **AWS API Gateway**: REST API（非プロキシ統合）
- **マッピングテンプレート**: VTL（Velocity Template Language）によるトークン生成

## 注意事項

- トークンは永続化されません
- 認証機能は含まれていません
- 本番環境での使用には適切なセキュリティ対策が必要です

---

## 開発環境セットアップ

If you prefer to use an integrated development environment (IDE) to build and test your application, you can use the AWS Toolkit.  
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS. The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code. See the following links to get started.

* [CLion](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [GoLand](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [WebStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [Rider](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PhpStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [RubyMine](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [DataGrip](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
token-auth-app$ sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
token-auth-app$ sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
token-auth-app$ sam local start-api
token-auth-app$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

## Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
token-auth-app$ sam logs -n HelloWorldFunction --stack-name "token-auth-app" --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
token-auth-app$ pip install -r tests/requirements.txt --user
# unit test
token-auth-app$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
token-auth-app$ AWS_SAM_STACK_NAME="token-auth-app" python -m pytest tests/integration -v
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sam delete --stack-name "token-auth-app"
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
