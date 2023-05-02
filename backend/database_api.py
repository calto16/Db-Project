from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid
import uvicorn
import mysql.connector

app = FastAPI()

# allow cross-origin resource sharing (CORS)
origins = ['http://localhost:8080', '*']
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# MySQL database configuration
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",
    database="mariadb"
)

# Route to get all games
@app.get('/games')
async def get_all_games():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    cursor.close()
    print(JSONResponse(content=games))
    return JSONResponse(content=games)

# Route to add a new game
@app.post('/games')
async def add_game(title: str, genre: str, played: bool):
    cursor = mydb.cursor()
    id = uuid.uuid4().hex
    sql = "INSERT INTO games (id, title, genre, played) VALUES ( %s, %s, %s, %s)"
    val = (id, title, genre, played)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    return JSONResponse(content={"message": "Game Added!"})

# Route to get a single game by ID
@app.get('/games/{game_id}')
async def get_game_by_id(game_id: int):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM games WHERE id = %s", (game_id,))
    game = cursor.fetchone()
    cursor.close()
    if game:
        return JSONResponse(content=game)
    else:
        return JSONResponse(content={"error": "Game not found!"})

# Route to update a game
@app.put('/games/{game_id}')
async def update_game(game_id: int, title: str, genre: str, played: bool):
    cursor = mydb.cursor()
    sql = "UPDATE games SET title = %s, genre = %s, played = %s WHERE id = %s"
    val = (title, genre, played, game_id)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    return JSONResponse(content={"message": "Game updated!"})

# Route to delete a game
@app.delete('/games/{game_id}')
async def delete_game(game_id: int):
    cursor = mydb.cursor()
    sql = "DELETE FROM games WHERE id = %s"
    val = (game_id,)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    return JSONResponse(content={"message": "Game deleted!"})

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
