CREATE DATABASE mindmirror_db;
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

CREATE TABLE entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    entry_date DATE,
    statement TEXT,
    mood_category VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- 5 users insert 
INSERT INTO users (username) VALUES 
('Ayesha'), ('Bilal'), ('Sara'), ('Hamza'), ('Zainab');

-- Ayesha (user_id = 1) 
INSERT INTO entries (user_id, entry_date, statement, mood_category) VALUES
(1, '2026-08-18', 'Had a really productive day and finished all my tasks', 'Feeling Good'),
(1, '2026-08-19', 'Anxious about the upcoming exam, cant focus properly', 'A Bit Overwhelmed'),
(1, '2026-08-20', 'Feeling really low today, nothing seems to be going right', 'Going Through a Tough Time'),
(1, '2026-08-21', 'Spent time with friends, feeling happy and relaxed', 'Feeling Good'),
(1, '2026-08-22', 'So much work piling up, feeling stressed about deadlines', 'A Bit Overwhelmed'),
(1, '2026-08-23', 'Struggling to find motivation to get out of bed', 'Going Through a Tough Time'),
(1, '2026-08-24', 'I dont see the point in anything anymore', "You're not Alone"),
(1, '2026-08-25', 'Went for a walk in the morning, feeling refreshed', 'Feeling Good'),
(1, '2026-08-26', 'Worried about how things will turn out this week', 'A Bit Overwhelmed'),
(1, '2026-08-27', 'Everything feels heavy and exhausting lately', 'Going Through a Tough Time'),
(1, '2026-08-28', 'Had a good conversation with family, feeling grateful', 'Feeling Good'),
(1, '2026-08-29', 'Feeling nervous about the presentation tomorrow', 'A Bit Overwhelmed'),
(1, '2026-08-30', 'Cant shake off this sad feeling since morning', 'Going Through a Tough Time'),
(1, '2026-08-31', 'Completed my project ahead of deadline, feeling accomplished', 'Feeling Good');

-- Bilal (user_id = 2)
INSERT INTO entries (user_id, entry_date, statement, mood_category) VALUES
(2, '2026-08-18', 'Finished reading a book I loved, feeling accomplished', 'Feeling Good'),
(2, '2026-08-19', 'Too many assignments due this week, feeling the pressure', 'A Bit Overwhelmed'),
(2, '2026-08-20', 'Barely got out of bed today, everything feels pointless', 'Going Through a Tough Time'),
(2, '2026-08-21', 'Played football with friends, had a great time', 'Feeling Good'),
(2, '2026-08-22', 'Cant stop overthinking about my future, feeling anxious', 'A Bit Overwhelmed'),
(2, '2026-08-23', 'Feeling numb, dont really want to talk to anyone', 'Going Through a Tough Time'),
(2, '2026-08-24', 'I feel like giving up, nothing I do matters', "You're not Alone"),
(2, '2026-08-25', 'Cooked a new recipe today, felt proud of myself', 'Feeling Good'),
(2, '2026-08-26', 'Deadline stress is getting to me, hard to relax', 'A Bit Overwhelmed'),
(2, '2026-08-27', 'Feeling drained, like I have no energy left', 'Going Through a Tough Time'),
(2, '2026-08-28', 'Had a peaceful morning, listened to my favorite music', 'Feeling Good'),
(2, '2026-08-29', 'Nervous about my interview next week', 'A Bit Overwhelmed'),
(2, '2026-08-30', 'Just want to be left alone, feeling isolated', 'Going Through a Tough Time'),
(2, '2026-08-31', 'Got good news today, feeling optimistic about things', 'Feeling Good');

-- Sara (user_id = 3)
INSERT INTO entries (user_id, entry_date, statement, mood_category) VALUES
(3, '2026-08-18', 'Had coffee with an old friend, felt really nice catching up', 'Feeling Good'),
(3, '2026-08-19', 'Juggling college and part time job, feeling exhausted', 'A Bit Overwhelmed'),
(3, '2026-08-20', 'Cried for no reason today, dont know whats wrong', 'Going Through a Tough Time'),
(3, '2026-08-21', 'Aced my test, feeling really proud of my hard work', 'Feeling Good'),
(3, '2026-08-22', 'Overthinking every little decision lately, feels exhausting', 'A Bit Overwhelmed'),
(3, '2026-08-23', 'Feel like a burden to everyone around me', 'Going Through a Tough Time'),
(3, '2026-08-24', 'Sometimes I wonder if anyone would even miss me', "You're not Alone"),
(3, '2026-08-25', 'Went shopping with mom, had a lovely day', 'Feeling Good'),
(3, '2026-08-26', 'Presentation coming up and I havent prepared enough, panicking', 'A Bit Overwhelmed'),
(3, '2026-08-27', 'Lost interest in things I used to enjoy', 'Going Through a Tough Time'),
(3, '2026-08-28', 'Got a compliment from my professor, feeling motivated', 'Feeling Good'),
(3, '2026-08-29', 'Worried I wont finish my project on time', 'A Bit Overwhelmed'),
(3, '2026-08-30', 'Feeling empty inside, hard to explain', 'Going Through a Tough Time'),
(3, '2026-08-31', 'Family dinner tonight, felt warm and loved', 'Feeling Good');

