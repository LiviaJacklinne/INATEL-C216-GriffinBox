DROP TABLE IF EXISTS "musicas";

CREATE TABLE "musicas" (
    "id" SERIAL PRIMARY KEY,
    "nome" VARCHAR(255) NOT NULL,
    "cantor" VARCHAR(255) NOT NULL,
    "album" VARCHAR(255) NOT NULL,
    "duracao" VARCHAR(255) NOT NULL
);

INSERT INTO "musicas" ("nome", "cantor", "album", "duracao") VALUES ('Última saudade', 'Henrique e Juliano', 'Manifesto 2', '2:17');
INSERT INTO "musicas" ("nome", "cantor", "album", "duracao") VALUES ('Ciumeira', 'Marilia Mendonça', 'Todos os Cantos', '3:10');
INSERT INTO "musicas" ("nome", "cantor", "album", "duracao") VALUES ('Última noite', 'Léo Foguete', 'Obrigado Deus', '2:34');