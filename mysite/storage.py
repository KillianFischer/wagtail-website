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
            'styles.css',
            '.map'
        ]

        filtered_paths = {}
        for path, hashed_path in paths.items():
            if any(pattern in path for pattern in skip_patterns):
                # Directly yield skipped files without processing
                if not dry_run:
                    original_path = self.path(path)
                    processed_path = self.path(hashed_path)
                    
                    if os.path.exists(original_path):
                        os.makedirs(os.path.dirname(processed_path), exist_ok=True)
                        with open(original_path, 'rb') as source:
                            with open(processed_path, 'wb') as dest:
                                dest.write(source.read())
                yield path, hashed_path, True
            else:
                filtered_paths[path] = hashed_path

        # Process remaining files
        if filtered_paths:
            yield from super().post_process(filtered_paths, dry_run, **options) 