-- Hamza (user_id = 4)
INSERT INTO entries (user_id, entry_date, statement, mood_category) VALUES
(4, '2026-08-18', 'Finally fixed my bike, small win but felt great', 'Feeling Good'),
(4, '2026-08-19', 'Rent due and bills piling up, feeling financial stress', 'A Bit Overwhelmed'),
(4, '2026-08-20', 'Havent left my room in two days, feeling stuck', 'Going Through a Tough Time'),
(4, '2026-08-21', 'Went hiking with friends, felt alive and happy', 'Feeling Good'),
(4, '2026-08-22', 'Job interview results pending, cant stop checking my phone', 'A Bit Overwhelmed'),
(4, '2026-08-23', 'Feel like a failure compared to everyone else', 'Going Through a Tough Time'),
(4, '2026-08-24', 'Thinking things would be easier if I just wasnt here', "You're not Alone"),
(4, '2026-08-25', 'Helped a neighbor today, felt good about myself', 'Feeling Good'),
(4, '2026-08-26', 'So much on my plate, dont know where to start', 'A Bit Overwhelmed'),
(4, '2026-08-27', 'Everything feels grey and dull lately', 'Going Through a Tough Time'),
(4, '2026-08-28', 'Watched a great movie, laughed a lot tonight', 'Feeling Good'),
(4, '2026-08-29', 'Exam results tomorrow, feeling really tense', 'A Bit Overwhelmed'),
(4, '2026-08-30', 'Dont feel like eating or doing anything today', 'Going Through a Tough Time'),
(4, '2026-08-31', 'Got a promotion at work, feeling on top of the world', 'Feeling Good');

-- Zainab (user_id = 5)
INSERT INTO entries (user_id, entry_date, statement, mood_category) VALUES
(5, '2026-08-18', 'Painted for the first time in months, felt so relaxing', 'Feeling Good'),
(5, '2026-08-19', 'Group project mates not cooperating, stressing me out', 'A Bit Overwhelmed'),
(5, '2026-08-20', 'Feeling disconnected from my own life lately', 'Going Through a Tough Time'),
(5, '2026-08-21', 'Celebrated my sisters birthday, such a fun evening', 'Feeling Good'),
(5, '2026-08-22', 'Cant sleep properly, mind racing with worries', 'A Bit Overwhelmed'),
(5, '2026-08-23', 'Nothing excites me anymore, just going through the motions', 'Going Through a Tough Time'),
(5, '2026-08-24', 'I feel invisible, like nobody really sees me', "You're not Alone"),
(5, '2026-08-25', 'Tried a new workout routine, feeling energized', 'Feeling Good'),
(5, '2026-08-26', 'Scholarship application deadline stressing me out badly', 'A Bit Overwhelmed'),
(5, '2026-08-27', 'Feel like crying but dont even know why', 'Going Through a Tough Time'),
(5, '2026-08-28', 'Had a lovely video call with my cousins abroad', 'Feeling Good'),
(5, '2026-08-29', 'Overwhelmed with thesis work, feeling behind schedule', 'A Bit Overwhelmed'),
(5, '2026-08-30', 'Just feeling really low with no clear reason', 'Going Through a Tough Time'),
(5, '2026-08-31', 'Small progress on my goals today, feeling hopeful', 'Feeling Good');

INSERT INTO entries (user_id, entry_date, statement, mood_category) VALUES
(6, '2026-08-18', 'Started my new semester with a lot of enthusiasm', 'Feeling Good'),
(6, '2026-08-19', 'First week going well, feeling confident', 'Feeling Good'),
(6, '2026-08-20', 'A few assignments due but managing okay', 'A Bit Overwhelmed'),
(6, '2026-08-21', 'Had a nice weekend, relaxed and recharged', 'Feeling Good'),
(6, '2026-08-22', 'Workload is increasing, feeling a bit anxious', 'A Bit Overwhelmed'),
(6, '2026-08-23', 'Struggling to keep up with everything now', 'A Bit Overwhelmed'),
(6, '2026-08-24', 'Feeling tired all the time lately, no energy', 'Going Through a Tough Time'),
(6, '2026-08-25', 'Cant seem to catch up no matter how hard I try', 'Going Through a Tough Time'),
(6, '2026-08-26', 'Isolating myself from friends, dont feel like talking', 'Going Through a Tough Time'),
(6, '2026-08-27', 'Everything feels like its falling apart', 'Going Through a Tough Time'),
(6, '2026-08-28', 'I dont know how much longer I can keep pushing through this', "You're not Alone"),
(6, '2026-08-29', 'Feel completely overwhelmed and hopeless', "You're not Alone"),
(6, '2026-08-30', 'Just want everything to stop for a while', "You're not Alone"),
(6, '2026-08-31', 'Still feeling really low, hard to see a way out', 'Going Through a Tough Time');

SELECT username, COUNT(*) as total_entries 
FROM entries e JOIN users u ON e.user_id = u.user_id 
GROUP BY username;

