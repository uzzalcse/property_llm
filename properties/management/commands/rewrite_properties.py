from django.core.management.base import BaseCommand
from properties.models import Property, PropertySummary, PropertyReview
from properties.services import PropertyService

class Command(BaseCommand):
    help = 'Rewrites property information using Gemini 2.0 Flash'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting property rewrite process...'))
        try:
            service = PropertyService()
            properties = Property.objects.all()
            
            for prop in properties:
                self.stdout.write(self.style.SUCCESS(f'Processing property {prop.id}...'))
                
                # Rewrite property info
                new_info = service.rewrite_property_info(prop)
                title, description = new_info.split('\n', 1)
                prop.property_title = title
                prop.save()
                
                # Generate and save summary
                summary = service.generate_summary(prop)
                PropertySummary.objects.create(
                    property=prop,
                    summary=summary
                )
                
                # Generate and save review
                rating, review = service.generate_review(prop)
                PropertyReview.objects.create(
                    property=prop,
                    rating=rating,
                    review=review
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully processed property {prop.id}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing properties: {str(e)}')
            )