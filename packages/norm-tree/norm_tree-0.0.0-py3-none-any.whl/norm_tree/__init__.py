# 形式チェック・正規化 [norm_tree]

import sys

# フォーマットエラー
f_err = Exception("[norm_tree error] invalid format.")

# 型チェックの生成 [norm_tree]
def gen_checker(format_obj):
	fo = format_obj
	# チェック関数
	def checker(arg):
		# 任意の値を許容
		if fo == ...: return arg
		# foが「チェッカー」の場合
		if type(fo) == type(lambda: None):
			return fo(arg)
		# 型での指定の場合
		if type(fo) == type(type(23)):
			if type(arg) != fo: raise f_err
			return arg
		# リスト指定の場合
		if type(fo) == type([]):
			if type(arg) != type([]): raise f_err	# リストチェック
			if len(arg) != len(fo): raise f_err	# 長さ一致チェック
			return [gen_checker(_fo)(e)
				for e, _fo in zip(arg, fo)]
		# 辞書の場合
		if type(fo) == type({}):
			if type(arg) != type({}): raise f_err	# 辞書チェック
			if set(arg) != set(fo): raise f_err	# keyの一致チェック
			return {k: gen_checker(fo[k])(arg[k])
				for k in arg}
		# 値そのものとの一致を見る場合
		if arg != fo: raise f_err
		return arg
	return checker

# nt_objのクラス
class NT_Obj:
	# 初期化処理
	def __init__(self):
		pass
	# 関数的呼び出し [norm_tree]
	def __call__(self, format_obj):
		# 型チェックの生成 [norm_tree]
		return gen_checker(format_obj)
	# フォーマットに即しているか否かを返すチェッカー [norm_tree]
	def tf(self, format_obj):
		# 加工前のチェッカー
		org_checker = self(format_obj)	# 関数的呼び出し [norm_tree]
		def checker(arg):
			try:
				org_checker(arg)
				return True
			except:
				return False
		return checker
	# どちらかを許す [norm_tree]
	def OR(self, *fo_ls): return self.listed_OR(fo_ls)	# リスト指定のOR [norm_tree]
	# リスト指定のOR [norm_tree]
	def listed_OR(self, fo_ls):
		# チェッカー
		def checker(arg):
			for fo in fo_ls:
				# チェッカーで包む
				one_checker = self(fo)	# 関数的呼び出し [norm_tree]
				try:
					return one_checker(arg)
				except:
					pass
			raise f_err
		return checker
	# 任意長のリスト [norm_tree]
	def list(self, format_obj):
		# チェック関数
		def checker(arg):
			if type(arg) != type([]): raise f_err	# リストチェック
			one_checker = self(format_obj)	# 関数的呼び出し [norm_tree]
			return [one_checker(e) for e in arg]
		return checker

# norm_treeモジュールとnt_objオブジェクトを同一視
nt_obj = NT_Obj()
sys.modules[__name__] = nt_obj