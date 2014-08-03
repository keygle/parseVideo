<?php
class Pps {
	public static function parse($url){
		$key = "";
		$data = $keys = array();
		//pps 的站点数组
		$pps_sites = array("dp.ugc.pps.tv","dp.ppstream.com","dp.ppstv.com");
		if(strpos($url,"/play_") != false){
			$keys = explode('.',substr($url,(strpos($url,"play_")+5)));
			$key = $keys[0]?trim($keys[0]):'';
			if($key){
				foreach($pps_sites as $val){
					//pps 的api 接口  http://dp.ppstv.com/get_play_url_cdn.php?sid=312WAZ&flash_type=1&type=0  type = 0/1/2  貌似表示清晰度？
					$get_url = "http://".$val."/get_play_url_cdn.php?sid=".$key."&flash_type=1";
					//$headers = @get_headers($get_url); 根据返回的状态来判断 is_array($headers) && (strrpos($headers[0], "200") != false)
					$video_str = @Base::_cget($get_url);
					if(!empty($video_str)&&(strpos($video_str,".pfv") != false)){
						$video_array = explode("&",$video_str);
						$data['normal'][] = substr($video_str,0,strpos($video_str,"?"));
						$data['title'] = $video_array[2]?ltrim($video_array[2],'title='):'';
						$data['seconds'] = $video_array[5]?ltrim($video_array[5],'ct='):'';
						break;
					}
					
				}
				if(!empty($data)){
					$html = Base::_cget($url);
					$video_ids = array();
					preg_match('#video_id:\s*"([^"]+)"#',$html,$video_ids);
					$video_id = $video_ids[1]?trim($video_ids[1]):'';
					//pps 的html5 接口
					$h5_url = "http://active.v.pps.tv/ugc/ajax/aj_html5_url.php?url_key={$key}&video_id={$video_id}";
					$h5_data = json_decode(substr(ltrim(Base::_cget($h5_url),"html5url("),0,-1),true);
					$data['fulent'][] = $h5_data[0]['path'];
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