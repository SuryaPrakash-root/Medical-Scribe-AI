import os
import asyncio
from dotenv import load_dotenv
from services import ScribeService

load_dotenv()

async def test():
    try:
        service = ScribeService()
        transcript = """
Doctor: Good morning, Mr. Kumar. How have you been feeling since your last visit?

Patient: Good morning, doctor. Not very well. I’ve been feeling very tired lately, especially in the afternoons. My blood sugar readings have also been higher than usual.

Doctor: What range are your sugar levels in?

Patient: Mostly between 190 and 230, even when I don’t eat much.
        """
        print("Testing transcript processing...")
        result = service.process_transcript(transcript)
        print("Result:", result)
    except Exception as e:
        print("Error occurred:")
        print(e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
