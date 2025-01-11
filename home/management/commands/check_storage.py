from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Check if DigitalOcean Spaces storage is configured correctly'

    def handle(self, *args, **options):
        try:
            # Try to write a test file
            test_file_name = 'storage_test.txt'
            default_storage.save(test_file_name, ContentFile('test content'))
            
            # Try to read the file
            if default_storage.exists(test_file_name):
                self.stdout.write(self.style.SUCCESS('Successfully wrote and read from storage'))
                # Clean up
                default_storage.delete(test_file_name)
            else:
                self.stdout.write(self.style.ERROR('File was not found after saving'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Storage test failed: {str(e)}'))