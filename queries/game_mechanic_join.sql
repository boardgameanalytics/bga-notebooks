/* Select all games and their mechanics */
SELECT
    g.id AS game_id,
    title,
    release_year,
    m.name AS mechanic
FROM game g
JOIN game_mechanic gm
    ON gm.game_id = g.id
JOIN mechanic m
    ON m.id = gm.mechanic_id;