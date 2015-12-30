# makefile for parse_video/, <https://github.com/sceext2/parse_video>, used for parse_video test
# version 0.0.1.0 test201512301521

# parse_video bin
PV_BIN=./parsev

# extractor test URLs
ET_URL_BKS1_1=http://www.iqiyi.com/v_19rrkfbay8.html
ET_URL_LETV_1=http://www.letv.com/ptv/vplay/24185834.html
ET_URL_HUNANTV_1=http://www.hunantv.com/v/2/168868/f/2928760.html

# test extractor bks1 vv mode
ET_URL_BKS1_2=http://www.iqiyi.com/v_19rrkgos5s.html

# TODO add parse Error and fix BUG test

target: test
.phony: target, test, clean, clean_test, test_bin, test_parse, test_more, test_v

# run parse_video auto test
test: test_bin, test_parse, test_more

clean: clean_test

# test parse_video bin
test_bin:
	echo "pv_test:: start test_bin "
	
	$(PV_BIN)
	$(PV_BIN) --help
	$(PV_BIN) --license
	$(PV_BIN) --version
	
	echo "pv_test:: [ OK ] end test_bin "
	# end test_bin

# test parse_video base parse functions, test each extractor
#   include:
# +   hd_min, hd_max select test
# +   i_min, i_max select test
# +   --debug, --quiet log test
test_parse:
	echo "pv_test:: start test_parse "
	
	echo "pv_test:: INFO: test extractor bks1 "
	# test extractor bks1
	$(PV_BIN) $(ET_URL_BKS1_1) -i 2
	$(PV_BIN) $(ET_URL_BKS1_1) --min 1 --max 1 --i-min 2 --i-max 3 --debug
	$(PV_BIN) $(ET_URL_BKS1_1) --min 2 --max -1 -q -m "pc_flash_gate;set_um"
	
	echo "pv_test:: INFO: test extractor letv "
	# test extractor letv
	$(PV_BIN) $(ET_URL_LETV_1) -i 3
	$(PV_BIN) $(ET_URL_LETV_1) -i 5 --debug
	
	echo "pv_test:: INFO: test extractor hunantv "
	# test extractor hunantv
	$(PV_BIN) $(ET_URL_HUNANTV_1) --debug
	$(PV_BIN) $(ET_URL_HUNANTV_1) -i 2
	
	echo "pv_test:: [ OK ] end test_parse "
	# end test_parse

# test extractor --more mode support
test_more:
	echo "pv_test:: start test_more "
	
	echo "pv_test:: INFO: test extractor bks1 "
	# test extractor bks1
	$(PV_BIN) $(ET_URL_BKS1_1) -i 1 -M 0 -m "pc_flash_gate;enable_more,set_um" -o "test_more.e_bks1.tmp.json"
	$(PV_BIN) $(ET_URL_BKS1_1) -i 3 --more "test_more.e_bks1.tmp.json"
	
	echo "pv_test:: INFO: test extractor letv "
	# test extractor letv
	$(PV_BIN) $(ET_URL_LETV_1) -m "pc_flash_gate;enable_more" -o "test_more.e_letv.tmp.json"
	$(PV_BIN) $(ET_URL_LETV_1) -i 3 --more "test_more.e_letv.tmp.json"
	
	echo "pv_test:: INFO: test extractor hunantv "
	# test extractor hunantv
	$(PV_BIN) $(ET_URL_HUNANTV_1) -i 1 -M 0 -m "pc_flash_gate;enable_more" -o "test_more.e_hunantv.tmp.json"
	$(PV_BIN) $(ET_URL_HUNANTV_1) -i 2 --more "test_more.e_hunantv.tmp.json"
	
	echo "pv_test:: [ OK ] end test_more "
	# end test_more

# remove test tmp files
clean_test:
	- rm test_more.e_bks1.tmp.json
	- rm test_more.e_letv.tmp.json
	- rm test_more.e_hunantv.tmp.json
	# end clean_test

# test extractor vv mode
test_v:
	# test extractor bks1
	$(PV_BIN) $(ET_URL_BKS1_2) -m "pc_flash_gate;set_flag_v" -i 3
	
	# end test_v

# end makefile


