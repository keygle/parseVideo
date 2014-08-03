<?php

class Renren56 {
	
	public static function parse($url){
		$data = $vid_array = $video_data = array();
		$vid = '';
		if(strpos($url, "vid-")){
			$vid_array = explode(".",substr($url,(strrpos($url,"vid-")+4)));
			$vid =  $vid_array[0];
		}else if(strpos($url, "v_")){
	        $vid_array = explode(".",substr($url,(strrpos($url,"v_")+2)));
	        $vid = $vid_array[0];
	    }
	    if(!empty($vid)){
	    	//获取56视频的地址
	    	$video_url = "http://vxml.56.com/json/{$vid}/?src=site";
	    	$video_json = Base::_cget($video_url);
	    	$video_data = json_decode($video_json,true);
	    	if(is_array($video_data)&&!empty($video_data['info']['rfiles'])){
	    		$data['title'] = $video_data['info']['Subject'];
	    		$data['seconds'] = ceil(intval($video_data['info']['duration'])/1000);
	    		foreach($video_data['info']['rfiles'] as $key =>$val){
	    			if($val['type'] == "normal") $data['normal'][] = $val['url'];
	    			if($val['type'] == "clear") $data['high'][] = $val['url'];
	    			if($val['type'] == "super") $data['super'][] = $val['url'];
	    		}

	    		return $data;
	    	}else{
	    		return false;
	    	}
	    }else{
	    	return false;
	    }
	
	}
}