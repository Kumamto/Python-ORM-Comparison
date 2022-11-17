import time
import os
from django.db import connection
from testdb.models import Items
from memory_profiler import profile


def main():
    """Run administrative tasks."""
    def test115():
        with open('stock_insert.csv', encoding='utf-8') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = ''.join(lines[i].strip('\n')).split(',')
            start = time.time()
            for i in range(len(lines)):
                sql = "INSERT INTO stocks VALUES (" + lines[i][0] + ", " + lines[i][1] + ", " + lines[i][2] + ");"
                c.execute(sql)
            now = time.time()
            print(f"Time Consumption For Query 15 is {(now - start) / len(lines)}\n")
            return



    # Test table with constraints

    QuerySet1 = [
        "select * from items1;",
        "select * from stocks1 where w_id=54 and s_qty>50;",
        "select * from items1 where i_price>99;",
        "select i_name from (stocks s inner join items i on s.i_id=i.i_id) t where w_id=54 and s_qty>50;",
        "select * from items1 where i_id=100;",
        "select t.w_id,round(avg(t.i_price)::numeric,2),count(*) from (select * from stocks1 s inner join items1 i on s.i_id=i.i_id) t group by t.w_id;",
        "select tmp.i_name from (select t.i_name, row_number() over(partition by t.w_id) r from(select * from stocks1 s inner join items1 i on s.i_id=i.i_id) t) tmp where tmp.r=1;",
        "update items1 set i_price=10.88 where i_id=5432;",
        "update warehouses1 set w_name='qwerty', w_street_1='asdfg', w_street_2='hjkl', w_city='zxcvb', w_state='BQ' where w_id=17;",
        "update items1 set i_price=50.12 where i_id in (select i_id from stocks1 where w_id=40 and s_qty>90);",
        "update stocks1 set s_qty=1 where i_id in (select i_id from items1 where i_price>98);",
        "delete from stocks1 where w_id=80;",
        "delete from stocks1 where i_id=99;",
        "delete from stocks1 where w_id in (select w_id from warehouses1 where w_state='LQ')"
    ]

    # Test1
    @profile(precision=4)
    def test21():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[0])
            c.fetchall()
        now = time.time()
        print(f"Time Consumption For Query 1 is {(now - start) / count}\n")
        return

    # Test2
    @profile(precision=4)
    def test22():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[1])
            c.fetchall()
        now = time.time()
        print(f"Time Consumption For Query 2 is {(now - start) / count}\n")
        return

    # Test3
    @profile(precision=4)
    def test23():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[2])
            c.fetchall()
        now = time.time()
        print(f"Time Consumption For Query 3 is {(now - start) / count}\n")
        return

    # Test4
    @profile(precision=4)
    def test24():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[3])
            c.fetchall()
        now = time.time()
        print(f"Time Consumption For Query 4 is {(now - start) / count}\n")
        return

    # Test5
    @profile(precision=4)
    def test25():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[4])
            c.fetchall()
        now = time.time()
        print(f"Time Consumption For Query 5 is {(now - start) / count}\n")
        return

    # Test6
    @profile(precision=4)
    def test26():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[5])
            c.fetchall()
        now = time.time()
        print(f"Time Consumption For Query 6 is {(now - start) / count}\n")
        return

    # Test7
    @profile(precision=4)
    def test27():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[6])
            c.fetchall()
        now = time.time()
        print(f"Time Consumption For Query 7 is {(now - start) / count}\n")
        return

    # Test8
    @profile(precision=4)
    def test28():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[7])
        now = time.time()
        print(f"Time Consumption For Query 8 is {(now - start) / count}\n")
        return

    # Test9
    @profile(precision=4)
    def test29():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[8])
        now = time.time()
        print(f"Time Consumption For Query 9 is {(now - start) / count}\n")
        return

    # Test10
    @profile(precision=4)
    def test210():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[9])
        now = time.time()
        print(f"Time Consumption For Query 10 is {(now - start) / count}\n")
        return

    # Test11
    @profile(precision=4)
    def test211():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[10])
        now = time.time()
        print(f"Time Consumption For Query 11 is {(now - start) / count}\n")
        return

    # Test12
    @profile(precision=4)
    def test212():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[11])
        now = time.time()
        print(f"Time Consumption For Query 12 is {(now - start) / count}\n")
        return

    # Test13
    @profile(precision=4)
    def test213():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[12])
        now = time.time()
        print(f"Time Consumption For Query 13 is {(now - start) / count}\n")
        return

    # Test14
    @profile(precision=4)
    def test214():
        start = time.time()
        for i in range(count):
            c.execute(QuerySet1[13])
        now = time.time()
        print(f"Time Consumption For Query 14 is {(now - start) / count}\n")
        return

    # Test15
    def test215():
        with open('stock_insert.csv', encoding='utf-8') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = ''.join(lines[i].strip('\n')).split(',')
            start = time.time()
            for i in range(len(lines)):
                sql = "INSERT INTO stocks1 VALUES (" + lines[i][0] + ", " + lines[i][1] + ", " + lines[i][2] + ");"
                c.execute(sql)
            now = time.time()
            print(f"Time Consumption For Query 15 is {(now - start) / len(lines)}\n")
            return

    print("——————————Without Constraints——————————\n")
    test11()
    test12()
    test13()
    test14()
    test15()
    test16()
    test17()
    test18()
    test19()
    test110()
    test111()
    test112()
    test113()
    test114()
    test115()

    print("——————————With Constraints——————————\n")
    test21()
    test22()
    test23()
    test24()
    test25()
    test26()
    test27()
    test28()
    test29()
    test210()
    test211()
    test212()
    test213()
    test214()
    test215()



if __name__ == '__main__':
    main()


