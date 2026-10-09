-- ================================================================
-- hytf-crm V4 迁移：RBAC菜单权限 + 操作日志表
-- 生产执行一次：
--   sudo docker exec -i hytf-mysql mysql -uroot -phytf_root_2026 hytf_crm < hytf-crm/sql/migration_v4.sql
-- ================================================================
USE hytf_crm;

-- 1. t_admin_user 增加 menus 字段（普通用户可见菜单，逗号分隔；super 忽略此字段）
ALTER TABLE t_admin_user ADD COLUMN menus VARCHAR(255) NOT NULL DEFAULT '' AFTER role;

-- 2. 操作日志表
CREATE TABLE IF NOT EXISTS t_operation_log (
                                               id INT AUTO_INCREMENT PRIMARY KEY,
                                               username VARCHAR(50) NOT NULL DEFAULT '',
    role VARCHAR(20) NOT NULL DEFAULT '',
    action VARCHAR(50) NOT NULL DEFAULT '',
    method VARCHAR(10) NOT NULL DEFAULT '',
    path VARCHAR(255) NOT NULL DEFAULT '',
    ip VARCHAR(64) NOT NULL DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_log_username (username),
    INDEX idx_log_created (created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 说明：yy 账号（密码 123456，role=super）由后端启动时自动引导创建，无需 SQL 插入。