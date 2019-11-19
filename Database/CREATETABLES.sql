/*
Name: MySQL DATABASE CICS3140
Author: VADZIM ARLOU
Version 0.9(BETA) TESTING PHASE 
*********************************************************************
*/ /*
        TO DO: CREATE VIEWS
               CHECK  DATA TYPES
               CONSOLIDATE DTA NEEDED WITH BACKEND
               GET SPECIFICATION ON WHAT QUIRIES ARE NEEDED IN A DATABASE
    */

/**********************************************************************/
DROP TABLE IF EXISTS `users`;
CREATE TABLE  `users`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`u_login` CHAR(16) NOT NULL UNIQUE,
	`u_password` CHAR(32) NOT NULL,
	`email` VARCHAR(50) NOT NULL UNIQUE,
	`nickname` VARCHAR(32),
	`u_github` VARCHAR(32),
	`reg_date`   DATETIME,
	`last_visit` DATETIME,
	`avatarPath` CHAR(36),
	`role_id` INT NOT NULL,
	`completed_projects` INT NOT NULL,

  CONSTRAINT `users_pk` PRIMARY KEY (`id`)
  /*
  Add all the foreign keys later with Alter table 
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`),
  FOREIGN KEY (`completed_projects`) REFERENCES `projectsdirectory`(`id`)
  */
);

ALTER TABLE `users` AUTO_INCREMENT = 1000;

INSERT INTO `users`(u_login,u_password,email, role_id, completed_projects)
values('rtstag', 'dfasdf', 'gadsg@gmail.com', 13, 1567);

/**********************************************************************/
/**********************************************************************/
/**********************************************************************/

DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles`(
	`id` int AUTO_INCREMENT,
	`code` char(16) NOT NULL UNIQUE,
	`name` varchar(32) NOT NULL,
	`isAdmin` BIT NOT NULL,
	PRIMARY KEY (`id`)
);

INSERT INTO `roles`(`code`, `name`, `isAdmin`) values
('BackEnd',   'role description', 0),
('FrontEnd',  'role description', 0),
('FullStack', 'role description', 0),
('AIsound',   'role description', 0),
('GameDev',   'eole description', 1);
/*ADD AS MANY ROLES AS YOU LIKE*/

/**********************************************************************/
/**********************************************************************/
/**********************************************************************/

DROP TABLE IF EXISTS `projectsdirectory`;
CREATE TABLE `projectsdirectory` (
	`id` INT NOT NULL,
	`parent_id` INT,
	`p_name` VARCHAR(20) NOT NULL,
	`p_description` TEXT NOT NULL,
	`p_status`  CHAR(13) NOT NULL,
	`p_roles`   VARCHAR(250) NOT NULL,
	`git_link`  VARCHAR(30) NOT NULL,
	`isVisible` BIT default 1,
	`urlName`   VARCHAR(75) NOT NULL,
	`author_id` INT NOT NULL,
	
	/*
    Add all the foreign keys later with Alter table 
	*/
	CONSTRAINT `project_pk` PRIMARY KEY (`id`),
	CONSTRAINT `folder_fk` FOREIGN KEY (`parent_id`) REFERENCES `projectsdirectory`(`id`), 
	CONSTRAINT `author_fk` FOREIGN KEY (`author_id`) REFERENCES `users`(`id`)
);

INSERT INTO `projectsdirectory`()
values
(0001, 1,'SPACE', 'Imun dnfa fdasfa sdaf', 'ACTIVE', 'In search of backend engineer', 
                                                        'https://github.com/', 1, 'http:/something/...', 1000),
(0002, 1,'FLOWER','Imun dnfa fdasfa sdaf', 'INACTIVE', 'In search of frontend engineer', 
                                                        'https://github.com/', 1, 'http:/something/...', 1000),
(0003, 2,'SPACE', 'Imun dnfa fdasfa sdaf', 'ACTIVE', 'In search of backend engineer', 
                                                        'https://github.com/', 1, 'http:/something/...', 1000);
                                                        

/**********************************************************************/
/**********************************************************************/
/**********************************************************************/
/*!!!USER POSTS also contain any information visible on the profile page!!!*/
/*CHECK WHAT KIND OF DATA YOU NEED*/
DROP TABLE IF EXISTS `userposts`;
CREATE TABLE `userposts`(
    `id`    INT PRIMARY KEY,
    `userID`INT NOT NULL,
    `date`  TIMESTAMP NOT NULL,
    `post`  TEXT NOT NULL,
    `type`  INT  NOT NULL,
    `author`INT  NOT NULL,
    `isActive` BIT,
    `isIssue`  BIT,
    `hasMediaFiles` BIT,
    `media_links` JSON,/*ALL USER RELATED files stored in JSON, images(avatar), info etc.*/
    `visibleProfileInfo` TEXT,
    /*first foreign key is about where thread lives*/
    CONSTRAINT `who_posted_fk`  FOREIGN KEY(`userID`) REFERENCES `users`(`id`),
    /*second foreign key is anyone who posts on the thread*/
    CONSTRAINT `post_author_fk` FOREIGN KEY(`userID`) REFERENCES `users`(`id`)
);
SET time_zone='+00:00';


/**********************************************************************/
/**********************************************************************/
/**********************************************************************/
/*
DROP TABLE IF EXISTS `userinformation`;
CREATE TABLE `userinformation`(
    `id` INT PRIMARY KEY,
    `userID` INT NOT NULL,
    `addedDate` date
);
*/
/*Just a simple view should be created instead of the table for a quick access to htis information*/
DROP TABLE IF EXISTS `userprojectlist`; 
CREATE TABLE `userprojectlist`(
    `id` INT PRIMARY KEY,
    `addedDate` DATETIME,
    `userID` INT,
    
    CONSTRAINT `user_fk` FOREIGN KEY(`userID`) REFERENCES `users`(`id`),
    CONSTRAINT `projects_fk` FOREIGN KEY(`id`) REFERENCES `projectsdirectory`(`id`)
);

/**********************************************************************/
/**********************************************************************/
/**********************************************************************/

DROP TABLE IF EXISTS `projectfiles`;
CREATE TABLE `projectfiles`(
    `hostID`INT NOT NULL,
    `authorID` INT NOT NULL,
    `accessLevel` CHAR(15) NOT NULL,/*DEFINE TYPES: private, protected, public and compare them in code for faster processing*/
    `addedDate` DATETIME,
    `parentDirectory` INT NOT NULL,
    `fileURL` VARCHAR(75) NOT NULL,
    `hasJason` BIT NOT NULL,
    `json_file` JSON,
    `hasGitLink` BIT NOT NULL,
    `gitURL` VARCHAR(75),
    `type` CHAR(15) NOT NULL,/*Define the common file types, so you can quickly dtermine it*/
    
    CONSTRAINT `id_pk` PRIMARY KEY(`hostID`),
    CONSTRAINT `host_fk` FOREIGN KEY(`hostID`) REFERENCES `users`(`id`),
    CONSTRAINT `file_author_fk` FOREIGN KEY(`authorID`) REFERENCES `users`(`id`),
    CONSTRAINT `project_fk`FOREIGN KEY(`parentDirectory`) REFERENCES `projectsdirectory`(`id`)
);