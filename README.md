# get_spreadsheet
Googleスプレッドシートの内容を取り込んでjson形式でS3にアップするlambdaプログラムソース

実行の仕方

curlコマンドで

curl -X POST 【awsLambdaの関数URL】 -H "Content-Type: application/json"  -d '{ "target_url": "【取得したいGoogleスプレッドシートのURL】" }'
を実行。

取得したいGoogleスプレッドシートには
予めGCPで発行したスプレッドシート閲覧可能なサービスアカウント
に対しての閲覧許可を付けておく。

サービスアカウントのcredentialのjsonファイルをcredentials_file.jsonとして
プログラムと同階層に置く。
