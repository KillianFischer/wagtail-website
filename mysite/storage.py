from whitenoise.storage import CompressedManifestStaticFilesStorage
import os

class CustomWhiteNoiseStorage(CompressedManifestStaticFilesStorage):
    def post_process(self, paths, dry_run=False, **options):
        """
        Skip problematic files during post-processing
        """
        skip_patterns = [
            'swiper-bundle.min.js',
            'swiper-bundle.min.css',
            'mysite.js',
            'mysite.css',
            'styles.css'
        ]

        filtered_paths = {
            path: paths[path] 
            for path in paths 
            if not any(pattern in path for pattern in skip_patterns)
        }

        try:
            yield from super().post_process(filtered_paths, dry_run, **options)
        except Exception as e:
            if not dry_run:
                # Copy files that were skipped without processing
                for path in paths:
                    if any(pattern in path for pattern in skip_patterns):
                        original_path = self.path(path)
                        processed_path = self.path(paths[path])
                        
                        if os.path.exists(original_path):
                            os.makedirs(os.path.dirname(processed_path), exist_ok=True)
                            with open(original_path, 'rb') as source:
                                with open(processed_path, 'wb') as dest:
                                    dest.write(source.read())
                            
                            # Generate the URL for the copied file
                            yield path, paths[path], True 