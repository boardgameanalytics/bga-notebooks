/* Select all games and counts of all their classifications */
SELECT
    g.id AS game_id,
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
    min_age,
    weight,
    owned_copies,
    wishlist,
    kickstarter,
	COUNT(DISTINCT(ga.artist_id)) as artists,
	COUNT(DISTINCT(gc.category_id)) as categories,
	COUNT(DISTINCT(gd.designer_id)) as designers,
    COUNT(DISTINCT(gm.mechanic_id)) as mechanics,
	COUNT(DISTINCT(gp.publisher_id)) as publishers
FROM game g
JOIN game_artist ga ON ga.game_id = g.id
JOIN game_category gc ON gc.game_id = g.id
JOIN game_designer gd ON gd.game_id = g.id
JOIN game_mechanic gm ON gm.game_id = g.id
JOIN game_publisher gp ON gp.game_id = g.id
GROUP BY g.id;