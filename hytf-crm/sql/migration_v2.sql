-- ================================================================
-- hytf-crm V2 增量迁移脚本（平台化 + 直播曝光度 + 出款管理）
-- 生产环境执行一次即可
-- ================================================================
USE hytf_crm;

-- 1. t_douyin_account 增加平台/投放类型/日预算/曝光度字段
ALTER TABLE t_douyin_account ADD COLUMN platform_code VARCHAR(30) NOT NULL DEFAULT 'douyin' AFTER customer_id;
ALTER TABLE t_douyin_account ADD COLUMN launch_type ENUM('FIRST_CHARGE','EXPOSURE') NULL DEFAULT NULL AFTER tier_daily_budget;
ALTER TABLE t_douyin_account ADD COLUMN daily_budget DECIMAL(12,2) NOT NULL DEFAULT 0 AFTER launch_type;
ALTER TABLE t_douyin_account ADD COLUMN launch_consumed DECIMAL(12,2) NOT NULL DEFAULT 0 AFTER daily_budget;
ALTER TABLE t_douyin_account ADD COLUMN exposure_1h INT NOT NULL DEFAULT 0 AFTER launch_consumed;

-- 2. 删除旧的 douyin_id UNIQUE 约束，改为 (platform_code, douyin_id) 联合唯一
-- 注意：旧约束名可能为 douyin_id，请确认后执行
ALTER TABLE t_douyin_account DROP INDEX douyin_id;
ALTER TABLE t_douyin_account ADD UNIQUE KEY uk_platform_douyin (platform_code, douyin_id);

-- 3. 创建平台表
CREATE TABLE IF NOT EXISTS t_platform (
                                          id INT AUTO_INCREMENT PRIMARY KEY,
                                          code VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    sort INT NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO t_platform (code, name, sort) VALUES
 ('yingke', '映客', 1),
 ('qiyin', '栖音', 2),
 ('bilibili', '哔哩哔哩', 3),
 ('liujianfang', '六间房', 4);

-- 4. 创建出款管理表
CREATE TABLE IF NOT EXISTS t_withdraw (
                                          id INT AUTO_INCREMENT PRIMARY KEY,
                                          name VARCHAR(50) NOT NULL,
    pay_date DATE NOT NULL,
    id_count INT NOT NULL DEFAULT 0,
    payable_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    remark VARCHAR(255) DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_pay_date (pay_date)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. 已有投放数据兼容：将已投放的记录标记为首充
UPDATE t_douyin_account SET launch_type = 'FIRST_CHARGE' WHERE tier IS NOT NULL AND launch_at IS NOT NULL AND launch_type IS NULL;