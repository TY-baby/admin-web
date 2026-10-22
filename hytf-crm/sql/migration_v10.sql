-- hytf-crm/sql/migration_v10.sql
-- V10: 网文推广网址访问计数表
CREATE TABLE IF NOT EXISTS t_novel_promo (
                                             id INT AUTO_INCREMENT PRIMARY KEY,
                                             code VARCHAR(20) NOT NULL COMMENT '网址码(#/book/xxx)',
    customer_id INT NOT NULL DEFAULT 0,
    account_id INT NOT NULL DEFAULT 0,
    platform_code VARCHAR(30) NOT NULL DEFAULT '',
    promo_content VARCHAR(20) NOT NULL DEFAULT '' COMMENT '工会宣传/招聘宣传',
    tier VARCHAR(1) NOT NULL DEFAULT 'A',
    base_reads INT NOT NULL DEFAULT 0 COMMENT '生成时的基础阅读量',
    visits INT NOT NULL DEFAULT 0 COMMENT '访问累计次数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_novel_promo_code (code),
    KEY idx_novel_promo_customer (customer_id),
    KEY idx_novel_promo_account (account_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='网文推广网址与访问计数';