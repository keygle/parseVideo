<?php
//error_reporting(0);
require 'parserVideo.class.php';
header("content-type:text/html;charset=utf-8");
function debug($url){
    $result = ParserVideo::parse($url);
    echo '<pre>';
    print_r($result);
}

include_once "../xhprof/xhprof_lib/utils/xhprof_lib.php";
include_once "../xhprof/xhprof_lib/utils/xhprof_runs.php";


// start profiling
//xhprof_enable();
//xhprof_enable(XHPROF_FLAGS_CPU + XHPROF_FLAGS_MEMORY);  //同时分析CPU和Mem的开销

//$url = "http://v.qq.com/cover/y/ypq1qwp0ktzusj9/h00132shwru.html";
// $url = "http://v.youku.com/v_show/id_XNzM0MzEyNDY0.html";
$url = "http://www.iqiyi.com/v_19rrnbyreg.html";
//$url = $_GET['url'];>
debug($url);

/*
// stop profiler
$xhprof_data = xhprof_disable();

// display raw xhprof data for the profiler run
//echo '<pre>';
//print_r($xhprof_data);


// save raw data for this profiler run using default
// implementation of iXHProfRuns.
$xhprof_runs = new XHProfRuns_Default();

// save the run under a namespace "xhprof_foo"
$run_id = $xhprof_runs->save_run($xhprof_data, "xhprof_foo");

echo "<a href='http://localhost/xhprof/xhprof_html/callgraph.php?run={$run_id}&source=xhprof_foo'>点击查看消耗时间</a>";


//print_r(get_headers("http://data.vod.itc.cn/preview?file=/233/52/28FAAL9Tq9UX9kOatm6bj7.mp4&start=28"));
*/