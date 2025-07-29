LangChain Instrumentation
=========================

To instrument LangChain applications, use the `LangChainCallbackHandler`.

.. code-block:: python

   import llmtrace
   from llmtrace.instrumentation.langchain import LangChainCallbackHandler
   from langchain_openai import ChatOpenAI # Or any other LangChain LLM
   from langchain.prompts import ChatPromptTemplate
   from langchain.chains import LLMChain # Or any other type of chain
   import asyncio

   async def main():
       llmtrace.init()
       handler = llmtrace.LangChainCallbackHandler() # Instantiate the handler

       # Pass the handler to your LLM or Chain
       llm = ChatOpenAI(model_name="gpt-4o", callbacks=[handler])
       prompt = ChatPromptTemplate.from_messages([
           ("system", "You are a helpful assistant."),
           ("user", "{input}")
       ])
       chain = LLMChain(llm=llm, prompt=prompt)

       response = await chain.ainvoke({"input": "What is the capital of Spain?"}) # Use .ainvoke for async calls
       print(response)

   if __name__ == "__main__":
       asyncio.run(main())
