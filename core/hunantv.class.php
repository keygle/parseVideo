<?php

class Hunantv {

	public static function parse($url){
		$html = Base::_cget($url);
		$videos = $infos =  $data = $video_data = array();
		preg_match("#VIDEOINFO\s*=\s*(\{[\s\S]+?\})#ms",$html,$videos);
		//修复json 里面的 键值不能像 http:// 等 存在冒号的  否则会 修复失败
		$infos = json_decode(preg_replace('@([\w_0-9]+):@', '"\1":', str_replace('\'', '"', $videos[1])),true);
		if(empty($infos)){
			return false;
			exit(0);
		}else{
			$limitrate = intval($infos['limit_rate']*1.2);
			//通过拼接参数 来获得视频地址 
			$fhv_url = "http://pcvcr.cdn.imgo.tv/ncrs/vod.do?fid=".$infos['code']."&limitrate=".$limitrate."&file=".$infos['file']."&fmt=2&pno=1";
			$m3u8_url = "http://pcvcr.cdn.imgo.tv/ncrs/vod.do?fid=".$infos['code']."&limitrate=".$limitrate."&file=".$infos['file']."&fmt=6&pno=3&m3u8=1";
			$video_data = json_decode(Base::_cget($fhv_url),true);
			if($video_data){
				$data['normal'][] = $video_data['info'];
				return $data;			
			}else{
				return false;
			}
		}
	}
}