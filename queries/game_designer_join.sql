/* Select all (non-nested) game data */
SELECT
    g.id as game_id,
    title,
    release_year,
    avg_rating,
    bayes_rating,
    total_ratings,
    std_ratings,
    min_players,
    max_players,
    min_playtime,
    max_playtime,
    weight,
    owned_copies,
    d.name AS designer
FROM game g
LEFT JOIN game_designer gd
    ON gd.game_id = g.id
LEFT JOIN designer d
    ON d.id = gd.designer_id;