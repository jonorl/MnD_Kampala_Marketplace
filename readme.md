# Mums & Dads Kampala Marketplace

#### Video Demo: [Insert Video URL Here]

## Introduction
Hello, I'm Jonathan Orlowski, originally from Argentina, but I've lived in London since 2012 and recently moved to Kampala, Uganda with my family. I created this project to address a need within the expat community in Kampala for an efficient way to buy and sell items. Currently, items are shared via PDFs, Word documents, or Google Sheets, which makes searching for specific items cumbersome.

## Project Overview
### Problem Statement
Expats in Kampala frequently buy and sell items through WhatsApp groups. However, the current method of sharing items via attached documents is inefficient and time-consuming.

### Solution
This project provides a web platform where users can register and list items for sale, export listings as PDFs, and share them via WhatsApp. The platform offers a searchable, paginated table of listings, improving the buying and selling process for the community.

## Features
- **User Registration**: Required for listing items.
- **Search Function**: Search items by name, description, contact name, or location.
- **Pagination**: Limits the table to 10 rows per page.
- **Mobile-Friendly**: Redesigned index page for better mobile experience.
- **Item Listing**: Allows users to list multiple items with a single form submission.
- **PDF Export**: Export listings as PDF using pdfmake.
- **Image Handling**: Upload, resize, and create thumbnails for images.
- **Modify Listings**: Users can edit or delete their listings.
- **Share to WhatsApp**: Quick share button for WhatsApp.

## Technical Details
- **Backend**: Flask with SQLAlchemy for database management.
- **Frontend**: HTML, CSS, and JavaScript.
- **Database**: SQLite3
- **Image Processing**: Python Imaging Library (PIL) and uuid for handling and randomizing filenames.
- **JavaScript**: Main.js for all JS functions including PDF export and image hover functionality.

### Key Challenges
1. **Data Standardization**: Initial attempts to parse data from PDFs/Docs were impractical due to inconsistent formats.
2. **Image Handling**: Managing image uploads and displaying full-sized images on hover.
3. **Path Issues**: Resolving Flask's handling of file paths to ensure images load correctly.

## How to Use
1. **Register**: Sign up to list items.
2. **List Items**: Add item details and images, export to PDF if needed.
3. **Search Listings**: Use the search bar to find specific items.
4. **Modify Listings**: Edit or delete your listings as needed.
5. **Share**: Use the WhatsApp share button to share listings.

## Libraries and Tools Used
- Flask
- SQLAlchemy
- PIL (Python Imaging Library)
- pdfmake (AJAX library)
- uuid
- ChatGPT and Claude AI
- CS50.ai debugger
- [favicon.io](https://favicon.io)
- [icons8](https://icons8.com)

## Acknowledgements
I'd like to thank Professor Malan and the staff at Harvard for offering this course for free. The resources provided, including the CS50 Finance exercise, were invaluable in completing this project.
