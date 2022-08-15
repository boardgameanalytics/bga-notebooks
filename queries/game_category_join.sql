/* Select all games and their categories */
SELECT
    g.id as game_id,
    title,
    release_year,
    c.name as category
FROM game g
JOIN game_category gc
    ON gc.game_id = g.id
JOIN category c
    ON c.id = gc.category_id;