-- hytf-crm 数据库初始化脚本（生产环境用；开发环境应用启动会自动建表）
CREATE DATABASE IF NOT EXISTS hytf_crm DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hytf_crm;

CREATE TABLE IF NOT EXISTS t_admin_user (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  real_name VARCHAR(50) DEFAULT '',
  role VARCHAR(20) DEFAULT 'admin',
  is_active TINYINT(1) DEFAULT 1,
  last_login_at DATETIME NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS t_customer (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_uid VARCHAR(10) NOT NULL UNIQUE,
  customer_name VARCHAR(50) NOT NULL,
  contact_name VARCHAR(50) DEFAULT '',
  phone VARCHAR(20) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  is_active TINYINT(1) DEFAULT 1,
  remark VARCHAR(255) DEFAULT '',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS t_douyin_account (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  douyin_id VARCHAR(50) NOT NULL UNIQUE,
  douyin_name VARCHAR(50) DEFAULT '',
  auto_code VARCHAR(6) NOT NULL UNIQUE,
  nickname VARCHAR(20) DEFAULT '',
  recharge_amount DECIMAL(12,2) NOT NULL,
  balance DECIMAL(12,2) NOT NULL DEFAULT 0,
  tier ENUM('A','B','C') NULL DEFAULT NULL,
  tier_daily_budget INT NOT NULL DEFAULT 0,
  launch_at DATETIME NULL,
  auth_start_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  auth_end_at DATETIME NULL,
  status ENUM('NORMAL','DISABLED') DEFAULT 'NORMAL',
  remark VARCHAR(255) DEFAULT '',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_customer (customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS t_finance_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  douyin_account_id INT NOT NULL,
  change_type ENUM('RECHARGE','CONSUME','REFUND','ADJUST') NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  balance_after DECIMAL(12,2) NOT NULL,
  stat_date DATETIME NOT NULL,
  remark VARCHAR(255) DEFAULT '',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_customer (customer_id),
  INDEX idx_account (douyin_account_id),
  INDEX idx_stat_date (stat_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS t_invoice (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NULL,
  customer_name VARCHAR(50) DEFAULT '',
  douyin_id VARCHAR(50) DEFAULT '',
  amount DECIMAL(12,2) NOT NULL,
  status ENUM('PENDING','PROCESSED') DEFAULT 'PENDING',
  invoice_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  processed_at DATETIME NULL,
  remark VARCHAR(255) DEFAULT '',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_customer (customer_id),
  INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 增量更新（已有环境手动执行一次）：
-- ALTER TABLE t_douyin_account MODIFY COLUMN tier ENUM('A','B','C') NULL DEFAULT NULL;
-- ALTER TABLE t_douyin_account MODIFY COLUMN tier_daily_budget INT NOT NULL DEFAULT 0;
-- ALTER TABLE t_douyin_account ADD COLUMN launch_at DATETIME NULL AFTER tier_daily_budget;
-- ============================================================

-- ============================================================
-- 增量更新（已有环境手动执行一次，服务器已执行过可跳过）：
-- ALTER TABLE t_invoice ADD COLUMN douyin_id VARCHAR(50) DEFAULT '' AFTER customer_name;
-- ============================================================
