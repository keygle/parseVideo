# makefile for parse_video/, <https://github.com/sceext2/parse_video>, used for parse_video test
# version 0.1.2.0 test201601022215

# parse_video bin
PV_BIN=./parsev

# extractor test URLs
ET_URL_BKS1_1=http://www.iqiyi.com/v_19rrkfbay8.html
ET_URL_LETV_1=http://www.letv.com/ptv/vplay/24185834.html
ET_URL_HUNANTV_1=http://www.hunantv.com/v/2/168868/f/2928760.html
ET_URL_TVSOHU_1=http://tv.sohu.com/20140914/n404300963.shtml
ET_URL_PPTV_1=http://v.pptv.com/show/0UyKCXHXR4XoZs4.html

# test extractor bks1 vv mode
ET_URL_BKS1_2=http://www.iqiyi.com/v_19rrkgos5s.html

# TODO add parse Error and fix BUG test

target: test
.PHONY: target test clean clean_py

# run parse_video auto test
test: test_bin test_parse test_more
.PHONY: test_bin test_parse test_more test_v

clean: clean_test
.PHONY: clean_test

# test parse_video bin
test_bin:
	# pv_test:: start test_bin
	$(PV_BIN)
	$(PV_BIN) --help
	$(PV_BIN) --license
	$(PV_BIN) --version
	# pv_test:: [ OK ] end test_bin

# test parse_video base parse functions, test each extractor
#   include:
# +   hd_min, hd_max select test
# +   i_min, i_max select test
# +   --debug, --quiet log test
test_parse: \
	test_parse_bks1 \
	test_parse_letv \
	test_parse_hunantv \
	test_parse_tvsohu \
	test_parse_pptv
.PHONY: test_parse_bks1 \
	test_parse_letv \
	test_parse_hunantv \
	test_parse_tvsohu \
	test_parse_pptv

test_parse_bks1:
	# pv_test:: INFO: parse test extractor bks1
	$(PV_BIN) $(ET_URL_BKS1_1) -i 2
	$(PV_BIN) $(ET_URL_BKS1_1) --min 1 --max 1 --i-min 2 --i-max 3 --debug
	$(PV_BIN) $(ET_URL_BKS1_1) --min 2 --max -1 -q -m "pc_flash_gate;set_um"

test_parse_letv:
	# pv_test:: INFO: parse test extractor letv
	$(PV_BIN) $(ET_URL_LETV_1) -i 3 -m "pc_flash_gate;fast_parse"
	$(PV_BIN) $(ET_URL_LETV_1) -i 5 -m "pc_flash_gate" --debug
	$(PV_BIN) $(ET_URL_LETV_1)

test_parse_hunantv:
	# pv_test:: INFO: parse test extractor hunantv
	$(PV_BIN) $(ET_URL_HUNANTV_1) --debug -i 2 -m "pc_flash_gate"
	$(PV_BIN) $(ET_URL_HUNANTV_1) -m "flvsp"

test_parse_tvsohu:
	# pv_test:: INFO: parse test extractor tvsohu
	$(PV_BIN) $(ET_URL_TVSOHU_1) -i 4 -m "flvsp"
	$(PV_BIN) $(ET_URL_TVSOHU_1) -M 0 --debug -m "pc_flash_gate"

test_parse_pptv:
	# pv_test:: INFO: parse test extractor pptv
	$(PV_BIN) $(ET_URL_PPTV_1) -i 4
	$(PV_BIN) $(ET_URL_PPTV_1) -M 0 --debug -m "pc_flash_gate"
	$(PV_BIN) $(ET_URL_PPTV_1) -m "android"

# test extractor --more mode support
test_more: \
	test_more_bks1 \
	test_more_letv \
	test_more_hunantv \
	test_more_tvsohu \
	test_more_pptv
.PHONY: test_more_bks1 \
	test_more_letv \
	test_more_hunantv \
	test_more_tvsohu \
	test_more_pptv

test_more_bks1:
	# pv_test:: INFO: more test extractor bks1
	$(PV_BIN) $(ET_URL_BKS1_1) -i 1 -M 0 -m "pc_flash_gate;enable_more,set_um" -o "test_more.e_bks1.tmp.json"
	$(PV_BIN) $(ET_URL_BKS1_1) -i 3 --more "test_more.e_bks1.tmp.json"

test_more_letv:
	# pv_test:: INFO: more test extractor letv
	$(PV_BIN) $(ET_URL_LETV_1) -i 1 -M 0 -m "pc_flash_gate;fast_parse,enable_more" -o "test_more.e_letv.tmp.json"
	$(PV_BIN) $(ET_URL_LETV_1) -i 3 --more "test_more.e_letv.tmp.json"

test_more_hunantv:
	# pv_test:: INFO: more test extractor hunantv
	$(PV_BIN) $(ET_URL_HUNANTV_1) -i 1 -M 0 -m "pc_flash_gate;enable_more" -o "test_more.e_hunantv.tmp.json"
	$(PV_BIN) $(ET_URL_HUNANTV_1) -i 2 --more "test_more.e_hunantv.tmp.json"

test_more_tvsohu:
	# pv_test:: INFO: more test extractor tvsohu
	$(PV_BIN) $(ET_URL_TVSOHU_1) -i 1 -M 0 -m "pc_flash_gate;enable_more" -o "test_more.e_tvsohu.tmp.json"
	$(PV_BIN) $(ET_URL_TVSOHU_1) -i 7 --more "test_more.e_tvsohu.tmp.json"

test_more_pptv:
	# pv_test:: INFO: more test extractor pptv
	$(PV_BIN) $(ET_URL_PPTV_1) -i 1 -M 0 -m "pc_flash_gate;enable_more" -o "test_more.e_pptv.tmp.json"
	$(PV_BIN) $(ET_URL_PPTV_1) -i 5 --more "test_more.e_pptv.tmp.json"

# remove test tmp files
clean_test:
	- rm test_more.e_bks1.tmp.json
	- rm test_more.e_letv.tmp.json
	- rm test_more.e_hunantv.tmp.json
	- rm test_more.e_tvsohu.tmp.json
	- rm test_more.e_pptv.tmp.json

# test extractor vv mode
test_v:
	# test extractor bks1
	$(PV_BIN) $(ET_URL_BKS1_2) -m "pc_flash_gate;set_flag_v" -i 3

# clean python 3 tmp (cache) files
clean_py:
	- find . | grep "\.pyc" | xargs rm -v
	- find . | grep "__pycache__" | xargs rmdir -v

# end makefile


