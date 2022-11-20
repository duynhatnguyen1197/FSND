<h1> FullStack Udacity Final Project Capstone</h1>

<h2>Description</h2>
<p>This web appplication is used create movies and managing and assigning actors to those movies. </p>

<h2>Tech Stack </h2>
<ul>
  <li>AUTH0 to generate and verify token</li>
  <li>Heroku
    <ul>
    <li>Deploy and host webapp</li>
    <li>Store data on postgres server</li>
    </ul>
  </li>
  <li>Python</li>
</ul>  
<h2>Prerequisite</h2>
<ul>
  <li>Python 3.x.x</li>
  <li><a href="https://pip.pypa.io/en/stable/installation/">Pip</a></li>
  <li><a href="https://www.postgresql.org/download/">Postgres</a></li>
</ul>
<h2>Project Dependencies</h2>
<p>Install package need to run this project</p>

```
pip install -r requirements.txt
```
<h2>Database</h2>
<ol>
  <li>
    <p>Create postgres database name "hollywood"</p>

```
create database hollywood;
```


  </li>
  <li>
    <p>Migrate</p>

```
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

  </li>
</ol>

<h2>Authentication</h2>
<p>We use <a href="https://auth0.com/">auth0</a> as third party authenticate</p>
<p>Role in project</p>
<ul>
  <li>Producer
    <ul>
      <li>View all data</li>
      <li>Add and delete Movie</li>
      <li>Add and delete Actor</li>
      <li>Edit Movie and Actor</li>
    </ul>
  </li>
  <li>Director
    <ul>
        <li>View all data</li>
        <li>Add and delete Actor</li>
        <li>Edit Movie and Actor</li>
      </ul>
  </li>
  <li>Assistant
    <ul>
        <li>View all data</li>
      </ul>
  </li>
</ul>
<h2>Local Run</h2>
<ul>
  <li><p>Renew JWT token</p>
    <p>
    Renew JWT token by access 
      <a href="https://dev-igo2gl7vxtgecv64.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=jewOjQ6kwVqyu3CtrbC7IRsJsGYfzL4l&redirect_uri=https://duyhuynhnguyen-final.herokuapp.com/
">
          AUTH0 domain
      </a>
    </p>
    <p>Update JWT token in ".env".You need an account to login (Contact me to get new JWT token)</p>
  </li>
  <li><p>Run Flask app</p>


```
cd duyhuynhnguyen-final
pyhon3 app.py
```

  </li>
</ul>

<h2>Test</h2>
<p>After you run application, open new terminal</p>
<p>Run</p>

```
python3 test_app.py
```
    
<h2>API</h2>
<ul>
  <li>GET: /data
    <ul>
      <li>Description: get all movies and actors play in that movie</li>
      <li>Sample : <code>curl -X GET http://127.0.0.1:5000/data</code></li>
    </ul>
  </li>
  <li>GET: /actors
    <ul>
      <li>Description: get all actors</li>
      <li>Sample : <code>curl -X GET http://127.0.0.1:5000/actors</code></li>
    </ul>
  <li>GET: /movies
    <ul>
      <li>Description: get all movies</li>
      <li>Sample : <code>curl -X GET http://127.0.0.1:5000/movies</code></li>
    </ul>
  <li>DELETE: /actor/{actor_id}
    <ul>
      <li>Description: delete actor by id</li>
      <li>Sample : <code>curl -X DELETE http://127.0.0.1:5000/actor/1</code></li>
    </ul>
  <li>DELETE: /movie/{movie_id}
    <ul>
      <li>Description: delete movie by id</li>
      <li>Sample : <code>curl -X DELETE http://127.0.0.1:5000/actor/1</code></li>
    </ul>
  </li>
  <li>POST: /movie
    <ul>
      <li>Description: add new movie</li>
      <li>Body:
<p>

```json
{
    "title":"Gone with the wind",
    "release_date":"12/24/2022",
    "actors":["Hong","Linh"]
}
```

</p>
<p>"actors": name of actors will play in the movie</p>
      </li>
    </ul>
  </li>
<li>POST: /actor
    <ul>
      <li>Description: add new actor</li>
      <li>Body:
<p>

```json
{
    "name":"Hong",
    "gender":"Female",
    "age":100
}
```

</p>
      </li>
    </ul>
  </li>
<li>PATCH: /actor/{actor_id}
    <ul>
      <li>Description: edit actor by id</li>
      <li>Body:
<p>

```json
{
    "name":"Linh",
    "gender":"Female",
    "age":100
}
```

</p>
      </li>
    </ul>
  </li>
<li>PATCH: /movie/{movie_id}
    <ul>
      <li>Description: edit movie by id</li>
      <li>Body:
<p>

```json
{
    "title":"New Name",
    "release_date":"",
    "add_actors":["Linh"],   
    "remove_actors":[]	     
}
```

</p>
<p>"add_actors": name of actors need to be added</p>
<p>"remove_actors": name of actors need to be removed</p>
      </li>
    </ul>
  </li>
</ul>

<h3>Link to my app on <a href="https://duyhuynhnguyen-final.herokuapp.com/">Heroku</a></h3>