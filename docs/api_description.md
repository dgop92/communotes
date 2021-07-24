Communotes API allows students to search formula photos of some subjects uploaded by the community. The community is made up of students which are taking the same subject or already took the subject and want to contribute

### Authentication

This API uses jwt tokens as authentication system, for more details about authentication and account management see [Auth API](https://github.com/)

### Pagination

All endpoints that retrieve items have the same pagination system <br>
Pagination examples can be found in [subject list](#/formulas/formulas_subjects_list)

```javascript
{
   "count":17,
   "next":"{baseUrl}/{path}/?page=3",
   "previous":"{baseUrl}/{path}/?page=2",
   "results":[
      "..."
   ]
}
```

#### JSON fields description

| field    | description                                                        |
|----------|--------------------------------------------------------------------|
| count    | total of items                                                     |
| next     | link to the next page of items, null if no next page exits         |
| previous | link to the previous page of items, null if no previous page exits |
| results  | list of items                                                      |

#### Query params

| param     | description                                             |
|-----------|---------------------------------------------------------|
| page      | an integer that represents the page to retrieve         |
| page_size | an integer from 1 to 100 that represents the page size  |


### Ordering, searching, and filtering

Some endpoints provide the ability of ordering results by a field or multiple fields. Those fields are specified in the endpoint description

* example for ordering by a single field `?ordering=field_name`

* example for ordering by multiple field `?ordering=field_name1,field_name2`

searching is similar to ordering so fields specified in the endpoint's description will tell you the available fields used in the search

* example for searching `?search=search_term`

and finally filtering works as expected field-value query params, if the value provided is invalid or does not exit a bad request will be the response

* example for searching `?field=value`

### Errors

This API is made using django REST framework, so there is a common structure while handling errors

#### Form Errors

If you use one of the following methods POST, PUT or PATCH and receive a 400 BAD REQUEST the JSON structure probably will be the following:

```
{
   "field_name": [List[str]],
   "non_field_errors": [List[str]]
}
```

Errors related to a field will have its own list of errors, this is also the same for those errors that are not related to any field

```
{
  "name": [
    "This field is required."
  ],
  "photo_classification": {
    "subject": [
      "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens."
    ],
    "exam_number": [
      "Ensure this value is less than or equal to 6."
    ]
  },
  "photo_context": {
    "formula_type": [
      "\"F21\" is not a valid choice."
    ]
  }
}
```

Note: Nested relationship follow the same structure

#### Authtentication Errors

If an endpoint required authentication and is not provided this will be the response

```
{
  "detail": "Authentication credentials were not provided."
}
```

If you don't have permission and try to access an endpoint anyways this will be the response

```
{
  "detail": "You do not have permission to perform this action."
}
```

#### Not Found Error

If you try to access to a resource that doesn't exist this will be the response

```
{
  "detail": "Not found."
}
```
