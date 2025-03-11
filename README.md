# Struts 1.x to Spring MVC JSP Conversion Utility

This utility helps in converting **Struts 1.x** JSP files to **Spring MVC** JSP files by replacing Struts-specific tags with their Spring MVC equivalents. It also supports **JSTL** tags and handles common Struts patterns like **form handling**, **logic tags**, **nested properties**, **Tiles templating**, and more.

## Features
- **Comprehensive Tag Conversion**: Converts **HTML**, **Bean**, **Logic**, **Nested**, and **Tiles** tags from Struts to Spring MVC equivalents.
- **Advanced Error Handling**: Logs and tracks unsupported or unhandled tags.
- **Performance Logging**: Measures and logs the time taken for tag replacements.
- **File Input/Output**: Supports reading from and writing to JSP files, making it easy to process large files.
- **Extensive Logging**: Logs every tag replacement, conversion, and potential errors, providing full traceability.
- **Optimized for Large Files**: Handles large JSP files efficiently and performs well even with complex structures.

## Prerequisites
- Python 3.x or higher
- No additional libraries required

## Installation

1. **Clone or Download the Project**:
   Clone the repository or download the files to your local machine.

2. **Install Python**:
   Ensure that **Python 3.x** is installed. You can download Python from [python.org](https://www.python.org/downloads/).

3. **Set up the environment** (optional but recommended):
   It's good practice to create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
