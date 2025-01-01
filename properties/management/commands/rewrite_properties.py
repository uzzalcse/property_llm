# properties/management/commands/rewrite_properties.py
from django.core.management.base import BaseCommand
from django.db import transaction
from properties.models import Property, PropertySummary, PropertyReview
from properties.services import PropertyService
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Rewrites property information using Gemini AI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=10,
            help='Number of properties to process in each batch'
        )
        parser.add_argument(
            '--start-from',
            type=int,
            default=0,
            help='Property ID to start processing from'
        )

    def process_property(self, prop: Property, service: PropertyService) -> Optional[str]:
        """Process a single property with error handling"""
        try:
            with transaction.atomic():
                # Rewrite property info
                new_title, new_description = service.rewrite_property_info(prop)
                prop.property_title = new_title
                prop.save()

                # Generate and save summary
                summary = service.generate_summary(prop)
                PropertySummary.objects.create(
                    id=prop.id,  # Set the ID explicitly to match the Property ID
                    property=prop,
                    summary=summary
                )

                # Generate and save review
                rating, review = service.generate_review(prop)
                PropertyReview.objects.create(
                    id=prop.id,  # Set the ID explicitly to match the Property ID
                    property=prop,
                    rating=rating,
                    review=review
                )

            return None  # No error

        except Exception as e:
            error_msg = f"Error processing property {prop.id}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        start_from = options['start_from']

        self.stdout.write(self.style.SUCCESS(
            f'Starting property rewrite process from ID {start_from} with batch size {batch_size}...'
        ))

        service = PropertyService()
        properties = Property.objects.filter(id__gte=start_from).order_by('id')
        total_count = properties.count()
        processed = 0
        errors = []

        for prop in properties.iterator():
            error = self.process_property(prop, service)
            if error:
                errors.append(error)
            else:
                processed += 1

            # Progress update
            self.stdout.write(
                self.style.SUCCESS(
                    f'Processed {processed}/{total_count} properties. '
                    f'Errors: {len(errors)}'
                )
            )

        # Final summary
        self.stdout.write(self.style.SUCCESS(
            f'\nProcess completed!\n'
            f'Successfully processed: {processed}\n'
            f'Errors: {len(errors)}\n'
        ))

        if errors:
            self.stdout.write(self.style.WARNING('Errors encountered:'))
            for error in errors:
                self.stdout.write(self.style.ERROR(error))
