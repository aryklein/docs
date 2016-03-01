BEGIN;
CREATE TABLE `domain` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(128) NOT NULL,
    `relay` boolean NOT NULL DEFAULT true,
    UNIQUE KEY `name` (`name`)
);
CREATE TABLE `transport` (
    `id` integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `domain_id` integer NOT NULL,
    `type` varchar(128) NOT NULL default 'lmtp:unix:private/dovecot-lmtp',
    CONSTRAINT `fk_transport_domain` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`),
    UNIQUE KEY `domain_id` (`domain_id`)
);
CREATE TABLE `virtual_user` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `domain_id` integer NOT NULL,
    `comment` varchar(255) NOT NULL,
    `address` varchar(255) NOT NULL,
    `pass` varchar(128) NOT NULL,
    `uid` smallint unsigned NOT NULL default 107,
    `gid` smallint unsigned NOT NULL default 114,
    `home` varchar(128) NOT NULL default '/var/vmail',
    `maildir` varchar(255) NOT NULL,
    `quota` bigint NOT NULL default '0',
    `active` boolean NOT NULL default true,
    `allow_imap` boolean NOT NULL default true,
    `allow_pop3` boolean NOT NULL default true,
    `last_login_ip` varchar(16),
    `last_login_date` DATETIME,
    `last_login_proto` varchar(5),
    CONSTRAINT `fk_virtual_user_domain` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`),
    UNIQUE KEY `address` (`address`)
);
CREATE TABLE `virtual_alias_map` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `domain_id` integer NOT NULL,
    `recipient` varchar(255) NOT NULL,
    `destination` TEXT NOT NULL,
    CONSTRAINT `fk_virtual_alias_map_domain` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`),
    UNIQUE KEY `recipient` (`recipient`)
);
COMMIT;
