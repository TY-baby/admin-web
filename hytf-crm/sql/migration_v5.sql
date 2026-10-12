-- ================================================================
-- hytf-crm V5 迁移：出款管理重构 + 打款对象表 + 平台修正 + 快手
-- 生产执行一次：
--   sudo docker exec -i hytf-mysql mysql -uroot -phytf_root_2026 hytf_crm < hytf-crm/sql/migration_v5.sql
-- ================================================================
USE hytf_crm;
SET NAMES utf8mb4;

-- 1. 修正平台名称（哔哩哔哩可能被误改），新增快手
UPDATE t_platform SET name='哔哩哔哩', sort=3 WHERE code='bilibili';
UPDATE t_platform SET name='映客', sort=1 WHERE code='yingke';
UPDATE t_platform SET name='栖音', sort=2 WHERE code='qiyin';
UPDATE t_platform SET name='六间房', sort=4 WHERE code='liujianfang';
INSERT IGNORE INTO t_platform (code, name, sort) VALUES ('kuaishou', '快手', 5);

-- 2. 创建打款对象表
CREATE TABLE IF NOT EXISTS t_payee (
                                       id INT AUTO_INCREMENT PRIMARY KEY,
                                       card_no VARCHAR(50) NOT NULL UNIQUE,
    bank_name VARCHAR(100) NOT NULL DEFAULT '',
    holder_name VARCHAR(50) NOT NULL,
    display_name VARCHAR(60) NOT NULL,
    sort INT NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 初始化打款对象数据（来源 pay_list.txt）
INSERT IGNORE INTO t_payee (card_no, bank_name, holder_name, display_name, sort) VALUES
('6215340302519420878', '中国建设银行股份有限公司盐亭支行', '钟淑含', '钟淑含1', 0),
('6214673610003763094', '中国建设银行股份有限公司绵阳安州支行', '钟淑含', '钟淑含2', 1),
('6217003610004760309', '中国建设银行股份有限公司绵阳安州支行', '刘川', '刘川', 2),
('6213360489990777577', '农行绵阳花荄支行', '吴娟', '吴娟', 3),
('6222621080001934822', '交通银行济宁开发区支行', '刘保全', '刘保全', 4),
('6212261610014315340', '工商银行临沂市沂水县支行', '尹永良', '尹永良', 5),
('6214838881080628', '招商银行', '海日', '海日', 6),
('6213360489991534274', '无', '谭春蓉', '谭春蓉', 7),
('6217003610011160535', '盐亭支行', '李文杰', '李文杰', 8);

-- 4. 重建出款管理表（删除旧结构，创建新结构）
DROP TABLE IF EXISTS t_withdraw;
CREATE TABLE t_withdraw (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            payee_id INT NOT NULL,
                            payee_card_no VARCHAR(50) NOT NULL DEFAULT '',
                            payee_bank_name VARCHAR(100) NOT NULL DEFAULT '',
                            payee_holder_name VARCHAR(60) NOT NULL DEFAULT '',
                            customer_id INT NOT NULL,
                            customer_name VARCHAR(100) NOT NULL DEFAULT '',
                            douyin_account_id INT NOT NULL,
                            douyin_id VARCHAR(50) NOT NULL DEFAULT '',
                            douyin_name VARCHAR(50) NOT NULL DEFAULT '',
                            generated_count INT NOT NULL DEFAULT 0,
                            payable_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
                            remark VARCHAR(255) NOT NULL DEFAULT '',
                            operator VARCHAR(50) NOT NULL DEFAULT '',
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                            INDEX idx_payee (payee_id),
                            INDEX idx_customer (customer_id),
                            INDEX idx_account (douyin_account_id),
                            INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;