import google.generativeai as genai
from config import Settings

settings = Settings()
class LLMService:

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_response(self,query:str,search_results:list[dict]):
        # print("yaha tak chla")
        context_text = "\n\n".join(
            [
                f"Source {i+1} ({result['url']}) :\n {result['content']}"
                for i,result in enumerate(search_results)
            ]
        )
        # print (context_text)

        full_prompt = f"""

         context from web search:
         {context_text}
         Query:
         {query}
         Please provide a comprehensive, detailed, well-cited, accurate response using the context data.kindly refrain from using your own knowledge unless its necessary
        """
        # print(full_prompt)

        response = self.model.generate_content(full_prompt,stream= True)

        for chunk in response:
            yield chunk.text

        