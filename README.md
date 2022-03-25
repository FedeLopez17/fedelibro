# FEDELIBRO
## Video Demo:  <URL HERE>

## Description:

Fedelibro is a library classification web application that allows users to store books methodically, within a database, in order to minimize search times. 
In contrast to most other library classification systems, Fedelibro is designed mainly for home usage, rather than libraries.
It works by giving each added book a unique numerical id, which is later used to find the book/s the user is looking for.




## How it works:
With Fedelibro not only can you add books, and look for them, but you can also sort the index table in different ways, delete previously added books, change your password, change the language of the page, and so on. Nevertheless, to avoid redundancy, only the two main functions of the web app (add and search) will be thoroughly explained. 
If you want to know everything you can do using this web application, and how to do it, you should check the "About" page.

To add a book, you need to go to the "Add" page by using the link in the navigation bar at the top of the page and then fill out a form describing the book you want to add.
Despite there being ten fields to fill, not all are required, in fact only the title and the main subject are needed to add a book (This is in case the user doesn't know who the author is, the year of publishment, etc). However, the user should always fill as many as they know, in order to make added books more distinguishable.
After the user fills the form and submits it via the submit button at the end of the form, the user is redirected to the index page, and an alert notifies him of the ID of the book. The user should then label said book with this ID, using a tag somehow attached to the book's spine, a piece of paper stuck to the piece of furniture or some other way the user sees fit. 
I'm fully aware this is not an optimal solution, as probably most people wouldn't want to stick a tag to their books or furniture. Nevertheless, in the absence of a better solution (hopefully temporarily), I personally think adding a tag to my books, or furniture, wouldn't be such a big deal. Of course, this is just my opinion. It's up to users to decide if this works for them. If it does not, they could either develop some kind of workaround or sadly quit using this app. 
Once again, I'm aware this is potentially one of the main drawbacks of Fedelibro. 
After labeling the book, the book needs to be stored, sorted by its ID in a numerically increasing manner from left to right. For instance, if my first added book's ID is 1, and I stored it in a bookshelf, my second added book whose ID will be 2, will be stored to the right of the first book.
Moreover, as another example, let's say I have added my first ten books, and have them sorted in a numerically increasing manner regarding their IDs (1-10). Later, I delete one of these previously added books whose ID was 5. Now I have only nine books within my database. Then, I want to add another book, so I fill the form and click the submit button, and, consequently, I am redirected to the Index page and shown the book's ID, which is 11. After that, I stick a tag to the book's spine and try to store it in my bookshelf with the other nine books. However, I'm suddenly faced with a conundrum, there's an empty space where the earlier deleted book (whose ID was 5) used to be, and there's also space to the right of the ninth book. Where should I store my book? Well, remember you should ALWAYS store the book you're trying to add next to the previously added book. So all I would have to do would be to squeeze the nine books together, removing the space where the fifth book used to be, and then store the current book to the right of the ninth book.
There's obviously no need to have all your books in the same piece of furniture. You could, for example, have books 1 to 50 (ID wise) in one bookshelf while keeping books 51-100 in another bookshelf.

Searching for a book is a very straightforward procedure. First users need to go to the "Search" page by using the Navbar at the top, and then fill out the same form filled when adding a book. The only difference this time is that this form will be used to scan through the database and find a match. In the case that a match is found, the user will be then redirected to a page containing a table detailing the found book (or books) as well as its ID, with which users can go to their bookshelf and look for the book's spine with that ID in its tag. On the other hand, if no book is found, Fedelibro will "lower its standards" and search again but only for books with matching title and main topic or subtopics. If it finds at least one, the user will be redirected and shown the previously mentioned table containing information about the book (or books) found, and its ID.
If Fedelibro doesn't find any book this time either, it will look for books with the same or similar title as that of the form. If it finds any, the user will be redirected to the said table page. In the case that still no book is found, it means that the book does not exist within the database (it was never added), or that you made a mistake in the search (e.g. misspellings).




## Future potential improvements and things that could have been done better:

In regards to features that could be useful for users (at least for some) to have but aren't included (at least not yet) in Fedelibro, the two main ones would be:
- Ability to link account to email, which would give users another way of resetting their forgotten passwords.
- Ability to print a ticket with books' IDs, which would then be used to identify books.

Furthermore, when it comes to things that could have been done better, the truth is that arguably everything could have been done much better, not only because of the omnipresent and widely known "room for improvement", but also because of the fact that I'm just barely getting my feet wet in this software development, more specifically web development, world.
Therefore, even though I'm really proud of the outcome of this project, I am aware that in this industry there's always the need for growth.
If I had to put my finger on some of those things that could have been done better, the styling of templates using (CSS) could definitely be improved. Styling was definitely one of the things I struggled the most with. Besides, I'm sure that some of the logic written in python, in the app.py file, could be improved as well. 
 



## Advantages over The Dewey Decimal System:

According to Wikipedia, the free encyclopedia ( https://en.wikipedia.org/wiki/Dewey_Decimal_Classification )
>The Dewey Decimal Classification (DDC), colloquially known as Dewey Decimal System, is a proprietary library classification system which allows new books to be added to a library in their appropriate location based on subject. It was first published in the United States by Melvil Dewey in 1876. Originally described in a forty-four-page pamphlet, it has been expanded to multiple volumes and revised through 23 major editions, the latest printed in 2011. It is also available in an abridged version suitable for smaller libraries. OCLC, a non-profit cooperative that serves libraries, currently maintains the system and licenses online access to WebDewey, a continuously updated version for catalogers.

>The Decimal Classification introduced the concepts of relative location and relative index. Libraries previously had given books permanent shelf locations that were related to the order of acquisition rather than topic. The classification's notation makes use of three-digit numbers for main classes, with fractional decimals allowing expansion for further detail. Numbers are flexible to the degree that they can be expanded in linear fashion to cover special aspects of general subjects. A library assigns a classification number that unambiguously locates a particular volume in a position relative to other books in the library, on the basis of its subject. The number makes it possible to find any book and to return it to its proper place on the library shelves. The classification system is used in 200,000 libraries in at least 135 countries.

>The Dewey Decimal Classification organizes library materials by discipline or field of study. Main divisions include philosophy, social sciences, science, technology, and history. The scheme comprises ten classes, each divided into ten divisions, each having ten sections. The system's notation uses Indo-Arabic numbers, with three whole numbers making up the main classes and sub-classes and decimals designating further divisions. The classification structure is hierarchical and the notation follows the same hierarchy. Libraries not needing the full level of detail of the classification can trim right-most decimal digits from the class number to obtain more general classifications. For example:

>500 Natural sciences and mathematics
    510 Mathematics
        516 Geometry
            516.3 Analytic geometries
                516.37 Metric differential geometries
                    516.375 Finsler geometry

>The classification was originally enumerative, meaning that it listed all of the classes explicitly in the schedules. Over time it added some aspects of a faceted classification scheme, allowing classifiers to construct a number by combining a class number for a topic with an entry from a separate table. Tables cover commonly used elements such as geographical and temporal aspects, language, and bibliographic forms. For example, a class number could be constructed using 330 for economics + .9 for geographic treatment + .04 for Europe to create the class 330.94 European economy. Or one could combine the class 973 (for the United States) + .05 (for periodical publications on the topic) to arrive at the number 973.05 for periodicals concerning the United States generally. The classification also makes use of mnemonics in some areas, such that the number 5 represents the country Italy in classification numbers like 945 (history of Italy), 450 (Italian language), 195 (Italian philosophy). The combination of faceting and mnemonics makes the classification synthetic in nature, with meaning built into parts of the classification number.


To summarize, When using the Dewey Decimal System, you assign a space for each subject, which is within a numerical range, and then you add decimal numbers to add further sub-categories.
This is an amazing system for libraries with hundreds of thousands of books, but it's not really fit for home usage, due to the limited storage room for books in normal houses.
The main problem Fedelibro would have if it were to use this system, is that users would have to either leave space to eventually add books within the same subject or, if they are unable to leave space due to not having enough room, they would have to rearrange all the books again every time they need to enter a new book into the system. 
With a system such as Fedelibro's, users can store every book back to back, regardless of subject, without having to leave space or rearrange books, and then, in the web app, they can filter through their books by subject, author, similar title, colour, whether it is hardcover or paper, ID number, cover-colour, etc and get the ID of every single one of their books. In short, the advantage Fedelibro has over The Dewey Decimal System for home usage, is the fact that it allows users to use their storage space as efficiently as possible, due to the ability to find any book almost instantaneously by using the web app.




## Technicalities:

Fedelibro was created using Python3, Javascript, SQL, HTML, CSS, Bootstrap, Jinja, Flask, PostgreSQL, SQLite3, and deployed to Heroku from Github.
Regarding directories, inside the "static" directory are all the stylesheets used to make Fedelibro look prettier, as well as the custom-made favicon.
Inside the templates directory, there are 26 templates, some of which are repeated templates translated to Portuguese and Spanish. This is because I didn't like the translation done automatically by Google, so I went ahead and disabled it, and translated each page (except for the login, register, and reset pages that do have google translation enabled) manually.
Within these templates, there are also some called layouts, which other templates expand upon in order to avoid having to type too much boilerplate code.
Besides those two directories, there are also some other files, including helpers.py (really useful functions), and the App.py file, which in some way acts as the puppeteer of the whole website. I don't think there's a need to explain it as it has pretty self-explanatory function and variable names as well as some comments explaining the logic.


Thank you for reading and especially thank you to everyone who makes CS50 possible. I am eternally grateful for the tools you have provided me with. 
Thanks to CS50 I have found a passion I will happily cultivate for the rest of my life!

# ** :D **


