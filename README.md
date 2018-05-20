# LiveVolumeParser
Scripts and snippets to assist with parsing a live volume. First created for testing multiprocessing library.

## Summary
LiveVolumeParser was first created for testing and understanding multiprocessing library better. 

Parsing of 63765 files using a single core took 1200 seconds.
Parsing of the same using 4 cores took 14 seconds.

Intention is to build this into scalable solution for parsing a live volume for YARA rules, grep matches on file paths for APT IOCs and other IR/TH based functions for finding bad stuff.
