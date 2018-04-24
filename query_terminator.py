import re
import numpy as np

class query_terminator:
    path=""
    querys=[]
    cates={}
    pattern_path=""
    conflict_=[]
    que={"query":0,"类别":0,"pv":0}
    patterns_total={}
    patterns_right={}
    patterns_detail={}
    patterns=[]
    Flag=False

    def __init__(self,path):
        self.path=path
        file = open(path, "r", encoding="utf-8")
        line=file.readline()
        while line!="":
            if line.startswith("#"):
                line=line.replace("\n","").split("\t")
                for i in line:
                    i=i.split(":")
                    if i[0] in self.que:
                        self.que[i[0]]=int(i[1])
                line=file.readline()
                continue
            line=line.replace("\n","").split("\t")
            try:
                line=[line[self.que["query"]],line[self.que["类别"]],line[self.que["pv"]]]
                self.querys.append(line)
                self.cates[line[1]]=1
            except:
                pass
            line=file.readline()
        print(self.cates)

    def setpattern(self,path):
        self.pattern_path=path
        pattern = open(self.pattern_path, "r", encoding="utf-8")
        line = pattern.readline()
        while line != "":
            line = line.replace("\n", "").split("\t")
            self.patterns.append(line)
            self.patterns_total[line[0]]=0
            self.patterns_right[line[0]]=0
            line = pattern.readline()

    def match_with_pattern(self,cate,WP=True):
        if cate=="all":
            self._all_match_with_pattern(WP)
        else:
            subquerys=[]
            for i in self.querys:
                if i[1]==cate:
                    subquerys.append(i)
            patterns=[]
            for line in self.patterns:
                if line[1]==cate:
                    patterns.append(line)
            totalpv=0
            matchpv=0
            matchnum=0
            for i in subquerys:
                totalpv+=int(i[2])
                flag=True
                notmatch=True
                for j in patterns:
                    if re.search(j[0],i[0].replace("湿疹","疾病").replace("脱发","疾病")):
                        if notmatch:
                            if self.Flag:
                                if j[1]==i[1]:
                                    try:
                                        self.patterns_right[j[0]]+=int(i[2])
                                    except:
                                        self.patterns_right[j[0]] = int(i[2])
                                try:
                                    self.patterns_total[j[0]] += int(i[2])
                                except:
                                    self.patterns_total[j[0]] = int(i[2])
                                try:
                                    self.patterns_detail[j[0]].append([j[0], i[0],i[1], int(i[2])])
                                except:
                                    self.patterns_detail[j[0]] = [[j[0], i[0],i[1], int(i[2])]]
                            flag=False
                            matchpv+=int(i[2])
                            matchnum+=1
                            if WP:
                                print(i,j[0],i[2])
                        if flag==False:
                            notmatch=False
                        if not notmatch:
                            try:
                                self.patterns_total[j[0]] += int(i[2])
                            except:
                                self.patterns_total[j[0]] = int(i[2])
                if flag:
                    if WP:
                        print(i[0],i[2],"----------------------------------------")
            if WP:
                print(cate,"已匹配pv：",matchpv,"总pv：",totalpv,"比例",matchpv/totalpv)
                print(cate,"已匹配数量：",matchnum,"总数量：",len(subquerys),"比例",matchnum/len(subquerys))
            return [[matchpv,totalpv],[matchnum,len(subquerys)]]

    def _all_match_with_pattern(self,WP=True):
        self.Flag=True
        totalpv=0
        matchpv=0
        totalnum=0
        matchnum=0
        for i in self.cates:
            if WP:
                print("##########################################")
            tmp=self.match_with_pattern(i,WP)
            totalpv+=tmp[0][1]
            matchpv+=tmp[0][0]
            totalnum+=tmp[1][1]
            matchnum+=tmp[1][0]
        if WP:
            print("已匹配pv：", matchpv, "总pv：", totalpv, "比例", matchpv / totalpv)
            print("已匹配数量：", matchnum, "总数量：", totalnum, "比例", matchnum / totalnum)

    def confusion(self):
        _num=0
        cate=[]
        for i in self.cates:
            self.cates[i]=_num
            cate.append(i)
            _num+=1
        confus=np.zeros((_num,_num))
        catetotal = {}
        for i in self.querys:
            try:
                catetotal[i[1]]+=int(i[2])
            except:
                catetotal[i[1]]=int(i[2])
            tmp_patt=[]
            for j in self.patterns:
                if re.search(j[0],i[0].replace("湿疹","疾病").replace("脱发","疾病")):
                    tmp_patt.append(j)
            if len(tmp_patt)>1 and len(set(np.array(tmp_patt)[:,1]))!=1:
                tmp=""
                for k in tmp_patt:
                    for kk in k:
                        tmp+=kk+"-->"
                    tmp+="||"
                tmp="["+tmp.rstrip()+"]"
                self.conflict_.append([i[0],int(i[2]),i[1],tmp])
            if i[1] in tmp_patt:
                confus[self.cates[i[1]],self.cates[i[1]]]+=int(i[2])
            if len(tmp_patt)==0:
                print(i,"---------未匹配--------")
            else:
                confus[self.cates[i[1]],self.cates[tmp_patt[0][1]]]+=int(i[2])
        self.conflict_.sort(key=lambda x: x[1], reverse=True)
        for i in confus:
            for j in i:
                print(str(j)+"\t",end="")
            print("\n",end="")
        for i in cate:
            print(i+"\t",end="")
        print("\n",end="")

        # 输出召回和准确
        print("pv：",end="")
        for i in range(len(cate)):
            print(str(catetotal[cate[i]])+"\t",end="")
        print("\n", end="")
        print("召回：",end="")
        zhtotal=0
        zhed=0
        for i in range(len(cate)):
            zhtotal+=catetotal[cate[i]]
            zhed+=confus[i][i]
            print(str(confus[i][i]/catetotal[cate[i]])+"\t",end="")
        print("\n",end="")
        print("准确：", end="")
        zqtotal=0
        zqed=0
        for i in range(len(cate)):
            zqtotal+=sum(confus[i])
            zqed+=confus[i][i]
            if sum(confus[i])==0:
                print("0"+"\t",end="")
            else:
                print(str(confus[i][i]/sum(confus[i]))+"\t",end="")
        print("\n",end="")
        print("总召回：",str(zhed/zhtotal),"总准确：",str(zqed/zqtotal))
        return confus

    def conflict(self):
        if self.conflict_!=[]:
            for i in self.conflict_:
                print(i)
        else:
            for i in self.querys:
                tmp_patt = []
                for j in self.patterns:
                    if re.search(j[0], i[0].replace("湿疹", "疾病").replace("脱发", "疾病")):
                        tmp_patt.append(j)
                if len(tmp_patt) > 1 and len(set(np.array(tmp_patt)[:, 1])) != 1:
                    tmp = ""
                    for k in tmp_patt:
                        for kk in k:
                            tmp += kk + '-->'
                        tmp += "||"
                    tmp = "[" + tmp.rstrip() + "]"
                    self.conflict_.append([i[0], int(i[2]), i[1], tmp])
            self.conflict_.sort(key=lambda x: x[1], reverse=True)
            for i in self.conflict_:
                print(i)
        return self.conflict_

    def detail(self,pattern__):
        if self.Flag:
            self.patterns_detail[pattern__].sort(key=lambda x: x[2], reverse=True)
            for i in self.patterns_detail[pattern__]:
                print(i)
        else:
            self.match_with_pattern("all",False)
            self.patterns_detail[pattern__].sort(key=lambda x: x[2],reverse=True)
            for i in self.patterns_detail[pattern__]:
                print(i)

    def overview(self):
        print("pattern  总pv 已匹配pv")
        if self.Flag:
            tmp=[]
            for i in self.patterns:
                tmp.append([i[0],self.patterns_total[i[0]],self.patterns_right[i[0]]])
            tmp.sort(key=lambda x: x[2], reverse=True)
            for i in tmp:
                print(i)
        else:
            self.match_with_pattern("all",False)
            tmp = []
            for i in self.patterns:
                tmp.append([i[0], self.patterns_total[i[0]], self.patterns_right[i[0]]])
            tmp.sort(key=lambda x: x[2], reverse=True)
            for i in tmp:
                print(i)

















