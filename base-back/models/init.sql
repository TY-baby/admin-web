
CREATE DATABASE IF NOT EXISTS base_room CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE base_room;

-- 部门表
CREATE TABLE IF NOT EXISTS departments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL COMMENT '部门名称',
  parent_id INT DEFAULT 0 COMMENT '父部门ID',
  leader_id INT DEFAULT 0 COMMENT '部门负责人ID',
  sort INT DEFAULT 0,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='部门表';

-- 用户表
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
  password VARCHAR(100) NOT NULL COMMENT '密码',
  real_name VARCHAR(50) DEFAULT '' COMMENT '真实姓名',
  phone VARCHAR(20) DEFAULT '' COMMENT '电话',
  email VARCHAR(100) DEFAULT '' COMMENT '邮箱',
  avatar VARCHAR(255) DEFAULT '' COMMENT '头像',
  dept_id INT DEFAULT 0 COMMENT '部门ID',
  role_id INT DEFAULT 0 COMMENT '角色ID',
  status TINYINT DEFAULT 1 COMMENT '状态 1启用 0禁用',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_dept (dept_id),
  INDEX idx_role (role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 角色表
CREATE TABLE IF NOT EXISTS roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL COMMENT '角色名称',
  code VARCHAR(50) DEFAULT '' COMMENT '角色编码',
  permissions TEXT COMMENT '权限JSON',
  remark VARCHAR(255) DEFAULT '',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色表';

-- 字典表
CREATE TABLE IF NOT EXISTS sys_dicts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  dict_type VARCHAR(50) NOT NULL COMMENT '字典类型',
  dict_code VARCHAR(50) NOT NULL COMMENT '字典编码',
  dict_label VARCHAR(100) NOT NULL COMMENT '字典标签',
  dict_value VARCHAR(100) NOT NULL COMMENT '字典值',
  sort INT DEFAULT 0,
  status TINYINT DEFAULT 1,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='字典表';

-- 客户表
CREATE TABLE IF NOT EXISTS customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_no VARCHAR(50) DEFAULT '' COMMENT '客户编号',
  name VARCHAR(100) NOT NULL COMMENT '客户名称',
  phone VARCHAR(20) DEFAULT '' COMMENT '电话',
  email VARCHAR(100) DEFAULT '' COMMENT '邮箱',
  company VARCHAR(100) DEFAULT '' COMMENT '公司名称',
  industry VARCHAR(50) DEFAULT '' COMMENT '所属行业',
  source VARCHAR(50) DEFAULT '' COMMENT '客户来源',
  status VARCHAR(20) DEFAULT '潜在客户' COMMENT '客户状态',
  level VARCHAR(20) DEFAULT '普通' COMMENT '客户等级',
  owner_id INT DEFAULT 0 COMMENT '归属人ID',
  province VARCHAR(50) DEFAULT '',
  city VARCHAR(50) DEFAULT '',
  district VARCHAR(50) DEFAULT '',
  address VARCHAR(255) DEFAULT '',
  tags VARCHAR(255) DEFAULT '' COMMENT '标签',
  remark TEXT COMMENT '备注',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_owner (owner_id),
  INDEX idx_status (status),
  INDEX idx_level (level),
  INDEX idx_source (source)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户表';

-- 客户联系人表
CREATE TABLE IF NOT EXISTS customer_contacts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL COMMENT '客户ID',
  name VARCHAR(50) NOT NULL COMMENT '联系人姓名',
  phone VARCHAR(20) DEFAULT '',
  email VARCHAR(100) DEFAULT '',
  position VARCHAR(50) DEFAULT '' COMMENT '职位',
  is_main TINYINT DEFAULT 0 COMMENT '是否主联系人',
  remark VARCHAR(255) DEFAULT '',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_customer (customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户联系人表';

-- 标签表
CREATE TABLE IF NOT EXISTS tags (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL COMMENT '标签名',
  color VARCHAR(20) DEFAULT '#409EFF' COMMENT '颜色',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='标签表';

-- 客户标签关联表
CREATE TABLE IF NOT EXISTS customer_tags (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  tag_id INT NOT NULL,
  UNIQUE KEY uk_customer_tag (customer_id, tag_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户标签关联表';

-- 商机表
CREATE TABLE IF NOT EXISTS opportunities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL COMMENT '客户ID',
  title VARCHAR(200) NOT NULL COMMENT '商机标题',
  amount DECIMAL(15,2) DEFAULT 0 COMMENT '预计金额',
  stage VARCHAR(50) DEFAULT '初步接触' COMMENT '阶段',
  probability INT DEFAULT 10 COMMENT '赢单概率%',
  expected_close_date DATE DEFAULT NULL COMMENT '预计成交日期',
  owner_id INT DEFAULT 0 COMMENT '负责人',
  source VARCHAR(50) DEFAULT '' COMMENT '商机来源',
  competitor VARCHAR(100) DEFAULT '' COMMENT '竞争对手',
  status VARCHAR(20) DEFAULT '跟进中' COMMENT '状态',
  remark TEXT COMMENT '备注',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_customer (customer_id),
  INDEX idx_owner (owner_id),
  INDEX idx_stage (stage)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商机表';

-- 商机跟进表
CREATE TABLE IF NOT EXISTS opportunity_follows (
  id INT AUTO_INCREMENT PRIMARY KEY,
  opportunity_id INT NOT NULL,
  follow_type VARCHAR(50) DEFAULT '电话' COMMENT '跟进方式',
  content TEXT COMMENT '跟进内容',
  stage VARCHAR(50) DEFAULT '' COMMENT '当前阶段',
  owner_id INT DEFAULT 0,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_opportunity (opportunity_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商机跟进表';

-- 产品表
CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) DEFAULT '' COMMENT '产品编码',
  name VARCHAR(100) NOT NULL COMMENT '产品名称',
  category VARCHAR(50) DEFAULT '' COMMENT '分类',
  price DECIMAL(15,2) DEFAULT 0 COMMENT '销售价格',
  cost DECIMAL(15,2) DEFAULT 0 COMMENT '成本价',
  stock INT DEFAULT 0 COMMENT '库存',
  unit VARCHAR(20) DEFAULT '件' COMMENT '单位',
  status TINYINT DEFAULT 1 COMMENT '状态',
  remark VARCHAR(255) DEFAULT '',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品表';

-- 订单表
CREATE TABLE IF NOT EXISTS orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_no VARCHAR(50) NOT NULL UNIQUE COMMENT '订单编号',
  customer_id INT NOT NULL COMMENT '客户ID',
  opportunity_id INT DEFAULT 0 COMMENT '关联商机ID',
  amount DECIMAL(15,2) DEFAULT 0 COMMENT '订单金额',
  discount DECIMAL(5,2) DEFAULT 0 COMMENT '折扣',
  actual_amount DECIMAL(15,2) DEFAULT 0 COMMENT '实付金额',
  status VARCHAR(20) DEFAULT '待确认' COMMENT '订单状态',
  pay_status VARCHAR(20) DEFAULT '未付款' COMMENT '付款状态',
  order_date DATE DEFAULT (CURDATE()) COMMENT '订单日期',
  delivery_date DATE DEFAULT NULL COMMENT '交付日期',
  owner_id INT DEFAULT 0 COMMENT '销售人员',
  remark TEXT COMMENT '备注',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_customer (customer_id),
  INDEX idx_owner (owner_id),
  INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 订单明细表
CREATE TABLE IF NOT EXISTS order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  product_name VARCHAR(100) DEFAULT '',
  quantity INT DEFAULT 1,
  unit_price DECIMAL(15,2) DEFAULT 0,
  total_price DECIMAL(15,2) DEFAULT 0,
  INDEX idx_order (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单明细表';

-- 跟进/消化记录表
CREATE TABLE IF NOT EXISTS follows (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL COMMENT '客户ID',
  follow_type VARCHAR(50) DEFAULT '电话' COMMENT '跟进方式',
  content TEXT COMMENT '跟进内容',
  next_follow_time DATETIME DEFAULT NULL COMMENT '下次跟进时间',
  owner_id INT DEFAULT 0 COMMENT '跟进人',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_customer (customer_id),
  INDEX idx_owner (owner_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='跟进记录表';

-- 回访记录表
CREATE TABLE IF NOT EXISTS visits (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  visit_type VARCHAR(50) DEFAULT '满意度回访' COMMENT '回访类型',
  content TEXT COMMENT '回访内容',
  result VARCHAR(255) DEFAULT '' COMMENT '回访结果',
  visit_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  owner_id INT DEFAULT 0,
  INDEX idx_customer (customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='回访记录表';

-- 任务/日程表
CREATE TABLE IF NOT EXISTS tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL COMMENT '任务标题',
  task_type VARCHAR(50) DEFAULT '跟进' COMMENT '任务类型',
  relate_type VARCHAR(50) DEFAULT '' COMMENT '关联类型',
  relate_id INT DEFAULT 0 COMMENT '关联ID',
  due_date DATETIME DEFAULT NULL COMMENT '截止时间',
  status VARCHAR(20) DEFAULT '待处理' COMMENT '状态',
  owner_id INT DEFAULT 0 COMMENT '负责人',
  reminder_time DATETIME DEFAULT NULL COMMENT '提醒时间',
  remark TEXT,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_owner (owner_id),
  INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务日程表';

-- VIP等级表
CREATE TABLE IF NOT EXISTS vip_levels (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL COMMENT '等级名称',
  level INT DEFAULT 1 COMMENT '等级值',
  discount DECIMAL(3,2) DEFAULT 1.00 COMMENT '折扣',
  threshold DECIMAL(15,2) DEFAULT 0 COMMENT '升级门槛',
  privileges TEXT COMMENT '权益说明',
  status TINYINT DEFAULT 1,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='VIP等级表';

-- 客户VIP关系表
CREATE TABLE IF NOT EXISTS customer_vip (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL UNIQUE,
  vip_level_id INT DEFAULT 1,
  points INT DEFAULT 0 COMMENT '积分',
  total_consumption DECIMAL(15,2) DEFAULT 0 COMMENT '累计消费',
  join_date DATE DEFAULT (CURDATE()),
  expire_date DATE DEFAULT NULL,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户VIP关系表';

-- 积分记录表
CREATE TABLE IF NOT EXISTS points_records (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  type VARCHAR(20) DEFAULT 'add' COMMENT 'add/add增加 minus消费',
  points INT DEFAULT 0,
  balance INT DEFAULT 0 COMMENT '变动后余额',
  description VARCHAR(255) DEFAULT '',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_customer (customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分记录表';

-- 流程定义表
CREATE TABLE IF NOT EXISTS workflows (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL COMMENT '流程名称',
  flow_key VARCHAR(50) NOT NULL UNIQUE COMMENT '流程编码',
  version INT DEFAULT 1,
  status TINYINT DEFAULT 1 COMMENT '状态',
  nodes JSON COMMENT '节点配置JSON',
  remark VARCHAR(255) DEFAULT '',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='流程定义表';

-- 流程节点表
CREATE TABLE IF NOT EXISTS workflow_nodes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  workflow_id INT NOT NULL,
  node_id VARCHAR(50) NOT NULL COMMENT '节点ID',
  node_name VARCHAR(100) DEFAULT '' COMMENT '节点名称',
  node_type VARCHAR(50) DEFAULT 'approval' COMMENT '节点类型',
  approvers VARCHAR(255) DEFAULT '' COMMENT '审批人IDs',
  conditions JSON COMMENT '条件JSON',
  next_nodes VARCHAR(255) DEFAULT '' COMMENT '下级节点',
  sort INT DEFAULT 0,
  INDEX idx_workflow (workflow_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='流程节点表';

-- 流程实例表
CREATE TABLE IF NOT EXISTS workflow_instances (
  id INT AUTO_INCREMENT PRIMARY KEY,
  workflow_id INT NOT NULL,
  business_key VARCHAR(100) DEFAULT '' COMMENT '业务标识',
  business_type VARCHAR(50) DEFAULT '' COMMENT '业务类型',
  title VARCHAR(200) DEFAULT '' COMMENT '标题',
  applicant_id INT DEFAULT 0 COMMENT '申请人ID',
  status VARCHAR(20) DEFAULT 'running' COMMENT '状态 running/approved/rejected',
  current_node_id VARCHAR(50) DEFAULT '' COMMENT '当前节点',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_workflow (workflow_id),
  INDEX idx_applicant (applicant_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='流程实例表';

-- 流程审批记录表
CREATE TABLE IF NOT EXISTS workflow_approvals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  instance_id INT NOT NULL,
  node_id VARCHAR(50) DEFAULT '',
  node_name VARCHAR(100) DEFAULT '',
  approver_id INT DEFAULT 0,
  action VARCHAR(20) DEFAULT 'approve' COMMENT 'approve/pass/reject',
  comment VARCHAR(500) DEFAULT '',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_instance (instance_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='流程审批记录表';

-- 通知消息表
CREATE TABLE IF NOT EXISTS notifications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(200) DEFAULT '',
  content TEXT,
  type VARCHAR(50) DEFAULT 'system',
  is_read TINYINT DEFAULT 0,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_user (user_id),
  INDEX idx_read (is_read)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='通知消息表';

-- 初始化基础数据
INSERT INTO departments (name, parent_id, sort) VALUES ('销售部', 0, 1), ('市场部', 0, 2), ('客服部', 0, 3);

INSERT INTO roles (name, code, permissions) VALUES
('超级管理员', 'super_admin', '["*"]'),
('销售经理', 'sales_manager', '["customer:*","opportunity:*","order:*","follow:*","vip:*"]'),
('销售专员', 'sales', '["customer:view","customer:add","opportunity:view","opportunity:add","follow:*"]');

INSERT INTO users (username, password, real_name, phone, dept_id, role_id) VALUES
('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Z5EO', '管理员', '13800138000', 1, 1),
('zhangsan', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Z5EO', '张三', '13800138001', 1, 3),
('lisi', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Z5EO', '李四', '13800138002', 1, 3);

INSERT INTO sys_dicts (dict_type, dict_code, dict_label, dict_value, sort) VALUES
('customer_status', 'potential', '潜在客户', '潜在客户', 1),
('customer_status', 'intention', '意向客户', '意向客户', 2),
('customer_status', 'deal', '成交客户', '成交客户', 3),
('customer_status', 'lost', '流失客户', '流失客户', 4),
('opportunity_stage', 'contact', '初步接触', '初步接触', 1),
('opportunity_stage', 'need', '需求确认', '需求确认', 2),
('opportunity_stage', 'quote', '方案报价', '方案报价', 3),
('opportunity_stage', 'negotiate', '商务谈判', '商务谈判', 4),
('opportunity_stage', 'win', '赢单', '赢单', 5),
('opportunity_stage', 'lose', '输单', '输单', 6),
('order_status', 'pending', '待确认', '待确认', 1),
('order_status', 'confirmed', '已确认', '已确认', 2),
('order_status', 'producing', '生产中', '生产中', 3),
('order_status', 'shipped', '已发货', '已发货', 4),
('order_status', 'completed', '已完成', '已完成', 5),
('order_status', 'cancelled', '已取消', '已取消', 6);

INSERT INTO customers (customer_no, name, phone, company, industry, source, status, level, owner_id, tags) VALUES
('C20260001', '张三科技', '13800138001', '张三科技有限公司', '互联网', '官网', '意向客户', 'A级', 2, '重点,跟进'),
('C20260002', '李四贸易', '13800138002', '李四贸易有限公司', '贸易', '推广', '成交客户', 'B级', 3, '老客户'),
('C20260003', '王五制造', '13800138003', '王五制造有限公司', '制造业', '转介绍', '潜在客户', 'C级', 2, '新线索'),
('C20260004', '赵六金融', '13800138004', '赵六金融服务公司', '金融', '官网', '意向客户', 'A级', 3, '高意向');

INSERT INTO opportunities (customer_id, title, amount, stage, probability, expected_close_date, owner_id, source) VALUES
(1, '张三科技 CRM 系统采购', 150000, '商务谈判', 70, '2026-07-15', 2, '官网'),
(2, '李四贸易年度服务续费', 80000, '赢单', 100, '2026-06-30', 3, '老客户'),
(3, '王五制造 ERP 对接项目', 220000, '需求确认', 40, '2026-08-20', 2, '转介绍'),
(4, '赵六金融数据中台建设', 500000, '方案报价', 50, '2026-08-01', 3, '官网');

INSERT INTO products (code, name, category, price, cost, stock, unit) VALUES
('P001', 'CRM 标准版', '软件', 30000, 5000, 999, '套'),
('P002', 'CRM 高级版', '软件', 60000, 10000, 999, '套'),
('P003', '数据大屏', '软件', 20000, 3000, 999, '套'),
('P004', '实施服务', '服务', 5000, 1000, 999, '人天');

INSERT INTO orders (order_no, customer_id, opportunity_id, amount, actual_amount, status, pay_status, order_date, owner_id) VALUES
('O20260001', 2, 2, 80000, 80000, '已完成', '已付款', '2026-06-20', 3),
('O20260002', 1, 1, 150000, 135000, '待确认', '未付款', '2026-06-22', 2);

INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, total_price) VALUES
(1, 1, 'CRM 标准版', 2, 30000, 60000),
(1, 4, '实施服务', 4, 5000, 20000),
(2, 2, 'CRM 高级版', 2, 60000, 120000),
(2, 3, '数据大屏', 1, 15000, 15000);

INSERT INTO follows (customer_id, follow_type, content, next_follow_time, owner_id) VALUES
(1, '电话', '客户对 CRM 功能比较满意，下周安排 demo', '2026-06-28 10:00:00', 2),
(2, '拜访', '老客户续约沟通，价格已确认', '2026-06-25 14:00:00', 3);

INSERT INTO vip_levels (name, level, discount, threshold, privileges) VALUES
('普通会员', 1, 1.00, 0, '基础服务'),
('银卡会员', 2, 0.95, 10000, '95折优惠+优先客服'),
('金卡会员', 3, 0.90, 50000, '9折优惠+专属客服'),
('钻石会员', 4, 0.85, 100000, '85折优惠+专属顾问');

INSERT INTO customer_vip (customer_id, vip_level_id, points, total_consumption, expire_date) VALUES
(2, 3, 5200, 80000, '2027-06-30'),
(1, 2, 1800, 15000, '2027-06-30');

INSERT INTO workflows (name, flow_key, nodes, remark) VALUES
('折扣审批流程', 'discount_approve', '[{"nodeId":"start","nodeName":"开始","nodeType":"start","nextNodes":["approval1"]},{"nodeId":"approval1","nodeName":"销售经理审批","nodeType":"approval","approvers":[1],"nextNodes":["end"]},{"nodeId":"end","nodeName":"结束","nodeType":"end"}]', '订单折扣超过9折需审批');

INSERT INTO workflow_nodes (workflow_id, node_id, node_name, node_type, approvers, next_nodes, sort) VALUES
(1, 'start', '开始', 'start', '', 'approval1', 1),
(1, 'approval1', '销售经理审批', 'approval', '1', 'end', 2),
(1, 'end', '结束', 'end', '', '', 3);
