OpenAI Instrumentation
======================

To instrument OpenAI API calls, use the `OpenAIInstrumentor`.

.. code-block:: python

   import llmtrace
   from llmtrace.instrumentation.openai import OpenAIInstrumentor
   import openai
   import asyncio

   async def main():
       llmtrace.init()
       OpenAIInstrumentor().instrument()

       # All calls to openai.ChatCompletion.create will be automatically logged
       res = await openai.ChatCompletion.create(
           model="gpt-3.5-turbo",
           messages=[{"role": "user", "content": "Write a short story about a friendly robot."}]
       )
       print(res.choices[0].message.content)

   if __name__ == "__main__":
       asyncio.run(main())
