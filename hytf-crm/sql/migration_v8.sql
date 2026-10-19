-- hytf-crm/sql/migration_v8.sql
-- V8: 投放类型历史标记列（修复同一 ID 切换类型后旧类型搜不到的问题）
ALTER TABLE t_douyin_account
    ADD COLUMN has_first_charge TINYINT(1) NOT NULL DEFAULT 0 AFTER launch_type,
    ADD COLUMN has_exposure TINYINT(1) NOT NULL DEFAULT 0 AFTER has_first_charge;

-- 回填：按历史批次 launch_type 标记
UPDATE t_douyin_account SET has_first_charge = 1
WHERE launch_type = 'FIRST_CHARGE' OR generated_items LIKE '%FIRST_CHARGE%';

UPDATE t_douyin_account SET has_exposure = 1
WHERE launch_type = 'EXPOSURE' OR generated_items LIKE '%EXPOSURE%';