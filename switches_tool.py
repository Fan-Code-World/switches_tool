#!/usr/bin/env python
# coding=utf-8
import csv
import re
import os
import sys
import sqlite3
reload(sys)
sys.setdefaultencoding('utf8')

class Switches_tool():
    def switches_dici(self,file_name):  #返回字典
        self.switches_test = {}
        switchesl_file_handle = file(file_name, 'r')
        switches_reader = csv.reader(switchesl_file_handle)
        self.header=next(switches_reader)
        for switches_line in switches_reader:
            host = switches_line[0]
            self.switches_test[host] = {}
            self.switches_test[host]['clss'] = switches_line[1]
            self.switches_test[host]['comment'] = switches_line[2:]
              
        switchesl_file_handle.close()
        return self.switches_test
    
    def key_id(self,comment_str):      #返回key值
        conn = sqlite3.connect('/usr/local/zddi/grid.db')
        c=conn.cursor()
        cursor=c.execute("select id,display_name,type from attrsmap")
        for row in cursor:
            if  (row[1] == comment_str) :
                return (row[0])
        conn.close()

    def key_str(self,host):         #返回key_1:自定义属性
        key = [ ]
        for sum in range(len(self.header)-2):
            i = self.key_id(self.header[sum+2])
            if i :  #如果在数据库中没有找到相应的key值，则不添加对应的自定义属性
                key.append('"key_%s"'%(i) + ':"%s"'% (self.switches_test[host]['comment'][sum]) ) 
        key = ','.join(key)
        return  key

if __name__ == '__main__':
    t1 = Switches_tool()
    xufan = t1.switches_dici(file_name = 'switch.csv')
    for host in t1.switches_test:
        os.system ( 'echo curl -X POST https://127.0.0.1:20120/query-tasks   -H \\"Content-type:application/json\\" -d \"\'\"\'{\"comment\":\"\", \"cron\":\"00 12 * * *\", \"enable_auto\":\"yes\",\"networks\":[], \"node\":\"local.master\", \"query_range\":\"target\", \"reccurence\":\"daily\", \"snmp_group\":\"%s\", \"snmp_hosts\":[\"%s\"], \"snmp_ver\":\"v2c\",%s }\'\"\'\" -k -u admin:admin'% (t1.switches_test[host]['clss'],host,t1.key_str(host = host) ))

