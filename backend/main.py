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


# Função para verificar se a musica ja existe
async def musica_existente(nome: str, cantor: str, conn: asyncpg.Connection):
    try:
        query = "SELECT * FROM musica WHERE LOWER(nome) = LOWER($1) AND LOWER(cantor) = LOWER($2)"
        result = await conn.fetchval(query, nome, cantor)
        return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao verificar se a musica existe: {str(e)}")

# 1. Adicionar musica
@app.post("/api/v1/musica/", status_code=201)
async def add_musica(msc: MusicaBase):
    conn = await get_database()
    if await musica_existente(msc.nome, msc.autor, conn):
        raise HTTPException(status_code=400, detail="Musica já existe.")
    try:
        query = "INSERT INTO musica (nome, autor, album, duracao, gostei) VALUES ($1, $2, $3, $4, $5)"
        async with conn.transaction():
            result = await conn.execute(query, msc.nome, msc.cantor, msc.album, msc.duracao, msc.gostei)
            return {"message": "Musica adicionada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao adicionar musica: {str(e)}")
    finally:
        await conn.close()

# 2. Listar todas as musicas
@app.get("/api/v1/musica/", response_model=List[Musica])
async def listar_musica():
    conn = await get_database()
    try:
        # Buscar todas as musicas no banco de dados
        query = "SELECT * FROM musica"
        rows = await conn.fetch(query)
        musica = [dict(row) for row in rows]
        return musica
    finally:
        await conn.close()


# 3. Listar as musicas marcadas como gostei
@app.get("/api/v1/musica/gostei/", response_model=List[Musica])
async def listar_musica_gostei():
    conn = await get_database()
    try:
        # Buscar todas as musicas no banco de dados
        query = "SELECT * FROM musica WHERE gostei like 'true'"
        rows = await conn.fetch(query)
        musica = [dict(row) for row in rows]
        return musica
    finally:
        await conn.close()
