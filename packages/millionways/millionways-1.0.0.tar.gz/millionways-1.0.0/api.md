# GetCall

Types:

```python
from millionways.types import GetCallRetrieveResponse
```

Methods:

- <code title="get /get-call/{callId}">client.get_call.<a href="./src/millionways/resources/get_call.py">retrieve</a>(call_id, \*\*<a href="src/millionways/types/get_call_retrieve_params.py">params</a>) -> <a href="./src/millionways/types/get_call_retrieve_response.py">GetCallRetrieveResponse</a></code>

# GetUserAnalysis

Types:

```python
from millionways.types import GetUserAnalysisRetrieveResponse
```

Methods:

- <code title="get /get-user-analysis/{userId}">client.get_user_analysis.<a href="./src/millionways/resources/get_user_analysis.py">retrieve</a>(user_id, \*\*<a href="src/millionways/types/get_user_analysis_retrieve_params.py">params</a>) -> <a href="./src/millionways/types/get_user_analysis_retrieve_response.py">GetUserAnalysisRetrieveResponse</a></code>

# GetUserChats

Types:

```python
from millionways.types import GetUserChatRetrieveResponse
```

Methods:

- <code title="get /get-user-chats/{userId}">client.get_user_chats.<a href="./src/millionways/resources/get_user_chats.py">retrieve</a>(user_id, \*\*<a href="src/millionways/types/get_user_chat_retrieve_params.py">params</a>) -> <a href="./src/millionways/types/get_user_chat_retrieve_response.py">GetUserChatRetrieveResponse</a></code>

# CreateUser

Types:

```python
from millionways.types import CreateUserCreateResponse
```

Methods:

- <code title="post /create-user">client.create_user.<a href="./src/millionways/resources/create_user.py">create</a>(\*\*<a href="src/millionways/types/create_user_create_params.py">params</a>) -> <a href="./src/millionways/types/create_user_create_response.py">CreateUserCreateResponse</a></code>

# CategorizeText

Types:

```python
from millionways.types import CategorizeTextClassifyResponse, CategorizeTextClassifyByUserResponse
```

Methods:

- <code title="post /categorize-text">client.categorize_text.<a href="./src/millionways/resources/categorize_text.py">classify</a>(\*\*<a href="src/millionways/types/categorize_text_classify_params.py">params</a>) -> <a href="./src/millionways/types/categorize_text_classify_response.py">CategorizeTextClassifyResponse</a></code>
- <code title="post /categorize-text/{userId}">client.categorize_text.<a href="./src/millionways/resources/categorize_text.py">classify_by_user</a>(user_id, \*\*<a href="src/millionways/types/categorize_text_classify_by_user_params.py">params</a>) -> <a href="./src/millionways/types/categorize_text_classify_by_user_response.py">CategorizeTextClassifyByUserResponse</a></code>

# AnalyzeTeam

Types:

```python
from millionways.types import AnalyzeTeamCreateResponse
```

Methods:

- <code title="post /analyze-team">client.analyze_team.<a href="./src/millionways/resources/analyze_team.py">create</a>(\*\*<a href="src/millionways/types/analyze_team_create_params.py">params</a>) -> <a href="./src/millionways/types/analyze_team_create_response.py">AnalyzeTeamCreateResponse</a></code>

# CategorizeAudio

Types:

```python
from millionways.types import CategorizeAudioCreateResponse, CategorizeAudioCreateForUserResponse
```

Methods:

- <code title="post /categorize-audio">client.categorize_audio.<a href="./src/millionways/resources/categorize_audio.py">create</a>(\*\*<a href="src/millionways/types/categorize_audio_create_params.py">params</a>) -> <a href="./src/millionways/types/categorize_audio_create_response.py">CategorizeAudioCreateResponse</a></code>
- <code title="post /categorize-audio/{userId}">client.categorize_audio.<a href="./src/millionways/resources/categorize_audio.py">create_for_user</a>(user_id, \*\*<a href="src/millionways/types/categorize_audio_create_for_user_params.py">params</a>) -> <a href="./src/millionways/types/categorize_audio_create_for_user_response.py">CategorizeAudioCreateForUserResponse</a></code>

