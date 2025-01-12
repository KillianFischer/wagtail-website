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
            '.map'  # Add this to skip source map files
        ]

        filtered_paths = {
            path: paths[path] 
            for path in paths 
            if not any(pattern in path for pattern in skip_patterns)
        }

        for path in paths:
            if any(pattern in path for pattern in skip_patterns):
                yield path, None, False  # Skip processing these files entirely

        yield from super().post_process(filtered_paths, dry_run, **options) 