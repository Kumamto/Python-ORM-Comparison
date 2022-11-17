import csv
import time
import numpy as np

from memory_profiler import profile
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from tortoise.expressions import Q, Subquery

class Items1(Model):
    i_id = fields.IntField(pk=True)
    i_name = fields.CharField(max_length=50)
    i_price = fields.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        table = 'items1'

    def __str__(self):
        return self.name

class Warehouses1(Model):
    w_id = fields.IntField(pk=True)
    w_name = fields.CharField(max_length=50, blank=True, null=True)
    w_street_1 = fields.CharField(max_length=50, blank=True, null=True)
    w_street_2 = fields.CharField(max_length=50, blank=True, null=True)
    w_city = fields.CharField(max_length=50, blank=True, null=True)
    w_state = fields.CharField(max_length=50, blank=True, null=True)

    class Meta:
        table = 'warehouses1'

    def __str__(self):
        return self.name

class Stocks1(Model):
    w = fields.OneToOneField('models.Warehouses1', pk=True, related_name = 'stocks.wid')
    i = fields.ForeignKeyField('models.Items1', related_name = 'stocks.iid')
    s_qty = fields.SmallIntField(blank=True, null=True)

    class Meta:
        table = 'stocks1'
        unique_together = (('w', 'i'),)

    def __str__(self):
        return self.name

def calculation(i, count, latency_list):
    latency_array = np.array(latency_list)
    total_latency = np.sum(latency_array)  # sec
    throughput = count / total_latency
    avr_latency = np.mean(latency_array) * 1000  # ms
    median_latency = np.median(latency_array) * 1000
    percentile_95 = np.percentile(latency_array, 95) * 1000
    percentile_99 = np.percentile(latency_array, 99) * 1000

    result = [i, total_latency, throughput, avr_latency, median_latency, percentile_95, percentile_99]

    with open('result.csv','a+') as f:
        csv_write = csv.writer(f)
        data_row = result
        csv_write.writerow(data_row)

    return result

@profile(precision=4)
async def run():
    await Tortoise.init(db_url="postgres://postgres:19981209@localhost:5432/django",
                        modules={"models": ["__main__"]})

    with open('result.csv', 'w') as f:
        csv_write = csv.writer(f)
        csv_head = ['Query index', 'total_latency', 'throughput', 'avr_latency', 'median_latency', 'percentile_95', 'percentile_99']
        csv_write.writerow(csv_head)


    # Test1 slow
    latency_list = []
    for i in range(1):
        start = time.time()
        await Items1.all()
        latency_list.append(time.time() - start)
    calculation(1, 1, latency_list)

    # Test2
    latency_list = []
    for i in range(1):
        start = time.time()
        await Stocks1.filter(Q(s_qty__gt=50) & Q(w=54)).all()
        latency_list.append(time.time() - start)
    calculation(2, 1, latency_list)

    # Test3
    latency_list = []
    for i in range(1):
        start = time.time()
        await Items1.filter(i_price__gt=99).all()
        latency_list.append(time.time() - start)
    calculation(3, 1, latency_list)

    # Test5
    latency_list = []
    for i in range(1):
        start = time.time()
        await Items1.filter(i_price=100).all()
        latency_list.append(time.time() - start)
    calculation(5, 1, latency_list)

    # Test8
    latency_list = []
    for i in range(1):
        start = time.time()
        await Items1.filter(i_id=5432).update(i_price=10.88)
        latency_list.append(time.time() - start)
    calculation(8, 1, latency_list)

    # Test9
    latency_list = []
    for i in range(1):
        start = time.time()
        await Warehouses1.filter(w_id=17).update(w_name='qwerty', w_street_1='asdfg', w_street_2='hjkl',
                                                 w_city='zxcvb', w_state='BQ')
        latency_list.append(time.time() - start)
    calculation(9, 1, latency_list)

    # Test10
    latency_list = []
    for i in range(1):
        start = time.time()
        mid = Subquery(Stocks1.filter(Q(w=40) & Q(s_qty__gt=90)).values('i_id'))
        await Items1.filter(i_id__in=mid).update(i_price=50.12)
        latency_list.append(time.time() - start)
    calculation(10, 1, latency_list)

    # Test11
    latency_list = []
    for i in range(1):
        start = time.time()
        mid = Subquery(Items1.filter(i_price__gt=98).values('i_id'))
        await Stocks1.filter(i_id__in=mid).update(s_qty=1)
        latency_list.append(time.time() - start)
    calculation(11, 1, latency_list)

    # Test12
    latency_list = []
    for i in range(1):
        start = time.time()
        await Stocks1.filter(w=80).delete()
        latency_list.append(time.time() - start)
    calculation(12, 1, latency_list)

    # Test13
    latency_list = []
    for i in range(1):
        start = time.time()
        await Stocks1.filter(i=99).delete()
        latency_list.append(time.time() - start)
    calculation(13, 1, latency_list)

    # Test14
    latency_list = []
    for i in range(1):
        start = time.time()
        mid = Subquery(Warehouses1.filter(w_state='LQ').values('w_id'))
        await Stocks1.filter(w_id__in=mid).delete()
        latency_list.append(time.time() - start)
    calculation(14, 1, latency_list)

    # Test15
    latency_list = []
    with open('stock_insert.csv', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = ''.join(lines[i].strip('\n')).split(',')
    count = len(lines)

    for i in range(count):
        start = time.time()
        warehouse = await Warehouses1.get(w_id=int(lines[i][0]))
        item = await Items1.get(i_id=int(lines[i][1]))
        await Stocks1.create(w=warehouse, i=item, s_qty=int(lines[i][2]))
        latency_list.append(time.time() - start)
    calculation(15, count, latency_list)

    '''
    # Test16
    latency_list = []
    with open('stock_insert.csv', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = ''.join(lines[i].strip('\n')).split(',')

    midList = []
    for _ in range(0, len(lines), 1000):
        midList.append(lines[_:_ + 1000])

    for i in range(10):
        start = time.time()
        Stocks1.bulk_create([Stocks1(w=await Warehouses1.get(w_id=int(j[0])),
                     i=await Items1.get(i_id=int(j[1])), s_qty=int(j[2])) for j in midList[i]])
        latency_list.append(time.time() - start)
    calculation(16, 10, latency_list)
    '''

if __name__ == '__main__':
    run_async(run())