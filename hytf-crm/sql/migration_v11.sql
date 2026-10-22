-- v11: 网文客户（无ID）隐藏资金账号标记
SET @col_exists = (SELECT COUNT(*) FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = 'hytf_crm' AND TABLE_NAME = 't_douyin_account' AND COLUMN_NAME = 'is_promo_only');
SET @sql = IF(@col_exists = 0,
  'ALTER TABLE t_douyin_account ADD COLUMN is_promo_only TINYINT(1) NOT NULL DEFAULT 0 AFTER has_novel_promo',
  'SELECT ''is_promo_only already exists'' AS msg');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;