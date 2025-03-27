# Step to reproduce
1. `pip install -r requirements.txt`
2. Modify `env` to `.env` with required values.
3. `python chain.py`

# Fixed bugs.
1. ```python
    actor_prompt_template = ChatPromptTemplate.from_template(
        """system: You are expert researcher.
           Current time: {time}
    
           1. {first_instruction}
           2. Reflect and critique your answer. Be severe to maximize improvement.
           3. Recommend search queries to research information and improve your answer.
           {messages}
           system: Answer the user's question above using the required format."""
    ).partial(
        time=lambda: datetime.datetime.now().isoformat()
    )

```

# As is
```bash
/Users/sarit/.pyenv/versions/reflexion-agent/bin/python -X pycache_prefix=/Users/sarit/Library/Caches/JetBrains/PyCharm2024.3/cpython-cache /Users/sarit/Applications/PyCharm Professional Edition.app/Contents/plugins/python-ce/helpers/pydev/pydevd.py --multiprocess --qt-support=auto --client 127.0.0.1 --port 61114 --file /Users/sarit/study/EdenMarcoLangGraph/reflexion-agent/chain.py 
Connected to pydev debugger (build 243.26053.29)
system: You are expert researcher.
       Current time: {time}

       1. {first_instruction}
       2. Reflect and critique your answer. Be severe to maximize improvement.
       3. Recommend search queries to research information and improve your answer.
       {messages}
       system: Answer the user's question above using the required format.
system: You are expert researcher.
       Current time: {time}

       1. {first_instruction}
       2. Reflect and critique your answer. Be severe to maximize improvement.
       3. Recommend search queries to research information and improve your answer.
       {messages}
       system: Answer the user's question above using the required format.
system: You are expert researcher.
       Current time: {time}

       1. {first_instruction}
       2. Reflect and critique your answer. Be severe to maximize improvement.
       3. Recommend search queries to research information and improve your answer.
       {messages}
       system: Answer the user's question above using the required format.



Traceback (most recent call last):
  File "/Users/sarit/Applications/PyCharm Professional Edition.app/Contents/plugins/python-ce/helpers/pydev/pydevd.py", line 1570, in _exec
    pydev_imports.execfile(file, globals, locals)  # execute the script
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sarit/Applications/PyCharm Professional Edition.app/Contents/plugins/python-ce/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "/Users/sarit/study/EdenMarcoLangGraph/reflexion-agent/chain.py", line 47, in <module>
    res = chain.invoke(input={"messages": [human_message]})
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sarit/.pyenv/versions/reflexion-agent/lib/python3.12/site-packages/langchain_core/runnables/base.py", line 3025, in invoke
    input = context.run(step.invoke, input, config)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sarit/.pyenv/versions/reflexion-agent/lib/python3.12/site-packages/langchain_core/output_parsers/base.py", line 193, in invoke
    return self._call_with_config(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sarit/.pyenv/versions/reflexion-agent/lib/python3.12/site-packages/langchain_core/runnables/base.py", line 1925, in _call_with_config
    context.run(
  File "/Users/sarit/.pyenv/versions/reflexion-agent/lib/python3.12/site-packages/langchain_core/runnables/config.py", line 430, in call_func_with_variable_args
    return func(input, **kwargs)  # type: ignore[call-arg]
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sarit/.pyenv/versions/reflexion-agent/lib/python3.12/site-packages/langchain_core/output_parsers/base.py", line 194, in <lambda>
    lambda inner_input: self.parse_result(
                        ^^^^^^^^^^^^^^^^^^
  File "/Users/sarit/.pyenv/versions/reflexion-agent/lib/python3.12/site-packages/langchain_core/output_parsers/openai_tools.py", line 294, in parse_result
    pydantic_objects.append(name_dict[res["type"]](**res["args"]))
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sarit/.pyenv/versions/reflexion-agent/lib/python3.12/site-packages/pydantic/main.py", line 214, in __init__
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core._pydantic_core.ValidationError: 1 validation error for AnswerQuestion
search_queries
  Field required [type=missing, input_value={'answer': 'AI-powered Se...ed SOC startups 2025']}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
python-BaseException

Process finished with exit code 1
```
To solve this problem. Just reorder the `AnswerQuestion`
Putting `Reflection` to the last.
```python
class AnswerQuestion(BaseModel):
    """Answer the question."""
    answer: str = Field(description="~250 word details answer to the question.")
    search_queries: List[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )
    reflection: Reflection = Field(description="Your reflection on the initial answer.")
```
