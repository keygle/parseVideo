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
			//通过解析 乐视 的xml 来获得视频地址
			$xml_url = "http://www.letv.com/v_xml/{$vid}.xml";
			$video_data = self::parseXml($xml_url);
			if($video_data){
				//存有视频的数组 有 dispatch dispatchbak dispatchbak1 dispatchbak2  这里使用 dispatch
				if(is_array($video_data['dispatch'])&&!empty($video_data['dispatch'])){
					foreach($video_data['dispatch'] as $key =>$val){
						if($key == "350") $data['fluent'][] = $val[0];
						if($key == "1000") $data['normal'][] = $val[0];
						if($key == "1300") $data['high'][] = $val[0];
						if($key == "720p") $data['super'][] = $val[0];
						if($key == "1080p") $data['original'][] = $val[0];
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
	public static function parseXml($url){
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
}