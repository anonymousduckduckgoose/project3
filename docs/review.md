# Project 3 Review

### Overview
This repo defines an minimum viable product (MVP) version of the Favicon Fetcher API Service which exposes an HTTP-based API designed to provide a simple and efficient solution for users to request a favicon from any website. All downloadable items from this doc are stored in this anonymous Github user account.

I chose to complete this project in python for the following reasons:

- Python has many simple-to-use libraries that make it easy to parse HTML for web scraping services. 
- Python has many versatile and well-documented API frameworks.
- It is the language I am most familiar with and therefore could quickly build-out within the recommended time-frame.

### Quick Review
On my original submission of this project, I opted to focus on the Infrastructure Code that paired with the service I submitted as I thought it would be most relevant for the role I was applying to. I opted not to remove that code from the repo, however, with the feedback provided, i significantly improved and focused on the API service directly. 
Since my original submission I opted to instrument monitoring through prometheus and grafana, handle requests through async for improved performance and scalability, added a couple of simple test cases, and handled the entire service through Docker instead of directly through the daemon. These changes provided significant reliability improvements and what I felt to be a production-ready framework that could be continued to build upon.
The biggest items I see for improvement (ultimately the trade-offs I made here) are the processing time for each GET /favicon/{protocol:url} request and more robust error handling based on more thorough testing. 
Overall, i think the improvements are one big step closer to production-quality from my original submission and I really appreciate the opportunity to review and update the service based on the feedback and clarified requirements of the project! 

Cheers,
Keri