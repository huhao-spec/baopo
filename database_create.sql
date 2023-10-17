CREATE DATABASE test_database;

CREATE TABLE Tempurter (
    main_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    id INT NOT NULL,
    tem VARCHAR(255) NOT NULL,
    PRIMARY KEY (main_time)
);

CREATE TABLE User_Info(
    usr_id VARCHAR(8) NOT NULL,
    usr_name VARCHAR(255) NOT NULL,
    usr_pass VARCHAR(255) NOT NULL,
    PRIMARY KEY (usr_id)
);

-- INSERT INTO User_Info (usr_id, usr_name, usr_pass) 
-- VALUES (SUBSTRING(REPLACE(UUID(), '-', ''), 1, 8), 'John', 'password123');
-- -- 使用UUID()函数生成一个带有标准分隔符的唯一标识符，然后使用REPLACE()函数删除分隔符，
-- -- 最后使用SUBSTRING()函数截取前8位字符作为usr_id的值。'John'和'password123'是示例的usr_name和usr_pass值，
-- -- 你可以根据实际需求进行更改。

CREATE TABLE Tempurter_Limit(
    limit_level INT(1) NOT NULL DEFAULT 1,
    tem_kimit INT(10) NOT NULL DEFAULT 100
);

CREATE TABLE Vedio_Path(
    mp4_name VARCHAR(255) NOT NULL,
    mp4_path VARCHAR(255) NOT NULL
);

CREATE TABLE Using_Logs(
    operation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    usr_id VARCHAR(8) NOT NULL,
    usr_name VARCHAR(255) NOT NULL,
    usr_operation VARCHAR(255) NOT NULL,
    log_path VARCHAR(255) NOT NULL,
    PRIMARY KEY (usr_id)
);

CREATE TABLE admin_info(
    admin_name VARCHAR(255) NOT NULL,
    admin_pass VARCHAR(255) NOT NULL
);

