import sys
sys.path.append("..")
import query_terminator

# "C:/Users/wangnanzhi/Desktop/诊疗中心/huangtao.txt"
# "C:/Users/wangnanzhi/Desktop/诊疗中心/pattern_on_server_bak.txt"
# qt=query_terminator.query_terminator("C:/Users/wangnanzhi/Desktop/诊疗中心/huangtao.txt")
# qt.setpattern("C:/Users/wangnanzhi/Desktop/诊疗中心/pattern_on_server_bak.txt")

qt=query_terminator.query_terminator(sys.argv[1])
qt.setpattern(sys.argv[2])
# print(sys.argv[0],sys.argv[1])

while True:
    str = input("enter conmand:")
    if str=="confusion":
        qt.confusion()
    if str=="conflict":
        qt.conflict()
    if str.startswith("category"):
        qt.match_with_pattern(str.split(" ")[1])
    if str=="pattern overview":
        qt.overview()
    if str.startswith("pattern detail"):
        qt.detail(str.split(" ")[2])