# properties/services.py
import google.generativeai as genai
from django.conf import settings
from .models import Property, PropertySummary, PropertyReview

class PropertyService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def rewrite_property_info(self, property_obj):
        prompt = f"""
        Please rewrite the following property information in a more engaging way:
        Title: {property_obj.property_title}
        Location: {property_obj.location}
        Room Type: {property_obj.room_type}
        Price: {property_obj.price}
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_summary(self, property_obj):
        prompt = f"""
        Generate a comprehensive summary for the following property:
        Title: {property_obj.property_title}
        Location: {property_obj.location}
        Room Type: {property_obj.room_type}
        Price: {property_obj.price}
        Rating: {property_obj.rating}
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_review(self, property_obj):
        prompt = f"""
        Based on the following property information, generate a detailed review and rating:
        Title: {property_obj.property_title}
        Location: {property_obj.location}
        Room Type: {property_obj.room_type}
        Price: {property_obj.price}
        Current Rating: {property_obj.rating}
        
        Format: 
        Rating: [1-5]
        Review: [detailed review]
        """
        
        response = self.model.generate_content(prompt)
        review_text = response.text
        
        # Parse rating and review from response
        rating_line = review_text.split('\n')[0]
        rating = float(rating_line.split(':')[1].strip())
        review = '\n'.join(review_text.split('\n')[1:]).strip()
        
        return rating, review