<?php

class Sina {
	
	public static function parse($url){
		$vid = $html = '';
		$data = $video_data = $vids = $vid_array = array();
		$html = Base::_cget($url);
		if(strpos($url, "#")){
			$vid_array[]= substr($url,(strpos($url, "#")+1));
		}else{
			preg_match("#vid:\s*'([^']+)'#ms",$html,$vids);
			//preg_match("#title:\s*'([^']+)'#ms",$html,$titles);
			//$title = (!empty($titles[1]))? trim($titles[1]): '';
			if(is_array($vids)&&!empty($vids[1])){
				$vid_array = explode("|",trim($vids[1])); //第二个vid为高清格式的vid
			}else{
				return false;
			}
		}
        if(empty($vid_array[0])){
            return  false;
        }

        $xml_url = self::generateUrl($vid_array[0]);
        $video_data = self::parseXml($xml_url);

		//根据vid 获得 ipad_vid 的api 接口   ipad_vid 部分在页面上也可以获得
		$api_ipad_url = "http://video.sina.com.cn/interface/video_ids/video_ids.php?v=".$vid_array[0];
		$vid_ipad_array = json_decode(Base::_cget($api_ipad_url),true);
		$ipad_vid = $vid_ipad_array['ipad_vid'];
		$data['title'] = $video_data['title']?$video_data['title']:'';
		$data['fluent'][] = "http://v.iask.com/v_play_ipad.php?vid=".$ipad_vid;
		$data['normal'][] = "http://v.iask.com/v_play_ipad.php?vid=".$vid_array[0];
        $data['seconds'] = $video_data['seconds']?$video_data['seconds']:'';
        if(!empty($vid_array[1])){
            $data['high'][] = "http://v.iask.com/v_play_ipad.php?vid=".$vid_array[1];
        }
		return $data;
	}

    /**
     * [generateUrl 根据vid 来生成xml 路径]
     * @param  [type] $vid [description]
     * @return [type]      [description]
     */
    private static function generateUrl($vid){
        // "http://v.iask.com/v_play.php?vid=117087793&uid=1&pid=1&tid=334&plid=4001&prid=ja_7_2184731619&referrer=http%3A%2F%2Fvideo.sina.com.cn%2F&ran=0.030293308664113283&r=video.sina.com.cn&v=4.1.42.29&p=i&k=26689ad82f6ce4f321594176"
        // 生成k值获得下载地址
        $ran = mt_rand(0,1000);
        $timestamp = time();
        $timestamp = decbin($timestamp);
        $timestamp = substr($timestamp, 0, -6);
        $timestamp = bindec($timestamp);  
        //这里是一个时间戳，目前可以固定，如果失效的话 用上面4行代码即可
        $ran_array = array(
            $vid,
            'Z6prk18aWxP278cVAH', //这个值用硕思直接破解竟然看不到，害得我测试了数小时，以为算法有问题
            $timestamp,
            $ran,
        );
        $key = implode('', $ran_array);
        $key = md5($key);
        $key = substr($key, 0, 16);
        $key .= $timestamp;
            
        $xml_url = 'http://v.iask.com/v_play.php?' . http_build_query(array(
                'vid' => $vid,
                'uid' => '1',
                'pid' => '1',
                'tid' => '334',
                'plid' => '4001',
                'prid' => 'ja_7_2184731619',
                'referrer' => 'http://video.sina.com.cn',
                'ran' => $ran,
                'r' => 'video.sina.com.cn',
                'v' => '4.1.42.29',
                'p' => 'i',
                'k' => $key,
            ));
        return $xml_url;
    }

    private static function parseXml($url){
        $video = $seconds = $title = '';
        $video_url = array();
        $xml_str = Base::_cget($url);
        if(!empty($xml_str)){
            $video = @simplexml_load_string($xml_str);
            $seconds = intval($video->timelength)/1000; //获得时长
            $title = strval($video->vname);
            //解析视频地址
            $durl = $video->durl;
            for($i=0;$i<$durl->count();$i++){
                $video_url[] = strval($durl[$i]->url);
            }
            return array("title"=>$title,"seconds"=>$seconds,'url'=>$video_url);
        }else{
            return false;
        }
    }
}