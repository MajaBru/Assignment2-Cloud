CREATE DATABASE IF NOT EXISTS fakeredditdb;

USE fakeredditdb;

CREATE TABLE IF NOT EXISTS `user` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) UNIQUE NOT NULL,
    `email` VARCHAR(100) UNIQUE NOT NULL,
    `password` VARCHAR(100) NOT NULL,
    `created_at` DATETIME
);


CREATE TABLE IF NOT EXISTS `post` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `text` VARCHAR(255) NOT NULL,
    `category` VARCHAR(50) NOT NULL,
    `created_at` DATETIME,
    `likes_count` INT DEFAULT 0,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
);


INSERT INTO `user` (`username`, `email`, `password`)
VALUES ('JabbaTheHutt', 'jabba@mail.com', 'jabba@mail.com'),
       ('John', 'johndoe@mail.com', 'johndoe@mail.com'),
       ('Jane', 'janedoe@mail.com', 'janedoe@mail.com'),
       ('Harry', 'harry@mail.com', 'harry@mail.com');



INSERT INTO `post` (`user_id`, `text`, `category`)
VALUES (1, 'My bunny bit me, help!', 'Bunnies'),
       (2, 'Dog breeding is weird. I once had a pug, and it couldnt breath. Poor dog.', 'Dogs'),
       (3, 'My cat is speaking human words. Is this normal?', 'Cats'),
        (4, 'How can I become a better dog owner? Im lazy af.', 'Dogs'),
        (1, 'Big bunny viciously attacks child! (Must watch) ', 'Bunnies'),
        (2, 'I want to adopt a dog, but I dont know what breed to choose. Any suggestions?', 'Dogs'),
        (3, 'My cat is a genius. He can open doors.', 'Cats'),
        (1, 'What the dog doin?', 'Dogs'),
        (4, 'What is the best dog food brand?', 'Dogs'),
        (1, 'These kittens are adorable!', 'Cats'),
        (2, 'My dog is demonic. Do I need to call the exorcist?', 'Dogs'),
        (3, 'Today, my cat died at 20 years old. I will miss her.', 'Cats'),
        (4, 'I like dogs better than people. Can anyone relate?', 'Dogs'),
        (1, 'My bunny is a ninja. He can jump 2 meters high.', 'Bunnies'),
        (2, 'How do I prevent my cat from becoming too fat? All she does is EAT.', 'Cats'),
        (3, 'My cat is a model. She poses for the camera.', 'Cats'),
        (4, 'I want to adopt a cat, but I dont know what breed to choose. Any suggestions?', 'Cats'),
        (1, 'My bunny is blind. On the daily, I have to help him navigate the house.', 'Bunnies'),
        (2, 'Such a distinguished gentleman.', 'Dogs'),
        (3, 'I cannot believe my bunny ate my homework. All that work for nothing', 'Bunnies');

