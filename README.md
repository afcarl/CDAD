# CDAD
Closed Domain Acronym Disambiguation tool

The ideas in this project are inspired by an academic paper titled: Artificial Intelligence or Asset Intelligence? Acronym Disambiguation for Enterprises by Yang Li, et. al, the paper has been submitted to the 2015 World Wide Web Conference and is currently under peer review.  

Instructions:
This project contains two parts: a backend portion written in Python, and a frontend viewer written in Swift.  To run the Python backend portion you will need python installed (the project was tested with version 2.7).  Additionally you will need one Python library called python-Levenshtein.  Once you have those installed you can go to the code directory and type: 
./acronym.py
This will extract acronyms and acronym meanings from the corpus contained in the docs folder.  The extracted acronyms, their meanings, and popularity scores are stored in a file called final.json, which can be passed to other applications.
The code repo contains a small corpus, should you want to add to this corpus, you can crawl and extract text with by typing:
./doc_crawler.py my_string
Where my_string is a string you want to search, for example: if you wanted to crawl and store documents containing the acronym CRM you would type:
./doc_crawler CRM.

