from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def root():
  return render_template('bootstrap.html'), 200


@app.route('/enternew')
def new_movie():
   return render_template('movies.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         title = request.form['title']
         genre = request.form['genre']
         actors = request.form['actors']
		 year = request.form['year']
		 review = request.form['review']
		 rank = request.form['rank']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO movies (title,genre,actors,year,review,rank) 
               VALUES (?,?,?,?)",(title,genre,actors,year,review,rank) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from movies")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)