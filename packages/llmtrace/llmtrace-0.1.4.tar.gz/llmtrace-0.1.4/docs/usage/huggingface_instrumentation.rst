HuggingFace Instrumentation
===========================

To instrument HuggingFace Transformers pipelines, use the `HFInstrumentor`.

.. code-block:: python

   import llmtrace
   from llmtrace.instrumentation.huggingface import HFInstrumentor
   from transformers import pipeline
   import asyncio

   async def main():
       llmtrace.init()
       hf_instrumentor = HFInstrumentor()

       # Create your pipeline and then instrument it
       nlp_pipeline = pipeline("text-generation", model="gpt2")
       hf_instrumentor.instrument_pipeline(nlp_pipeline)

       # Calls to this pipeline will be logged
       # Note: Some HuggingFace pipelines might not be inherently asynchronous.
       # If the pipeline is not awaitable, it will execute synchronously.
       result = nlp_pipeline("Once upon a time, in a faraway kingdom, there was a dragon...")
       print(result[0]['generated_text'])

   if __name__ == "__main__":
       asyncio.run(main())
