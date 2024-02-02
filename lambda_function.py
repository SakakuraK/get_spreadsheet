import json
import re
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import boto3

# 保存先バケット名ディレクトリ名を指定
S3_BUCKET = os.environ['S3_BUCKET']
S3_DIRECTORY = os.environ['S3_DIRECTORY']

# 認証情報の設定
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials_file.json', scope)
client = gspread.authorize(creds)

def lambda_handler(event, context):
    
    s3 = boto3.resource('s3')
    #print("event->")
    #print(event)
    #print("context->")
    #print(context.aws_request_id)
    
    # POST内容が正しいかチェック
    if "body" in event:
        #ret = "ok"
        
        if "target_url" in event["body"]:
            #ret = "all ok"
            
            #print(event["body"])
            #url = "https://docs.google.com/spreadsheets/d/11SdpDMNyA-zOtAH7Zuj4lRg603Fst_rgsGfnlhXCii8/edit#gid=0"
            post_body = json.loads(event["body"])
            
            #print(post_body)
            url = post_body["target_url"]
            
            target_worksheet = "シート1"
        
            match = re.search(r'/d/([^\/]+)/', url)
            
            if match and match.group(1) != "":
                document_id = match.group(1)
                #print(document_id)
                # スプレッドシートにアクセス
                #URLの後ろパラメーターID指定でアクセス スプレッドシートIDは、スプレッドシートのURLから「/d/」と「/edit」の間の部分
                #sheet = client.open_by_key(document_id).worksheet(target_worksheet)
                sheet = client.open_by_key(document_id).get_worksheet(0)
            
                # sheet.get_all_records()は、スプレッドシートの最初の行をフィールド名として扱い、それをキーとする辞書のリストを返します。
                data = sheet.get_all_records()
                
                obj = s3.Object(f"{S3_BUCKET}",f"{S3_DIRECTORY}/{document_id}.json")
                
                s3_file_path = S3_DIRECTORY+"/"+document_id+".json"
                #print(data)
                
                obj.put(Body = json.dumps(data, ensure_ascii=False)) #←変数をJSON変換し S3にPUTする
                
                return {
                    'statusCode': 200,
                    'body': {
                            'mes':'get spreadsheet!',
                            's3_bucket_name':S3_BUCKET,
                            's3_file_path':s3_file_path
                    }
                }
                
            else:
                #print("Document ID not found in the URL.")
                return {
                    'statusCode': 500,
                    'body': json.dumps('error: spreadsheet ID not found in the URL.')
                }
            
            
            
            
        else:
            return {
                'statusCode': 500,
                'body': json.dumps('error: Argument is incomplete. Please set "target_url".')
            }
    else:
        #ret = "ng"
        return {
            'statusCode': 500,
            'body': json.dumps('error: Missing argument.')
        }
    
    
    
