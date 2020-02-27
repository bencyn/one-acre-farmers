# One Acre Fund Seasonless Repayments

The postman interface allows the user to post repayment data then receives a json output of computed repayments and a customer summary of the updated credit records

## Post-mortem

##### Current project status

- a user can view create update or delete customers, seasons, customer summaries, and repayments
- user can also list , post repayment uploads and generate repayment records depending on status of the repayment record (Cascade, Override, overpaid)

##### Estimate on the outstanding work

- a maximum of one week to cover all the edge cases.
##### Successes/what went well

- I managed to implement overpaid and override case scenarios when a user uploads repayments for a specific season and or payment with no autostanding previous credits. This also reflects on the final customer summary

##### Bumps/what you wished went better

- meet the minimum expectations by fully implementing all the projects deliverables

##### How you would improve your approach in future projects

- priotize tasks by focusing on the less challeging to more challeging ones.This would reduce the time spent to resolve a blocker

##### Improvements/enhancements to this project for future consideration

- add unit tests and integrate travis circle CI so as to keep track of the test coverage
- refactore code and integerate tools like code climate to help enhance code readability and maintainability
- add more validations
- host the api application to a production server prefarrably apache, nginix or heroku
- implement authenitication by use of auth2 jwt_tokens
- create a user interface that consume the api endpoints
