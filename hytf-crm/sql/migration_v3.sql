-- ================================================================
-- hytf-crm V3 增量迁移脚本（Phase 1：投放时生成落库 + 出款管理重构 + 类型筛选）
-- 生产环境执行一次即可
-- 执行命令：
--   sudo docker exec -i hytf-mysql mysql -uroot -phytf_root_2026 hytf_crm < hytf-crm/sql/migration_v3.sql
-- ================================================================
USE hytf_crm;

-- 1. t_douyin_account 增加 generated_items 列：存储投放时一次性生成的 ID + 昵称 + 单条值
--    格式：JSON 数组字符串 [{"biz_code":"123456","nickname":"恒耀投手_xxx","value":100}, ...]
--    首充类型：value = 单条消耗金额；曝光度类型：value = 单条 1h 曝光量
ALTER TABLE t_douyin_account ADD COLUMN generated_items TEXT NULL AFTER exposure_1h;

-- 2. 增加索引：按投放类型/投放时间筛选（出款管理 & 用户管理类型筛选需要）
ALTER TABLE t_douyin_account ADD INDEX idx_launch_type (launch_type);
ALTER TABLE t_douyin_account ADD INDEX idx_launch_at (launch_at);

-- 3. 已有历史投放数据的兼容说明：
--    generated_items 为 NULL 时，导出接口自动回退到"实时随机生成"逻辑（不落库），
--    仅新发生的投放会一次性落库，避免历史数据大批量回填风险。