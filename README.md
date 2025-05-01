# qshahid-swe645-asst4

## Example POST requests for /api/surveys

### Example 1
```
POST /api/surveys
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Doe",
  "streetAddress": "123 Main St",
  "city": "Fairfax",
  "state": "VA",
  "zipcode": "22030",
  "telephone": "123-456-7890",
  "email": "john.doe@example.com",
  "dateOfSurvey": "2025-04-13",
  "likedMost": "students",
  "interestSource": "internet",
  "recommendLikelihood": "very likely",
  "additionalComments": "Great experience!"
}
```

### Example 2
```
POST /api/surveys
Content-Type: application/json

{
  "firstName": "Alice",
  "lastName": "Smith",
  "streetAddress": "456 College Ave",
  "city": "Arlington",
  "state": "VA",
  "zipcode": "22201",
  "telephone": "987-654-3210",
  "email": "alice.smith@example.com",
  "dateOfSurvey": "2025-05-01",
  "likedMost": "campus",
  "interestSource": "friends",
  "recommendLikelihood": "likely",
  "additionalComments": "Loved the campus atmosphere!"
}
```

### Example 3
```
POST /api/surveys
Content-Type: application/json

{
  "firstName": "Bob",
  "lastName": "Johnson",
  "streetAddress": "789 University Blvd",
  "city": "Reston",
  "state": "VA",
  "zipcode": "20190",
  "telephone": "555-123-4567",
  "email": "bob.johnson@example.com",
  "dateOfSurvey": "2025-04-30",
  "likedMost": "sports",
  "interestSource": "television",
  "recommendLikelihood": "unlikely",
  "additionalComments": "Would like to see more sports events."
}
```

