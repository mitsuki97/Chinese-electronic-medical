#!/usr/bin/env python3
# coding: utf-8
# File: transfer_data.py
"""
一, 目标序列标记集合
O非实体部分,TREATMENT治疗方式, BODY身体部位, SIGN疾病症状, CHECK医学检查, DISEASE疾病实体,
二, 序列标记方法
采用BIO三元标记 self.cate_dict ={}
三, 数据转换
评测方提供了四个目录(一般项目, 出院项目, 病史特点, 诊疗经过),四个目录下有txtoriginal文件和txt标注文件,内容样式如下:
一般项目-1.txtoriginal.txt
    女性，88岁，农民，双滦区应营子村人，主因右髋部摔伤后疼痛肿胀，活动受限5小时于2016-10-29；11：12入院。
一般项目-1.txt:
    右髋部	21	23	身体部位
    疼痛	27	28	症状和体征
    肿胀	29	30	症状和体征
"""
import os
from collections import Counter

class TransferData:
    def __init__(self):
        cur = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.label_dict = {
                      '检查和检验': 'CHECK',
                      '症状和体征': 'SIGNS',
                      '疾病和诊断': 'DISEASE',
                      '治疗': 'TREATMENT',
                      '身体部位': 'BODY'}
        self.cate_dict ={
                         'O':0,
                         'TREATMENT-I': 1,
                         'TREATMENT-B': 2,
                         'BODY-B': 3,
                         'BODY-I': 4,
                         'SIGNS-I': 5,
                         'SIGNS-B': 6,
                         'CHECK-B': 7,
                         'CHECK-I': 8,
                         'DISEASE-I': 9,
                         'DISEASE-B': 10
                        }
        self.origin_path = os.path.join(cur, 'data_origin')
        self.train_filepath = os.path.join(cur, 'train.txt')
        return

    def transfer(self):
        f = open(self.train_filepath, 'w+',encoding="utf-8")
        count = 0
        for root,dirs,files in os.walk(self.origin_path):
            for file in files:
                filepath = os.path.join(root, file)
                if 'original' not in filepath:
                    continue
                label_filepath = filepath.replace('.txtoriginal','')
                print(filepath, '\t', label_filepath)
                content = open(filepath,'r',encoding='utf8').read().strip()
                res_dict = {}
                for line in open(label_filepath,'r',encoding='utf8'):
                    res = line.strip().split('	')
                    start = int(res[1])
                    end = int(res[2])
                    label = res[3]
                    label_id = self.label_dict.get(label)
                    for i in range(start, end+1):
                        if i == start:
                            label_cate = 'B-'+label_id
                        else:
                            label_cate = 'I-'+label_id
                        res_dict[i] = label_cate
                for indx, char in enumerate(content):
                    char_label = res_dict.get(indx, 'O')
                    print(char, char_label)
                    f.write(char + ' ' + char_label + '\n')
        f.close()
        return

if __name__ == '__main__':
    handler = TransferData()
    train_datas = handler.transfer()