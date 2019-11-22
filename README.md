# Code:Rush 2019

## <string:team> backend

Hier entsteht ein super cooles backend für unsere Lösung der HUK-Challenge beim Code:Rush 2019!

## database

tables:
- user

### user table

#### create user
adds a new user to the user table <br>
route: /user <br>
method: POST <br>
expects: json {'id':id, 'name':name}

