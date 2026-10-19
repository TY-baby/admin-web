-- hytf-crm/sql/migration_v7.sql
-- V7: 出款管理结算日期/热度/平台字段；开票平台字段
ALTER TABLE t_withdraw
    ADD COLUMN heat_value INT NOT NULL DEFAULT 0 AFTER generated_count,
    ADD COLUMN settle_date DATE NULL AFTER payable_amount,
    ADD COLUMN platform_code VARCHAR(30) NOT NULL DEFAULT '' AFTER douyin_name;

CREATE INDEX idx_withdraw_settle_date ON t_withdraw (settle_date);
CREATE INDEX idx_withdraw_platform ON t_withdraw (platform_code);

UPDATE t_withdraw w
    JOIN t_douyin_account a ON a.id = w.douyin_account_id
    SET w.platform_code = IFNULL(a.platform_code, '')
WHERE w.platform_code = '' OR w.platform_code IS NULL;

UPDATE t_withdraw SET settle_date = DATE(created_at) WHERE settle_date IS NULL;

ALTER TABLE t_invoice
    ADD COLUMN platform_code VARCHAR(30) NOT NULL DEFAULT '' AFTER douyin_id;

UPDATE t_invoice i
    JOIN t_douyin_account a ON a.douyin_id = i.douyin_id AND a.customer_id = i.customer_id
    SET i.platform_code = IFNULL(a.platform_code, '')
WHERE i.platform_code = '' OR i.platform_code IS NULL;