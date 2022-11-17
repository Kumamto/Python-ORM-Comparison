import os
import csv
import time

import numpy as np
from memory_profiler import memory_usage
from django.http import HttpResponse
from django.db.models import Q, F, Count, Avg, Func
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from testdb.models import Items1, Stocks1, Warehouses1

class Round2(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s::numeric, 2)"

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

def query1():
    count = int(os.environ.get("ITERATIONS", "1000"))
    latency_list = []
    for i in range(count):
        start = time.time()
        res = Items1.objects.all()
        now = time.time()
        latency_list.append(now - start)
    output = calculation(1, count, latency_list)

    return output

def query2():
    count = int(os.environ.get("ITERATIONS", "1000"))
    latency_list = []
    for i in range(count):
        start = time.time()
        res = Stocks1.objects.filter(Q(s_qty__gt=50) & Q(w=54)).all()
        now = time.time()
        latency_list.append(now - start)
    output = calculation(2, count, latency_list)
    return output

def query3():
    count = int(os.environ.get("ITERATIONS", "1000"))
    latency_list = []
    for i in range(count):
        start = time.time()
        res = Items1.objects.filter(i_price__gt=99).all()
        now = time.time()
        latency_list.append(now - start)
    output = calculation(3, count, latency_list)
    return output

def query4():
    count = int(os.environ.get("ITERATIONS", "1000"))
    latency_list = []
    for i in range(count):
        start = time.time()
        res = Items1.objects.filter(Q(stocks1__w_id=54)&Q(stocks1__s_qty__gt=50)).values('i_name')
        now = time.time()
        latency_list.append(now - start)
    output = calculation(4, count, latency_list)
    return output

def query5():
    count = int(os.environ.get("ITERATIONS", "1000"))
    latency_list = []
    for i in range(count):
        start = time.time()
        res = Items1.objects.filter(i_price=100).all()
        now = time.time()
        latency_list.append(now - start)
    output = calculation(5, count, latency_list)
    return output

def query6():
    count = int(os.environ.get("ITERATIONS", "1000"))
    latency_list = []
    for i in range(count):
        start = time.time()
        res = Items1.objects.filter(stocks1__w__gt=0).values('stocks1__w').annotate(Count('stocks1__w'), avg = Round2(Avg('i_price')))
        now = time.time()
        latency_list.append(now - start)
    output = calculation(6, count, latency_list)
    return output

#Very slow since use raw sql
def query7():
    count = int(os.environ.get("ITERATIONS", "10"))
    latency_list = []
    for i in range(count):
        start = time.time()
        mid = Items1.objects.filter(Q(stocks1__w__gt=0)).values('i_id', 'i_name').annotate(
            rank=Window(expression=RowNumber(), partition_by=[F('stocks1__w')]))
        sql, params = mid.query.sql_with_params()
        mid_filtered = mid.raw(f"SELECT i_id, i_name FROM ({sql}) t WHERE rank = 1", params)
        res = list(mid_filtered)
        now = time.time()
        latency_list.append(now - start)
    output = calculation(7, count, latency_list)
    return output

def query8():
    count = int(os.environ.get("ITERATIONS", "1000"))
    latency_list = []
    for i in range(count):
        start = time.time()
        res = Items1.objects.filter(i_id=5432).update(i_price=10.88)
        now = time.time()
        latency_list.append(now - start)
    output = calculation(8, count, latency_list)
    return output

def query9():
    count = int(os.environ.get("ITERATIONS", "1000"))
    latency_list = []
    for i in range(count):
        start = time.time()
        res = Warehouses1.objects.filter(w_id=17).update(w_name='qwerty', w_street_1='asdfg', w_street_2='hjkl',
                                                  w_city='zxcvb', w_state='BQ')
        now = time.time()
        latency_list.append(now - start)
    output = calculation(9, count, latency_list)
    return output

def query10():
    count = int(os.environ.get("ITERATIONS", "1000"))
    latency_list = []
    for i in range(count):
        start = time.time()
        mid = Stocks1.objects.filter(Q(w=40) & Q(s_qty__gt=90)).only('i')
        Items1.objects.filter(i_id__in=mid).update(i_price=50.12)
        now = time.time()
        latency_list.append(now - start)
    output = calculation(10, count, latency_list)
    return output

#Slow
def query11():
    count = int(os.environ.get("ITERATIONS", "1"))
    latency_list = []
    for i in range(count):
        start = time.time()
        mid = Items1.objects.filter(i_price__gt=98).only('i_id')
        Stocks1.objects.filter(i__in=mid).update(s_qty=1)
        now = time.time()
        latency_list.append(now - start)
    output = calculation(11, count, latency_list)
    return output

def query12():
    count = int(os.environ.get("ITERATIONS", "1"))
    latency_list = []
    for i in range(count):
        start = time.time()
        Stocks1.objects.filter(w=80).delete()
        now = time.time()
        latency_list.append(now - start)
    output = calculation(12, count, latency_list)
    return output

def query13():
    count = int(os.environ.get("ITERATIONS", "1"))
    latency_list = []
    for i in range(count):
        start = time.time()
        Stocks1.objects.filter(i=99).delete()
        now = time.time()
        latency_list.append(now - start)
    output = calculation(13, count, latency_list)
    return output

def query14():
    count = int(os.environ.get("ITERATIONS", "1"))
    latency_list = []
    for i in range(count):
        start = time.time()
        mid_query = Warehouses1.objects.filter(w_state='LQ').only('w_id')
        Stocks1.objects.filter(w__in=mid_query).delete()
        now = time.time()
        latency_list.append(now - start)
    output = calculation(14, count, latency_list)
    return output

def query15():
    latency_list = []
    with open('stock_insert.csv', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = ''.join(lines[i].strip('\n')).split(',')
    count = len(lines)
    for i in range(count):
        warehouse = Warehouses1.objects.get(w_id = int(lines[i][0]))
        item = Items1.objects.get(i_id = int(lines[i][1]))
        start = time.time()
        Stocks1.objects.create(w=warehouse, i=item, s_qty=int(lines[i][2]))
        now = time.time()
        latency_list.append(now - start)
    output = calculation(15, count, latency_list)
    return output

def query16():
    latency_list = []

    with open('stock_insert.csv', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = ''.join(lines[i].strip('\n')).split(',')

    midList = []
    for _ in range(0, len(lines), 1000):
        midList.append(lines[_:_ + 1000])

    stockList = []
    for i in range(10):
        stockList.append([Stocks1(w = Warehouses1.objects.get(w_id = int(j[0])), i = Items1.objects.get(i_id = int(j[1])), s_qty = int(j[2])) for j in midList[i]])

    for i in range(10):
        start = time.time()
        Stocks1.objects.bulk_create(stockList[i])
        now = time.time()
        latency_list.append(now - start)
    output = calculation(16, 10, latency_list)
    return output


def test2(request):
    html_raw = "<html><body>"

    with open('result.csv', 'w') as f:
        csv_write = csv.writer(f)
        csv_head = ['Query index', 'total_latency', 'throughput', 'avr_latency', 'median_latency', 'percentile_95', 'percentile_99']
        csv_write.writerow(csv_head)

    # Try one-to-one insert, then have to reset the stocks1 table to try query16
    for i in range(7, 8):
        html_raw += "<p>Max memory usage for query " + str(i) + " : %s MB</p>"

    html_raw += "</body></html>"

    html = html_raw % (max(memory_usage(query7)))

    return HttpResponse(html)
