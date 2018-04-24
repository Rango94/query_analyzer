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
    # 输出混淆矩阵，各个类别的准召，总准召
    if str=="confusion":
        qt.confusion()
    # 输出冲突项，多个不同类别的pattern打上同一个query
    if str=="conflict":
        qt.conflict()
    # 输出某一类别下的所有query匹配情况，category all命令为输出所有
    if str.startswith("category"):
        qt.match_with_pattern(str.split(" ")[1])
    # 输出所有pattern的表现情况，也就是每一个pattern匹配正确的pv量与总的匹配上的pv量
    if str=="pattern overview":
        qt.overview()
    # 输出某一pattern的具体表现情况,输出匹配的query，query实际的类别，pv量
    if str.startswith("pattern detail"):
        qt.detail(str.split(" ")[2])