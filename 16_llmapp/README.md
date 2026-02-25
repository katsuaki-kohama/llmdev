# 16_llmapp

## キャラクター（System Prompt）の設定

このアプリでは、LLMに対して「あなたはねこです。」のようなキャラクター設定を **system メッセージ** として最初に1回だけ付与できます。

### 設定方法

1. リポジトリ直下の `.env` に `SYSTEM_PROMPT` を追加します（無ければ新規作成）。

例:

```env
API_KEY=sk-...
SYSTEM_PROMPT=あなたはねこです。語尾に「にゃ」を付けて、短めに答えてください。
```

2. Flaskアプリを再起動します。

### 反映される場所

- チャット（RAGあり）: `16_llmapp/chatbot/graph.py`
- チャット（検索のみ）: `16_llmapp/original/graph.py`

`SYSTEM_PROMPT` が空の場合は system メッセージを付与しません。
