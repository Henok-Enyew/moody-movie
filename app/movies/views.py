from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def get_movie_recommendations(mood):
    try:
        # prompt = f"I am feeling {mood}. Please recommend movies that match this mood. Just give me the movie names as array, no extra information or introduction needed just only the movie names and short description as array of objects. "
        prompt = f"Provide a list of movie recommendations based on the mood '{mood}', including only the movie names and a short description of each. No categories, no extra commentary—just the names and descriptions in a simple, clean format. , dont include * in your response i want a response just like json format example - {{name: titanic, discrption:movide discription}}' thats it no other introduction or ending needed act as api request to be formal"
    
        response = client.models.generate_content(
            model="gemini-2.0-flash",  
            contents=f"Recommend movies for a {mood} mood"
        )

        if response.text:
            return {"movies": response.text.split('\n')}  
        else:
            return {"error": "No recommendations found"}

    except Exception as e:
        return {"error": f"Failed to fetch recommendations: {str(e)}"}



@api_view(["POST"])
def recommend_movies(request):
    mood = request.data.get("mood", "")
    if mood:
        movie_recommendations = get_movie_recommendations(mood)
        return Response(movie_recommendations)
    else:
        return Response({"error": "Mood is required"}, status=400)
