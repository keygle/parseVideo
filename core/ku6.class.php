<?php

class Ku6 {

	public static function parse($url){
		$vid = "";
		$data = $vids_array = $video_data = $sharpness = array();
		if(strpos($url, "/show/")){
			$vids_array = explode(".html",substr($url,(strpos($url, "/show/")+6)));
			$vid = $vids_array[0]?$vids_array[0]:"";
		}else if(strpos($url, "/show_")){
			$vids_array = explode(".html",substr($url,(strrpos($url, "/")+1)));
			$vid = $vids_array[0]?$vids_array[0]:"";
		}

		if(!empty($vid)){
			//酷6视频接口
			$video_url = "http://v.ku6.com/fetchVideo4Player/{$vid}.html";
			$video_data = json_decode(Base::_cget($video_url),true);
			$data['title'] = $video_data['data']['t'];
			$vtimes = explode(',',$video_data['data']['vtime']);
			$data['seconds'] = $vtimes[0];
			if(is_array($video_data['data'])&& !empty($video_data['data']['f'])){
				$video_url_array = explode(',',$video_data['data']['f']);
				if(is_array($video_url_array) && !empty($video_url_array[0])){
					//酷6视频码率 接口 http://main.gslb.ku6.com/...sa8fcc1450dcab0092e0d9c20a186f1f5-1-00-00-00.f4v?ref=out
					//多段视频只拿第一段 获取码率
					$ref_url = $video_url_array[0]."?ref=out";
					$sharpness = self::getVideoRate($ref_url);
					if(!empty($sharpness)){
						foreach($video_url_array as $val){
							foreach($sharpness as $k => $v){
								//根据码率 获得相应的 视频地址
								$data[$k][] = $val."?strart=0&rate=".$v;
							}
						}
					}
				}
			}
			return $data;

		}else{
			return false;
		}


	}

	/**
	 * [getVideoRate 获得视频的码率数组]
	 * @param  [type] $url [description]
	 * @return [type]      [description]
	 */
	private static function getVideoRate($url){
		$sharpness = array();
		$video_info = json_decode(Base::_cget($url),true);
		$video_rate= explode(";",$video_info["RateInfo"]);
		if(is_array($video_rate)&&!empty($video_rate)){
			foreach($video_rate as $key => $val){
				$tmp_array = explode("@",$val);
				if($tmp_array[1] == "流  畅") $sharpness["fluent"] = $tmp_array[0];
				if($tmp_array[1] == "标  清") $sharpness["normal"] = $tmp_array[0];
				if($tmp_array[1] == "高  清") $sharpness["high"] = $tmp_array[0];
				if($tmp_array[1] == "超  清") $sharpness["super"] = $tmp_array[0];
			}
		}
		return $sharpness;	
	}
}