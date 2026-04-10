import json
import os
import urllib.request

import anthropic

diff = open("/tmp/pr_diff.txt").read()
if not diff.strip():
    print("差分なし。レビューをスキップします。")
    exit(0)

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": (
                "以下の Python コードの差分をレビューしてください。\n\n"
                "観点:\n"
                "- バグ・クラッシュの可能性\n"
                "- セキュリティ上の問題\n"
                "- 明らかなロジックの誤り\n\n"
                "問題がなければ「問題なし」とだけ返してください。\n"
                "問題がある場合のみ、箇条書きで簡潔に指摘してください。\n"
                "改善提案や細かいスタイルの指摘は不要です。\n\n"
                f"```diff\n{diff}\n```"
            ),
        }
    ],
)

review = message.content[0].text
pr = os.environ["PR_NUMBER"]
repo = os.environ["REPO"]
token = os.environ["GH_TOKEN"]

body = json.dumps({"body": f"🤖 **自動レビュー**\n\n{review}"}).encode()
req = urllib.request.Request(
    f"https://api.github.com/repos/{repo}/issues/{pr}/comments",
    data=body,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    },
)
urllib.request.urlopen(req)
print("レビューコメントを投稿しました。")
