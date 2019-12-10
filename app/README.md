# CISC 3140 Class Project

To run the app.py file, you must set up a local database (for now), preferably MySQL, with the appropriate columns and properties. 
(In Addition to everything written in the main README)

A table for Users:
- `ID`: An integer, primary key, auto increments 
- `First Name`: A string or varchar, cannot be null
- `Last name`: A string or varchar, cannot be null
- `Email`: A string or varchar, must be unique, cannot be null
- `Username`: A string or varchar, must be unique, cannot be null 
- `Password`: A string or varchar, cannot be null 
- `Occupation`: A string or varchar, can be null
- `Biography`: A string or varchar, can be null
- `Github_Link`: A string or varchar, can be null
- `Posts`: back reference (one to many relationship to the Post table)


A table for Posts:
- `Post_ID`: An integer, primary key, auto increments
- `Title`: A string or varchar, cannot be null
- `Date_Posted`: A timestamp, initialized automatically
- `Content`: A string or varchar, cannot be null
- `Likes`: An integer, initialized to 1
- `User_ID`: A foriegn key integer, each "Post" must be created by one user


In Addition, you must set up 4 environment variables:
- `SQLALCHEMY_DATABASE_URI`: The URI for you local database, which follows a format such as `'mysql+pymysql://user:password@127.0.0.1:3306/dbName'`
- `SECRET_KEY`: A "secret" key for performing certain operations, usually a random sequence of characters (one given in app.py)
- `MAIL_USERNAME`: Your email that can actually send emails for password reset purposes (in this case it's using gmail)
- `MAIL_PASSWORD`: That email's password
