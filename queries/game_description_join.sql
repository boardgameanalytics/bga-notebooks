/* Select all games with descriptions */
SELECT
    g.id as game_id,
    title,
    release_year,
    description
FROM game g
JOIN game_description d
    ON g.id = d.game_id;