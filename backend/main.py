from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import asyncpg
import os

# Função para obter a conexão com o banco de dados PostgreSQL
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/musica") 
    return await asyncpg.connect(DATABASE_URL)

# Inicializar a aplicação FastAPI
app = FastAPI()

# Modelo para adicionar novas musicas
class Musica(BaseModel):
    id: Optional[int] = None
    nome: str
    cantor: str
    album: str
    duracao: str
    gostei: bool

class MusicaBase(BaseModel):
    nome: str
    cantor: str
    album: str
    duracao: str
    gostei: bool

class CuritrMusica(BaseModel):
    gostei: Optional[bool] = None;

# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response


# Função para verificar se a musica ja existe
async def musica_existente(nome: str, cantor: str, conn: asyncpg.Connection):
    try:
        query = "SELECT * FROM musicas WHERE LOWER(nome) = LOWER($1) AND LOWER(cantor) = LOWER($2)"
        result = await conn.fetchval(query, nome, cantor)
        return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao verificar se a musica existe: {str(e)}")

# 1. Adicionar musica
@app.post("/api/v1/musicas/", status_code=201)
async def adicionar_musica(msc: MusicaBase):
    conn = await get_database()
    if await musica_existente(msc.nome, msc.autor, conn):
        raise HTTPException(status_code=400, detail="Musica já existe.")
    try:
        query = "INSERT INTO musicas (nome, autor, album, duracao, gostei) VALUES ($1, $2, $3, $4, $5)"
        async with conn.transaction():
            result = await conn.execute(query, msc.nome, msc.cantor, msc.album, msc.duracao, msc.gostei)
            return {"message": "Musica adicionada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao adicionar musica: {str(e)}")
    finally:
        await conn.close()

# 2. Listar todas as musicas
@app.get("/api/v1/musicas/", response_model=List[Musica])
async def listar_musica():
    conn = await get_database()
    try:
        # Buscar todas as musicas no banco de dados
        query = "SELECT * FROM musicas"
        rows = await conn.fetch(query)
        musica = [dict(row) for row in rows]
        return musica
    finally:
        await conn.close()

# Buscar musica por ID
@app.get("/api/v1/musicas/{musica_id}")
async def listar_musica_por_id(musica_id: int):
    conn = await get_database()
    try:
        # Buscar o musica por ID
        query = "SELECT * FROM musicas WHERE id = $1"
        musica = await conn.fetchrow(query, musica_id)
        if musica is None:
            raise HTTPException(status_code=404, detail="Musica não encontrada.")
        return dict(musica)
    finally:
        await conn.close()

# 4. Adicionar a musica como "gostei"
@app.patch("/api/v1/musicas/{musica_id}")
async def curtir_musica(musica_id: int, atualizar_musica: CuritrMusica):
    conn = await get_database()
    try:
        # Verificar se o livro existe
        query = "SELECT * FROM musicas WHERE id = $1"
        musicas = await conn.fetchrow(query, musica_id)
        if musicas is None:
            raise HTTPException(status_code=404, detail="Musica não encontrada!")

        # Atualizar apenas os campos fornecidos
        update_query = """
            UPDATE musicas
            SET titulgostei  = COALESCE($1, gostei),
            WHERE id = $2
        """
        await conn.execute(
            update_query,
            atualizar_musica.gostei,
            musica_id
        )
        return {"message": "Musica atualizada com sucesso!"}
    finally:
        await conn.close()

# 6. Remover uma musica pelo ID
@app.delete("/api/v1/musicas/{musica_id}")
async def excluir_musica(musica_id: int):
    conn = await get_database()
    try:
        # Verificar se a musica existe
        query = "SELECT * FROM musicas WHERE id = $1"
        musica = await conn.fetchrow(query, musica_id)
        if musica is None:
            raise HTTPException(status_code=404, detail="Musica não encontrada.")

        # Remover o musica do banco de dados
        delete_query = "DELETE FROM musicas WHERE id = $1"
        await conn.execute(delete_query, musica_id)
        return {"message": "Musica excluida com sucesso!"}
    finally:
        await conn.close()

# 7. Resetar banco de dados de livros
@app.delete("/api/v1/musicas/")
async def resetar_livros():
    init_sql = os.getenv("INIT_SQL", "db/init.sql")
    conn = await get_database()
    try:
        # Read SQL file contents
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        # Execute SQL commands
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!"}
    finally:
        await conn.close()

# 3. Listar as musicas marcadas como gostei
@app.get("/api/v1/gostei/", response_model=List[Musica])
async def listar_musica_gostei():
    conn = await get_database()
    try:
        # Buscar todas as musicas no banco de dados
        query = "SELECT * FROM musicas WHERE gostei = TRUE"
        rows = await conn.fetch(query)
        musica = [dict(row) for row in rows]
        return musica
    finally:
        await conn.close()
