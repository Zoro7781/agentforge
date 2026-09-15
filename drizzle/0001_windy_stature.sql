ALTER TABLE `builds` ADD `testing_started` integer;--> statement-breakpoint
CREATE UNIQUE INDEX `idx_builds_project_digest` ON `builds` (`project_id`,`digest`);