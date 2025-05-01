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

## Example GET request
```
GET /api/surveys
```
Returns a list of all surveys.

```
GET /api/surveys/{id}
```
Returns a single survey by its ID.

## Example PUT request
```
PUT /api/surveys/1
Content-Type: application/json

{
  "firstName": "Updated",
  "lastName": "Name",
  "streetAddress": "999 New St",
  "city": "Reston",
  "state": "VA",
  "zipcode": "20190",
  "telephone": "555-000-0000",
  "email": "updated.email@example.com",
  "dateOfSurvey": "2025-05-01",
  "likedMost": "campus",
  "interestSource": "internet",
  "recommendLikelihood": "likely",
  "additionalComments": "Updated comment."
}
```
Updates the survey with ID 1.

## Example DELETE request
```
DELETE /api/surveys/1
```
Deletes the survey with ID 1.

---

## Note about db_secret.json
The `db_secret.json` file in this GitHub repo is just an example of the format required for database secrets. **You must upload your own `db_secret.json` as a Jenkins secret file with your actual RDS database name, admin username, and password.**

Example format:
```
{
  "DB_NAME": "your_db_name",
  "DB_USER": "your_db_user",
  "DB_PASSWORD": "your_db_password",
  "DB_HOST": "your_db_host",
  "DB_PORT": 3306
}
```

