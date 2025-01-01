import google.generativeai as genai
from django.conf import settings
from .models import Property
import time
from typing import Tuple
import re

class PropertyService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.retry_delay = 60  # Delay in seconds before retrying after rate limit
        self.max_retries = 3
    
    def _make_api_call(self, prompt: str, retries: int = 0) -> str:
        """
        Make an API call with retry logic for rate limiting
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) and retries < self.max_retries:
                time.sleep(self.retry_delay)
                return self._make_api_call(prompt, retries + 1)
            raise e

    def rewrite_property_info(self, property_obj: Property) -> Tuple[str, str]:
        """
        Rewrite property title and description, returning them separately
        """
        prompt = f"""
        Rewrite the following property information in an engaging way.
        Provide the response in exactly this format:
        TITLE: [new title]
        DESCRIPTION: [new description]

        Original Information:
        Title: {property_obj.property_title}
        Location: {property_obj.location}
        Room Type: {property_obj.room_type}
        Price: {property_obj.price}
        """
        
        response = self._make_api_call(prompt)
        
        # Parse the response using regex to handle various formats
        title_match = re.search(r'TITLE:\s*(.*?)(?:\n|$)', response, re.IGNORECASE)
        desc_match = re.search(r'DESCRIPTION:\s*(.*?)(?:\n|$)', response, re.IGNORECASE | re.DOTALL)
        
        title = title_match.group(1).strip() if title_match else property_obj.property_title
        description = desc_match.group(1).strip() if desc_match else ""
        
        return title, description

    def generate_summary(self, property_obj: Property) -> str:
        """
        Generate a comprehensive summary for the property
        """
        prompt = f"""
        Generate a comprehensive summary (2-3 paragraphs) for this property:
        Title: {property_obj.property_title}
        Location: {property_obj.location}
        Room Type: {property_obj.room_type}
        Price: {property_obj.price}
        Rating: {property_obj.rating}

        Format your response as a continuous paragraph without any prefixes or labels.
        """
        
        return self._make_api_call(prompt)

    def generate_review(self, property_obj: Property) -> Tuple[float, str]:
        """
        Generate a rating and review for the property
        """
        prompt = f"""
        Generate a detailed review and rating for this property:
        Title: {property_obj.property_title}
        Location: {property_obj.location}
        Room Type: {property_obj.room_type}
        Price: {property_obj.price}
        
        Provide your response in exactly this format:
        RATING: [single number between 1-5]
        REVIEW: [your detailed review]
        """
        
        response = self._make_api_call(prompt)
        
        # Parse rating and review using regex
        rating_match = re.search(r'RATING:\s*([\d.]+)', response, re.IGNORECASE)
        review_match = re.search(r'REVIEW:\s*(.*)', response, re.IGNORECASE | re.DOTALL)
        
        if not rating_match or not review_match:
            raise ValueError("Could not parse rating or review from response")
            
        rating = float(rating_match.group(1))
        if rating < 1 or rating > 5:
            rating = max(1, min(5, rating))  # Clamp between 1 and 5
            
        review = review_match.group(1).strip()
        
        return rating, review
