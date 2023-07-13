-- Averegae weighted average for all
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_score DECIMAL(10, 4);
    DECLARE total_weight DECIMAL(10, 4);
    DECLARE avg_weighted_score DECIMAL(10, 4);
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN user_cursor;

    -- Start looping through users
    users_loop: LOOP
        -- Fetch the next user ID
        FETCH user_cursor INTO user_id;

        IF done THEN
            LEAVE users_loop;
        END IF;

        -- Reset the variables for each user
        SET total_score = 0;
        SET total_weight = 0;
        SET avg_weighted_score = 0;

        -- Compute the total score and total weight for the user
        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO total_score, total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Compute the average weighted score
        IF total_weight > 0 THEN
            SET avg_weighted_score = total_score / total_weight;
        END IF;

        -- Update the user's average weighted score in the users table
        UPDATE users SET average_score = avg_weighted_score WHERE id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END //

DELIMITER ;

