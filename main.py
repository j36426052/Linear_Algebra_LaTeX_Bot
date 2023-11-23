from dotenv import load_dotenv
import os
import requests
import json

# 前置作業

## 載入 .env 檔案
load_dotenv()
SECRETS = os.getenv('SECRETS')

def get_questions(week):
    ## 存取環境變數
    DATABASE_ID = os.getenv('DATABASE_ID')
    # 設定 HTTP 請求

    ## 設定 URL

    url = "https://api.notion.com/v1/databases/"+DATABASE_ID+"/query"

    ## 設定請求標頭
    headers = {
        'Authorization': f'Bearer {SECRETS}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

    # 設定請求主體
    data = {
        "filter": {'and':[
            { 'or':[
            {"property":"題目狀態",
            'status':{
                'equals':"寫完了，需要確認"
            }},
            {"property":"題目狀態",
            'status':{
                'equals':"完成"
            }}
            ]},
            {"property":"第幾次",
            'select':{
                'equals':week
            }}
            ]}
    }

    # 發送請求
    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    # 輸出回應內容
    result = json.loads(response.text)

    # 經常用到的 result 們，以 a in result["results"] 作為出發點

    questions = []

    for a in result["results"]:
        question = {}
        question['status'] = a['properties']['題目狀態']['status']['name']
        names = []
        for item in a['properties']['解題人員']['multi_select']:
            #print(a)
            names.append(item['name'])
        question['names'] = names
        question['title'] = a['properties']['Name']['title'][0]['text']['content']
        question['id'] = a['id']
        questions.append(question)
        #print(question)
    return questions

def get_page_content(pageid):
    url = "https://api.notion.com/v1/blocks/"+pageid+"/children?page_size=100"
    #print(url)
    headers = {
        'Authorization': f'Bearer {SECRETS}',
        'Notion-Version': '2022-06-28'
    }

    response = requests.get(
        url,
        headers=headers
    )

    # 輸出回應內容
    result = json.loads(response.text)
    resultList= result["results"]

    # 有error就重來一次
    counter = len(resultList)-1
    print(counter)
    for i in range(0,counter):
        try:
            cool = resultList[counter-i]["code"]["rich_text"][0]["text"]["content"]
            print(cool)
            break
        except:
            print('change')

    #try:
    #    cool = resultList[len(resultList)-1]["code"]["rich_text"][0]["text"]["content"]
    #except:
    #    print(resultList)
    #    cool = 'nope'
    try:
        print(cool)
    except:
        print(resultList[1])
    return cool


front = """
\\documentclass
[answers]
{exam}
\\usepackage[english]{babel}
\\usepackage[utf8x]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage[a4paper,margin = 2cm]{geometry}
\\usepackage{amsmath,amsthm,amssymb}
\\usepackage{graphicx}
\\usepackage{tcolorbox}
\\usepackage{tasks}
\\usepackage{paralist}
\\usepackage{mathrsfs}
\\newcommand{\\N}{\\mathbb{N}}
\\newcommand{\\Z}{\\mathbb{Z}}
\\newcommand{\\R}{\\mathbb{R}}
\\everymath{\\displaystyle}
\\usepackage{xeCJK}   % Chinese input settings
\\setCJKmainfont{標楷體} % Windows使用者請使用這行

\\begin{document}
\\begin{questions}
"""

back = """
\\end{questions}

\\end{document}
"""

mid = ''

for question_set in get_questions('二'):
    main = get_page_content(question_set['id'])
    mid += main

    status = question_set['status']
    names = ''
    for name in question_set['names']:
        names += name + '  '
    qid = question_set['title']
    # names = question_set[names]

    property = f"""
    \\begin{{tcolorbox}}
    狀態：{status}  負責人：{names}  題號{qid}
    \\end{{tcolorbox}}
    """
    mid += property

with open('file/main.tex', 'w', encoding='utf-8') as file:
    file.write(front + mid + back)

#questions = get_questions('二')
#print(questions)
#https://www.notion.so/2-1-3-823d2bb4bd78487b8e66a9de0766ed4d?pvs=4
#get_page_content('823d2bb4-bd78-487b-8e66-a9de0766ed4d')