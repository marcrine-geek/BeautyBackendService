## api endpoints

# POST
## register
### tested
`/api/register`

```json
requires
{
    "email":string,
    "password":string,
    "fullname":string
}
```
```json
response status 200
{
    "email": "user85@gmail.com",
    "message": "user registered successfully",
    "status": 200
}
```
```json
response status 400
{
    "message": "Unauthorized user",
    "status": 400
}
```

# POST
## login
### tested
`/api/ogin`
```json
requires
{
    "email":string,
    "password":string
}
```
```json
response status 200
{
    "message": "successful login",
    "email": "marc@gmail.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hcmNAZ21haWwuY29tIiwidXNlcmlkIjo2LCJleHAiOjE3MDE5NDA3NTl9.hry3Xzex7s6pPmkrBlfbcyGeTEBiPWz43CFr3Yebll4",
    "status": 200
}
```
```json
response status 400
{
    "message": "Unauthorized user",
    "status": 400
}
```
