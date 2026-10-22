-- hytf-crm/sql/migration_v9.sql
-- V9: 新增“网文推广”投放类型（NOVEL_PROMO）
ALTER TABLE t_douyin_account
    MODIFY COLUMN launch_type ENUM('FIRST_CHARGE','EXPOSURE','NOVEL_PROMO') NULL DEFAULT NULL;

ALTER TABLE t_douyin_account
    ADD COLUMN has_novel_promo TINYINT(1) NOT NULL DEFAULT 0 AFTER has_exposure;

-- 回填历史标记（一般为空，幂等安全）
UPDATE t_douyin_account SET has_novel_promo = 1
WHERE launch_type = 'NOVEL_PROMO' OR generated_items LIKE '%NOVEL_PROMO%';