# Chat

Types:

```python
from millionways.types import ChatGenerateResponseResponse, ChatGenerateResponseForUserResponse
```

Methods:

- <code title="post /chat">client.chat.<a href="./src/millionways/resources/chat.py">generate_response</a>(\*\*<a href="src/millionways/types/chat_generate_response_params.py">params</a>) -> <a href="./src/millionways/types/chat_generate_response_response.py">ChatGenerateResponseResponse</a></code>
- <code title="post /chat/{userId}">client.chat.<a href="./src/millionways/resources/chat.py">generate_response_for_user</a>(user_id, \*\*<a href="src/millionways/types/chat_generate_response_for_user_params.py">params</a>) -> <a href="./src/millionways/types/chat_generate_response_for_user_response.py">ChatGenerateResponseForUserResponse</a></code>

# ChatResult

Types:

```python
from millionways.types import ChatResultGenerateResponse
```

Methods:

- <code title="post /chat-result">client.chat_result.<a href="./src/millionways/resources/chat_result.py">generate</a>(\*\*<a href="src/millionways/types/chat_result_generate_params.py">params</a>) -> <a href="./src/millionways/types/chat_result_generate_response.py">ChatResultGenerateResponse</a></code>

# MentalHealthChatbot

Types:

```python
from millionways.types import MentalHealthChatbotGenerateResponseResponse
```

Methods:

- <code title="post /mental-health-chatbot">client.mental_health_chatbot.<a href="./src/millionways/resources/mental_health_chatbot.py">generate_response</a>(\*\*<a href="src/millionways/types/mental_health_chatbot_generate_response_params.py">params</a>) -> <a href="./src/millionways/types/mental_health_chatbot_generate_response_response.py">MentalHealthChatbotGenerateResponseResponse</a></code>

# ChatStream

Types:

```python
from millionways.types import ChatStreamGenerateResponseResponse
```

Methods:

- <code title="post /chat-stream">client.chat_stream.<a href="./src/millionways/resources/chat_stream.py">generate_response</a>(\*\*<a href="src/millionways/types/chat_stream_generate_response_params.py">params</a>) -> <a href="./src/millionways/types/chat_stream_generate_response_response.py">ChatStreamGenerateResponseResponse</a></code>

# SalesAssistant

Types:

```python
from millionways.types import SalesAssistantGenerateInsightsResponse
```

Methods:

- <code title="post /sales-assistant">client.sales_assistant.<a href="./src/millionways/resources/sales_assistant.py">generate_insights</a>(\*\*<a href="src/millionways/types/sales_assistant_generate_insights_params.py">params</a>) -> <a href="./src/millionways/types/sales_assistant_generate_insights_response.py">SalesAssistantGenerateInsightsResponse</a></code>

# Summarize

Types:

```python
from millionways.types import SummarizeCreateResponse
```

Methods:

- <code title="post /summarize">client.summarize.<a href="./src/millionways/resources/summarize.py">create</a>(\*\*<a href="src/millionways/types/summarize_create_params.py">params</a>) -> <a href="./src/millionways/types/summarize_create_response.py">SummarizeCreateResponse</a></code>

# GetUser

Types:

```python
from millionways.types import GetUserRetrieveResponse, GetUserListResponse
```

Methods:

- <code title="get /get-user/{userId}">client.get_user.<a href="./src/millionways/resources/get_user.py">retrieve</a>(user_id, \*\*<a href="src/millionways/types/get_user_retrieve_params.py">params</a>) -> <a href="./src/millionways/types/get_user_retrieve_response.py">GetUserRetrieveResponse</a></code>
- <code title="get /get-users">client.get_user.<a href="./src/millionways/resources/get_user.py">list</a>(\*\*<a href="src/millionways/types/get_user_list_params.py">params</a>) -> <a href="./src/millionways/types/get_user_list_response.py">GetUserListResponse</a></code>
