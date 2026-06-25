const { query } = require('../models/db')

function randomTrend(days = 7) {
  return Array.from({ length: days }, (_, i) => {
    const d = new Date()
    d.setDate(d.getDate() - (days - 1 - i))
    return { date: d.toISOString().slice(5, 10), value: Math.floor(Math.random() * 50) + 10 }
  })
}

function randomMiniSpark() {
  return Array.from({ length: 12 }, () => (Math.random() * 100).toFixed(1))
}

exports.stats = async (req, res) => {
  const today = new Date().toISOString().slice(0, 10)

  const [[customers], [opportunities], [orders], [deals], [todayOrders], [sources], [stages], [topCustomers]] = await Promise.all([
    query('SELECT COUNT(*) AS total FROM customers'),
    query('SELECT COUNT(*) AS total FROM opportunities'),
    query('SELECT COUNT(*) AS total FROM orders'),
    query("SELECT COUNT(*) AS total FROM opportunities WHERE stage = '赢单'"),
    query('SELECT COUNT(*) AS total FROM orders WHERE order_date = ?', [today]),
    query('SELECT source AS name, COUNT(*) AS value FROM customers GROUP BY source'),
    query('SELECT stage AS name, COUNT(*) AS value FROM opportunities GROUP BY stage'),
    query('SELECT c.name, SUM(o.actual_amount) AS value FROM orders o JOIN customers c ON o.customer_id = c.id GROUP BY o.customer_id ORDER BY value DESC LIMIT 5')
  ])

  const amountRows = await query('SELECT SUM(actual_amount) AS total FROM orders WHERE status != "已取消"')

  res.json({
    code: 0,
    data: {
      totalCustomers: customers.total,
      totalOpportunities: opportunities.total,
      totalOrders: orders.total,
      totalAmount: amountRows[0].total || 0,
      deals: deals.total,
      todayOrders: todayOrders.total,
      customerTrend: randomTrend(),
      orderTrend: randomTrend(),
      amountTrend: randomTrend(),
      sources,
      stages,
      channelData: [
        { name: '展会现场', value: 3245.21 },
        { name: '线上商城', value: 2187.64 },
        { name: '代理分销', value: 1536.88 },
        { name: '企业直销', value: 1021.43 },
        { name: '其他渠道', value: 764.16 }
      ],
      topExhibitions: [
        { name: '智能制造博览会', value: 1236.52, ratio: 14.1 },
        { name: '医疗健康展', value: 1021.34, ratio: 11.7 },
        { name: '消费电子展', value: 986.71, ratio: 11.3 },
        { name: '新能源汽车展', value: 862.15, ratio: 9.8 },
        { name: '全球供应链展', value: 754.16, ratio: 8.6 }
      ],
      topCustomers: topCustomers.map(i => ({ name: i.name, value: i.value })),
      keyMetrics: [
        { label: '新客数', value: 5678, change: '+12.5', spark: randomMiniSpark() },
        { label: '复购率', value: '27.3%', change: '+1.8pt', spark: randomMiniSpark() },
        { label: '退款金额', value: '186,542', change: '-5.6%', spark: randomMiniSpark() },
        { label: '毛利率', value: '45.7%', change: '+0.9pt', spark: randomMiniSpark() },
        { label: '库存周转率', value: '8.2', change: '+0.3', spark: randomMiniSpark() },
        { label: '平均发货时效', value: '1.3天', change: '-0.1', spark: randomMiniSpark() }
      ],
      salesRank: [
        { name: '张伟', value: 128 },
        { name: '李娜', value: 105 },
        { name: '王强', value: 88 },
        { name: '刘洋', value: 72 },
        { name: '陈静', value: 65 }
      ]
    },
    message: 'ok'
  })
}
