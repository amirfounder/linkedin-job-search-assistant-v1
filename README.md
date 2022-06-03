# Process

### High Level (Part 1 - Extract Info)

1. Confirm Login
2. For each query template:
   1. Navigate to specific page
   2. Content script sends HTML to HTTP server
3. Extract Recruiters from each HTML page
4. For each recruiter:
   1. Create open invite message template

***This entire process will include checkpoints saved in some DB***

### High Level (Part 2 - User Actions)

1. Start the program
2. Program spits out options
   1. Run extract_info ETL (should be run 1 / month)
   2. Do outreach
      1. default strategy = 2 recruiters from same company / 3 days
   3. Do followups

### Open LinkedIn and login

Be sure this part is taken care of before running the script.
Errors will be thrown otherwise.

### Identify search bar

1. `Local computer -> Browser (search URL)`
2. `Content Script (Run highlight)`
3. `Content Script -> HTTP Server (request screenshot - includes RED)`
4. `Content Script -> HTTP Server (request screenshot - original)`

### Run a search query



1. `Local`
2. `Content Script -> HTTP Server (initial page open)`
3. `Content Script -> HTTP Server (page after it has loaded / 5 sec. timeout)`
4. 