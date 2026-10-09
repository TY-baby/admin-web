-- ================================================================
-- hytf-crm V4 迁移：RBAC菜单权限 + 操作日志表
-- 生产执行一次：
--   sudo docker exec -i hytf-mysql mysql -uroot -phytf_root_2026 hytf_crm < hytf-crm/sql/migration_v4.sql
-- ================================================================
USE hytf_crm;

-- 1. t_admin_user 增加 menus 字段（幂等：已存在则跳过，避免 Duplicate column 中断脚本）
SET @col_exists = (SELECT COUNT(*) FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = 'hytf_crm' AND TABLE_NAME = 't_admin_user' AND COLUMN_NAME = 'menus');
SET @ddl = IF(@col_exists = 0,
  'ALTER TABLE t_admin_user ADD COLUMN menus VARCHAR(255) NOT NULL DEFAULT '''' AFTER role',
  'SELECT ''menus column already exists'' AS msg');
PREPARE stmt FROM @ddl; EXECUTE stmt; DEALLOCATE PREPARE stmt;

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

-- 3. 角色归位：admin 降为业务管理员（无系统菜单），yy 为唯一超管
UPDATE t_admin_user SET role='admin' WHERE username='admin';
UPDATE t_admin_user SET role='super' WHERE username='yy';
