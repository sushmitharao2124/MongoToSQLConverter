## Backend Engineering

#### Your task is to create a MongoDB to SQL translator written in Python
Examples:
						
in: db.user.find({name:'julio'}); 
out: SELECT * FROM user WHERE name = 'julio';
						
in: db.user.find({_id:23113},{name:1,age:1}); 
out: SELECT name, age FROM user WHERE _id = 23113;
						
in: db.user.find({age:{$gte:21}},{name:1,_id:1}); 
out: SELECT name, _id FROM user WHERE age >= 21;
						
#### The translator should only support the following mongodb operators:
						
$or
$and( remember $and and comma separated values on an object are the same) 
$lt
$lte
$gt
$gte
$ne
$in

●  There can be any combinations of operators in a single query.

●  The code should be documented, especially supporting the decisions made in terms of algorithms and chosen data structures.

●  The translator only needs to support db.find. It is OK to return an error for all other types of queries.

●  The project should be in python. No external tool should be used as a SQL query builder or for JSON parsing.

●  The evaluation criteria is the same as if you were submitting code to be reviewed by your team.

