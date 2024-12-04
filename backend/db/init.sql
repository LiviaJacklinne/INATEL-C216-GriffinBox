DROP TABLE IF EXISTS "musicas";

CREATE TABLE "musicas" (
    "id" SERIAL PRIMARY KEY,
    "nome" VARCHAR(255) NOT NULL,
    "cantor" VARCHAR(255) NOT NULL,
    "album" VARCHAR(255) NOT NULL,
    "duracao" VARCHAR(255) NOT NULL,
    "gostei" BOOLEAN
);

INSERT INTO "musicas" ("nome", "cantor", "album", "duracao", "gostei") VALUES ('Última saudade', 'Henrique e Juliano', 'Manifesto 2', '2:17', false);
INSERT INTO "musicas" ("nome", "cantor", "album", "duracao", "gostei") VALUES ('Ciumeira', 'Marilia Mendonça', 'Todos os Cantos', '3:10', false);
INSERT INTO "musicas" ("nome", "cantor", "album", "duracao", "gostei") VALUES ('Última noite', 'Léo Foguete', 'Obrigado Deus', '2:34', true);