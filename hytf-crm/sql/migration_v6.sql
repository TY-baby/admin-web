-- hytf-crm/sql/migration_v6.sql
-- V6: 出款管理增加类型（首充/曝光度）字段，并回填历史数据
ALTER TABLE t_withdraw
    ADD COLUMN launch_type VARCHAR(20) NOT NULL DEFAULT '' AFTER douyin_name;

CREATE INDEX idx_withdraw_launch_type ON t_withdraw (launch_type);

-- 回填：按 douyin_account 的当前 launch_type 兜底
UPDATE t_withdraw w
    JOIN t_douyin_account a ON a.id = w.douyin_account_id
    SET w.launch_type = IFNULL(a.launch_type, '')
WHERE w.launch_type = '' OR w.launch_type IS NULL;