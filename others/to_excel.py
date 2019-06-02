import codecs
import xlwt
from datetime import datetime

TRADE_TYPE_MAP = {
    '000': '综合记账', '001': '冲正',
    '002': '结息', '003': '分润', '004': '内部转账', '005': '批量内部转账', '006': '人工调账',
    '007': '充值', '008': '提现', '009': '余额支付', '010': '退款余额', '300': '手续费结算', '301': '支付通道出账结算',
    '302': '支付通道入账结算', '303': '主动对账充值', '304': '主动对账提现', '305': '后管主动对账', '501': '营销账户充值',
    '502': '营销账户提现', '503': '营销账户充值结算', '504': '营销账户提现结算', '507': '他行来账', '999': '其他'
}
TRAGE_STATUS = {
    'Y': '已撤销/冲正',
    'N': '正常交易'
}


def write_excel():
    f = xlwt.Workbook()  # 创建工作簿

    '''
    创建第一个sheet:
      sheet1
    '''
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'记账交易日记号', u'渠道ID', u'交易类型', u'交易日期', u'交易时间', u'入账日期', u'交易流水号', u'冲正,撤销标志', u'电子账号', u'对手交易账号',
            u'交易金额符号', u'交易金额', u'交易后余额', u'交易描述']

    # 生成第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i])

    with codecs.open(r'C:\test\download\20190309/NEWALEVE50016006-20190308', 'rb',
                     encoding='utf-8') as fp:
        count = 1
        for each in fp.readlines():
            rows = each.split('|')[:-1]
            rows[2] = TRADE_TYPE_MAP.get(rows[2], rows[2])
            rows[3] = datetime.strftime(datetime.strptime(rows[3], '%Y%m%d'), '%Y-%m-%d')
            rows[4] = datetime.strftime(datetime.strptime(rows[4], '%H%M%S'), '%H:%M:%S')
            rows[5] = datetime.strftime(datetime.strptime(rows[5], '%Y%m%d'), '%Y-%m-%d')
            rows[7] = TRAGE_STATUS.get(rows[7], rows[7])
            count += 1
            for j in range(0, len(rows)):
                sheet1.write(count, j, rows[j])

    f.save(r'C:\test\demo1.xls')  # 保存文件


write_excel()
