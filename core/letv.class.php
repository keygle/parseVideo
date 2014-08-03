<?php

class Letv {

	public static function parse($url){
		$html = Base::_cget($url);
		$vid = '';
		$vids = $data = $video_data = array();
		preg_match("#vid:\s*([\d]+),#ms",$html,$vids);
		$vid = $vids[1]?trim($vids[1]):'';
		if(empty($vid)){
			return false;
			exit(0);
		}else{
			$tkey = Letv::getKey(time());
			//通过解析 乐视 的xml 来获得视频地址 tkey值需要计算  
			$xml_url = "http://api.letv.com/mms/out/video/play?id={$vid}&platid=1&splatid=101&format=0&tkey={$tkey}&domain=www.letv.com";
			$video_data = Letv::parseXml($xml_url);
			if($video_data){
				//存有视频的数组 有 dispatch dispatchbak dispatchbak1 dispatchbak2  这里使用 dispatch
				if(is_array($video_data['dispatch'])&&!empty($video_data['dispatch'])){
					foreach($video_data['dispatch'] as $key =>$val){
						//加上后面的参数才可以播放
						if($key == "350") $data['fluent'][] = Letv::getPlayUrl($val[0]);
						if($key == "1000") $data['normal'][] = Letv::getPlayUrl($val[0]);
						if($key == "1300") $data['high'][] = Letv::getPlayUrl($val[0]);
						if($key == "720p") $data['super'][] = Letv::getPlayUrl($val[0]);
						if($key == "1080p") $data['original'][] = Letv::getPlayUrl($val[0]);
					}
				}
				$data['title'] = $video_data['title'];
				$data['seconds'] = $video_data['duration'];	
				return $data;			
			}else{
				return false;
			}
		}
	}

	/**
	 * [parseXml 解析相关xml]
	 * @param  [type] $url [description]
	 * @return [type]      [description]
	 */
	static public function parseXml($url){
		$xml_str = Base::_cget($url);
		$xml_obj = @simplexml_load_string($xml_str);
		$playurl = $xml_obj->playurl;
		if(!empty($playurl)){
			$play_str = strval($playurl);
			$play_json = json_decode($play_str,true);
			if(is_array($play_json)){
				return $play_json;
			}else{
				return false;
			}
			
		}else{
			return  false;
		}
	}

	/**
	 * [getKey 2014 letv tkey值的算法]
	 * @param  [type] $t [时间戳]
	 * @return [type]    [description]
	 */
	static private function getKey($t){
	    for($e, $s = 0; $s < 8; $s++){
	        $e = 1 & $t;
	        $t >>= 1; 
	        $e <<= 31; 
	        $t += $e;
	    }
		return $t^185025305;
	}

	/**
	 * [getPlayUrl 根据前面拿到的url 获得视频地址]
	 * @param  [type] $url [description]
	 * @return [type]      [description]
	 */
	static private function getPlayUrl($url){
		$tn = (mt_rand(10000,99999)*865);
		$url = $url."&termid=1&format=1&hwtype=un&ostype=Windows8.1&tag=letv&sign=letv&expect=3&tn=0.".$tn."&pay=0&rateid=1000";
		$playJson = Base::_cget($url);
		$urls = json_decode($playJson,true);
		if($urls['location']){
			return $urls['location'];
		}else{
			return false;
		}
		
	}
}