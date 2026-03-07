def llm_response_stream():
    yield {"content": "今天", "stop": False}
    yield {"content": "天气", "stop": False}
    yield {"content": "不错", "stop": True}
    yield {"content": "（这条不该被看到）", "stop": False}


llm = llm_response_stream()

for response in llm:
    print("LLM response:", response["content"])
    if response["stop"]:
        print("LLM response ended.")
        break
