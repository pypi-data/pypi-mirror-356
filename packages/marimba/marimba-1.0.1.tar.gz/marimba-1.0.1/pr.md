[Fix] Replace piexif with PyExifTool for robust EXIF handling

## Summary

This pull request addresses critical EXIF corruption issues in processed images by migrating from piexif to PyExifTool for standards-compliant metadata handling. The changes include a new dependency validation system with clear error messaging and various code quality improvements across the metadata processing pipeline.

## Problem

The piexif library was corrupting EXIF headers in processed images, making them unreadable in certain applications like Windows 11 Image Viewer. ExifTool validation revealed overlapping IFDs, odd offsets, out-of-sequence entries, and malformed GPS data that violated EXIF standards. Additional code quality issues included blind exception handling and overly complex methods.

## Solution

Replaced piexif with PyExifTool for robust, standards-compliant EXIF handling using the industry-standard ExifTool binary. Implemented comprehensive dependency validation with platform-specific installation instructions via rich error panels. Refactored EXIF processing to use tag-based operations and improved code quality with specific exception handling and reduced complexity.

## Design

The architecture features upfront dependency validation at the command level to fail fast when external tools are missing. EXIF processing was redesigned around PyExifTool's tag-based API, replacing direct binary manipulation with standards-compliant metadata injection. Thumbnail generation uses temporary files with exiftool embedding instead of in-memory operations. Error handling follows a layered approach with specific exception types and comprehensive logging for debugging.

## Impact

Eliminates EXIF corruption issues, ensuring processed images remain viewable across all applications. Users benefit from clearer error messaging and reduced setup difficulties. Improved code quality makes the codebase more maintainable and scientific workflows more reliable.

## Testing

All existing unit tests pass, with Ruff linting and MyPy type checking completing successfully. Dependency validation tested for both available and missing tool scenarios. EXIF metadata injection validated across various image formats for standards compliance.

## Breaking Changes

Requires ExifTool to be installed on the system and PyExifTool to replace piexif in dependencies. Internal EXIF processing method signatures have changed, potentially affecting custom pipelines that directly interact with iFDO metadata processing.

## Added Files

- `marimba/core/utils/dependencies.py`: Comprehensive dependency validation system with platform-specific error messaging and installation instructions for external tools like exiftool and ffmpeg.

## Modified Files

- `marimba/core/schemas/ifdo.py`: Rewritten EXIF processing to use PyExifTool with tag-based metadata injection and standards-compliant thumbnail generation.
- `marimba/core/utils/summary.py`: Added ffmpeg/ffprobe dependency validation for video analysis.
- `marimba/lib/exif.py`: Migrated to PyExifTool for EXIF data extraction with dependency validation.
- `marimba/lib/gps.py`: Replaced piexif GPS coordinate extraction with PyExifTool implementation.
- `marimba/lib/video.py`: Added PyAV/FFmpeg dependency validation with clear error messaging.
- `marimba/main.py`: Integrated dependency validation into package and process commands.
- `pyproject.toml`: Updated dependencies to replace piexif with PyExifTool.
- `tests/core/utils/test_dataset.py`: Removed unused imports for code cleanliness.

## Additional Notes

This PR addresses #19 and requires ExifTool to be installed on the system where Marimba runs, which is available for all major operating systems through package managers or direct download. The dependency validation system provides clear installation instructions for each platform to guide users through the setup process. Performance may be slightly different due to the change from in-memory binary manipulation to external tool execution, but standards compliance and reliability are significantly improved.

## Notes to Reviewer

Please pay special attention to the new dependency validation system in `marimba/core/utils/dependencies.py` as it introduces a new pattern for handling external tool requirements. Verify that the EXIF processing changes in `marimba/core/schemas/ifdo.py` maintain all existing functionality while improving standards compliance. Test the error messaging with missing dependencies to ensure the installation instructions are clear and platform-appropriate. Consider testing with sample images that previously exhibited EXIF corruption to confirm the fix resolves the original issue.