<?php

class Pptv {
	
	public static function parse($url){
		$vid = '';
		$html = Base::_cget($url);
		preg_match('#"vid":\s*([\d]+)#ms',$html,$vids);
		$vid = $vids[1]?trim($vids[1]):'';
		if($vid){
			return self::getVideoData($vid);
		}else{
			return false;
		}
	}

	private static function getVideoData($vid){
		//pptv 接口 http://play.api.pptv.com/boxplay.api?cb=json&auth=mpptv&ver=2&id=16904252&ft=5&type=mpptv&platform=ikan&_=1382552026550
		$file_array = $data = array();
		$get_url = "http://play.api.pptv.com/boxplay.api?cb=json&auth=mpptv&ver=2&id=".$vid."&ft=5&type=mpptv&platform=ikan&_=".time().mt_rand(100,999);
		$video_json = rtrim(ltrim(Base::_cget($get_url),'json ('),');');
		$video_data = json_decode($video_json,true);
		foreach($video_data['childNodes'] as $nodeVals){
			//获得影片名称和视频文件参数 
			if($nodeVals['tagName'] == 'channel'){
				$data['title'] = $nodeVals['nm'];
				$data['seconds'] = $nodeVals['dur'];
				foreach($nodeVals['childNodes'] as $nodeVal){
					if($nodeVal['tagName'] == 'file'){
						foreach($nodeVal['childNodes'] as $node){
							if($node['tagName'] == 'item'){
								//获取视频文件参数地址
								$file_array[$node['ft']]['file']= $node['rid'];
								$file_array[$node['ft']]['height']= $node['height'];
								$file_array[$node['ft']]['width']= $node['width'];
							}
						}
					}
				}
			}
			//获得视频地址参数
			if($nodeVals['tagName'] == 'dt'){
				foreach($nodeVals['childNodes'] as $nodeVal){
					//获取视频ip地址
					if($nodeVal['tagName'] == 'sh'){
						$file_array[$nodeVals['ft']]['host'] = $nodeVal['childNodes'][0];
					}
					//获取视频key值
					if($nodeVal['tagName'] == 'key'){
						$file_array[$nodeVals['ft']]['key'] =  $nodeVal['childNodes'][0];
					}					
				}
			}
		}

		if(!empty($file_array)){
			foreach ($file_array as $key => $val){
				//构建视频地址 视频地址不能带 key值 
				if($key == 0) $data['normal'][]= 'http://'.$val['host'].'/0/'.$val['file'].'?k='.$val['key'].'&type=web.fpp'; 
				if($key == 1) $data['high'][]= 'http://'.$val['host'].'/0/'.$val['file'].'?k='.$val['key'].'&type=web.fpp'; 
				if($key == 2) $data['super'][]= 'http://'.$val['host'].'/0/'.$val['file'].'?k='.$val['key'].'&type=web.fpp'; 
				if($key == 5) $data['fluent'][]= 'http://'.$val['host'].'/0/'.$val['file'].'?k='.$val['key'].'&type=web.fpp'; 
			}	
			return $data;	
		}else{
			return false;
		}
	}
}