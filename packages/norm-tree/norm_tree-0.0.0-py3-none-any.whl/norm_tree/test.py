# 形式チェック・正規化 [norm_tree]
# 【動作確認 / 使用例】

import sys
import math
import ezpip
norm_tree = ezpip.load_develop("norm_tree", "../", develop_flag = True)
nt = norm_tree

# 基本的な使い方
checker = nt([int, [8, str]])	# [整数, [8, 文字列]] の形を認識
print(checker([9, [8, "hello"]]))	# -> OK
try:
	print(checker([9, [8, 77]]))	# -> 例外
except:
	print("NG!")


# 四捨五入 (独自関数は受理する場合は正規化結果を返し、受理しない場合に例外を投げる)
def round_int(arg_num):
	return math.floor(arg_num + 0.5)	# str等の場合は例外を投げる

checker1 = nt({	# チェッカーの作成 [norm_tree]
	"command": [
		nt.OR("goto", "run"),	# どちらかを許す [norm_tree]
		type("")	# 文字列型の全てのものを受理。str などと書いても良い。
	],
	"num_list": nt.list(round_int),	# 任意長のリスト [norm_tree]
	"info": nt.OR(nt.list(...), None)	# 「...」は任意のオブジェクトを表す
})

res = checker1({"command": ["goto", "home"], "num_list": [1.2, 8, 9], "info": [True, 8]})
print(res)	# -> 受理されて1.2が四捨五入される

try:
	checker1({"command": ["go", "home"], "num_list": [1.2, 8, 9], "info": [True, 8]})	# -> 例外
except Exception as e:
	print(e)

# フォーマットに即しているか否かを返すチェッカー [norm_tree]
checker2 = nt.tf([24, type("")])
print(checker2([24, "hoge"]))	# -> True
print(checker2([24, 4]))	# -> False

# 高度な指定 -- 句構造文法的な入れ子構造の受理

# checker3 = nt.listed_OR(int, nt.list(checker3)) という意味のことをpython文法に則して書きたい
or_nodes = [int, ...]
checker3 = nt.listed_OR(or_nodes)	# リスト指定のOR [norm_tree]
or_nodes[1] = nt.list(checker3)	# 後から書き換えて自己言及

print(checker3(77))	# -> 受理
print(checker3([1, 2, 3]))	# -> 受理
print(checker3([1, 2, [3]]))	# -> 受理
print(checker3([[9, 8, [[[], [7, 8]]]], 7, [9, 0]]))	# -> 受理
try:
	print(checker3([1, 2, [3, "hoge"]]))	# -> 例外
except:
	print("NG!")