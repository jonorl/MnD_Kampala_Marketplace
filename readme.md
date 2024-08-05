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

## Original description for CS50

The lines written above were suggested by ChatGPT as to write a professionally well written readme.me file. The below is what I've written originally which I'm going to keep since CS50 requires a minimum of 750 words.

Hello, I'm Jonathan Orlowski, originally from Argentina, but I've lived in London since 2012 and I've now moved
recently to Kampala, Uganda along with my family (I'm 38 btw). Here I've joined the expat diaspora which has it's
own WhatsApp group, namely one for mums & dads in Kampala. In this group people are coming and leaving as most
expats only stay for a few years and then go back to their countries of origin. People who leave post items they
want to sell, and people arriving obviously want to buy them. The only problem is that people share their stuff
by attaching PDFs or Word documents or sharing Google Sheets or the likes, so if I want to find something
specific, I need to go one by one searching through every file, which is quite annoying. Hence this project.

Originally, I tried to see if I could capture and parse the data from these PDFs/Docs/etc and put them in a
database, however, everyone tends to put different bits of information, different columns with different names
making the standardisation near impossible. So I thought I would take this from a different approach. Have users
register their items before sharing, and at the same time giving them a tool to export as a PDF and a "share to
WhatsApp" button.

The site is open for everyone to see the listing, no registration required to see, but it is necessary to register
to list an item. The items are displayed on a table with the rows being generated from the database via SQLAlchemy
as I tried to not use CS50 library.

There is a search function at the top that will scan for keywords and returning rows if anything is found under
the name, description, contact name or location. I've added pagination to limit the table to 10 rows per page.
This index page had to be redesigned for mobile users as seeing tables on a phone or tablet looks quite awful.

To list an item, users must be registered and then click on the "List new items" link at the top of the page.
The first few text fields: contact name, phone number, email, location are stored on a separate table called
contacts on the database as these tend to be the same irrespective of the number of items. Then users can list
their stuff, adding a name, description (which can be long), price, currency (there's a selector between UGX and
USD), the availability and the option to add an image. Once that's done, they can add another item by pressing the
"add another item" button which has a javascript function to add new html lines so that users can add more than
one item at the time. Before they can list it so that it appears on the index site, there's the option to export
as PDF, which is another button linking to a javascript function using a pdfmake function from the ajax library.
One of the main challenges here was that the images weren't yet added to the server until the List item button
was pressed as this would trigger the POST method, so finding the workaround took a lot of time.

There's also a python function to reduce the size of the image and to create a thumbnail. Both are stored on a
folder called uploads within the static folder. There's also a limit to 10MB, but the image stored will be
1600x1200 and the thumbnail 200x200. There's a javascript function that shows the full size image when hovering
over the template. There's validation for valid file extensions: png, jpg, gif. Another issue that took me forever
to fix was around the paths. For whatever reason Flask didn't like the full path like '/workspaces/39122230/'
so the images wouldn't load and Flask would return a 404 even though the link would work perfectly well. I had
to add an if statement to remove that if found and then re-add it when creating the rule that would delete
images from the database. I also wanted to make sure that this would be skipped if that prefix path wouldn't be
found so that I can re-purpose this one to go into live production someday. I've used the PIL library to handle
the images as well as uuid to randomise the filenames.

Once the item(s) have been listed, they should be available for everyone to see. But what if there's an error
and the user needs to amend, correct something, or maybe the item was sold but they want to leave it on the
database for people to check how much things are worth or maybe they just want to completely remove that item.
Users can go to "Modify a Listing" which will show the items created by that specific user and all the same
attributes can be modified or removed. Once that's done, they can hit the "Save Changes" button at the bottom
which will prompt a confirmation once pressed (this is javascript as opposed to a flash message).

I've placed all the JS code on main.js and used a single styling sheet on styles.css - I wanted to separate these
two from the HTML code. All the HTML has passed the tests on the validator.

There are "change password" and "logout" functions that are very similar to the same exercise from finance and
lastly a "share to WhatsApp" button on the top right hand side corner. I've re-used the apology cat from
the finance exercise, I really hope that's allowed.

For this project I've used a combination of ChatGPT and Claude AI as well as the CS50.ai debugger. I've use the favicon generator from https://favicon.io/favicon-generator/ and the WhatsApp icon from https://icons8.com

Lastly, I'd like to thank professor Malan and all the staff at Harvard that made this course possible for free.
