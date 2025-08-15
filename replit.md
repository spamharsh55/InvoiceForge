# PDF Form Generator

## Overview

A Flask web application that generates filled PDF documents by overlaying user-provided form data onto existing PDF templates. The application uses a simple web form to collect data fields and produces a downloadable PDF with the information positioned at specific coordinates on the template.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Simple HTML Forms**: Uses Flask's `render_template_string` to serve a basic HTML form with inline CSS styling
- **Form-based Input**: Collects multiple data fields including personal information, addresses, and various charges/fees
- **Direct Form Submission**: Posts form data directly to the Flask backend without client-side JavaScript

### Backend Architecture
- **Flask Web Framework**: Lightweight Python web server handling form rendering and PDF generation
- **PDF Processing Pipeline**: 
  - Accepts form data via POST requests
  - Creates PDF overlays using ReportLab for text positioning
  - Merges overlays with existing PDF templates using PyPDF2
  - Returns generated PDFs as downloadable files

### PDF Generation System
- **Template-based Approach**: Uses existing PDF templates as base documents
- **Coordinate-based Positioning**: Places form data at specific X,Y coordinates on the PDF
- **Two-step Process**: 
  1. Creates an overlay PDF with form data positioned correctly
  2. Merges the overlay with the original template

### Data Storage
- **No Persistent Storage**: Application processes data in-memory only
- **Temporary File Handling**: Uses BytesIO streams for PDF manipulation without disk storage
- **Stateless Design**: Each request is independent with no session management

## External Dependencies

### Python Libraries
- **Flask**: Web framework for handling HTTP requests and responses
- **ReportLab**: PDF generation library for creating text overlays and coordinate grids
- **PyPDF2**: PDF manipulation library for reading templates and merging documents

### Development Tools
- **Coordinate Grid Generator**: Helper functionality to determine precise text positioning on PDF templates
- **PDF Size Detection**: Utilities to read template dimensions for proper overlay sizing

### File Dependencies
- **PDF Templates**: Requires existing PDF files to serve as form templates
- **Font Resources**: Uses standard Helvetica fonts for text rendering