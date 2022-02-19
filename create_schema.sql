CREATE TABLE IF NOT EXISTS `survival_rates` (
  `index` bigint DEFAULT NULL,
  `cohort` text,
  `survival_rate` double DEFAULT NULL,
  KEY `ix_survival_rates_index` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
