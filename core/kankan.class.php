<?php

class Kankan {

	//视频清晰度数组
	private static $sharpness_array = array("fluent","normal","high","super");
	private static $list_array = array('teleplay','tv','lesson','documentary');

    /**
     * [parse description]
     * @param  [type] $url  [视频地址]
     * @param  [type] $list [电视剧列表] 
     * @return [type]       [description]
     */
	public static function parse($url,$list = null){
        $html = Base::_cget($url);
        $data = array();
        preg_match("#G_MOVIE_TITLE\s*=\s*'([^']+)'#ms",$html,$titles);
        $title = iconv('gbk', 'utf-8', $titles[1]);
        preg_match("#G_MOVIEID\s*=\s*'([^']+)'#ms",$html,$movieids); //获得电影id 
        preg_match("#G_MOVIE_TYPE\s*=\s*'([^']+)'#ms",$html,$types);//获得视频类型
        $movie_id = $movieids[1];
        $type = trim($types[1]);
        preg_match("#subnames:\[([^]]+)\]#ms",$html,$subnames); //获得视频名数组
        eval('$video_names= array('.$subnames[1].');');
        $video_name = $video_names[count($video_names)-1]?$video_names[count($video_names)-1]:'';
        $video_name = iconv('gbk', 'utf-8', $video_name);    
        if(strpos($url,"subid=")){
        	preg_match("#subid=([\d]+)#",$url,$subid);
        	$subid = $subid[1];
            $subids[] = $subid; 
        }else{
        	preg_match("#subids:\[([^]]+)\]#ms",$html,$subids); //获得视频id数组
            $subids = array_filter(explode(',',$subids[1]));
        	$subid = array_pop($subids); //将最后的id 赋值

        }
        //判断是不是获得电视列表
        if($list == 'list'){
            $data['list'] = self::getVideoList($movie_id,$subids,$video_names);
        } 

        if(in_array($type,self::$list_array) && !empty($video_name)){
        	//匹配多集电视
        	$data['title'] = $title."--".$video_name;
        }else{
        	//匹配单个影片
        	$data['title'] = $title;
        }
        //匹配网页上的gcid
    	preg_match_all("#http://pubnet.sandai.net:8080/\d/([^/]+)/#",$html,$gcids);
        $gcid_array = $gcids[1];
    	if(is_array($gcid_array)&&count($gcid_array)>0){
            //只选取前四段。
    		for($i=0;$i<4;$i++){
    			$data['flv'][self::$sharpness_array[$i]][] = self::getVideoUrl($gcid_array[$i]);
    		}
    	}

    	return  $data;	
	}

	/**
	 * [getVideoUrl 根据gcid来获得视频地址]
	 * @param  [type] $gcid [description]
	 * @return [type]       [description]
	 */
	private static function getVideoUrl($gcid,$file_type="flv"){
        if($file_type == "mp4"){
            $get_url = "http://mp4.cl.kankan.com/getCdnresource_flv?gcid=";
            $url = $get_url.strtoupper($gcid);
            $video_html = Base::_cget($url);  //获得视频地址信息
            preg_match('#ip:"([^"]+)?".*path:"([^"]+)?"#',$video_html,$videos);            
            preg_match("#param1:([\d]+),param2:([\d]+)#",$video_html,$params);
            $video_url = "http://".$videos[1]."/".$videos[2]."?key=".md5('xl_mp43651'.$params[1].$params[2])."&key1=".$params[2];
            //mp4 格式的key 为 md5('xl_mp43651'.$params[1].$params[2])
        }else{
            $get_url = "http://p2s.cl.kankan.com/getCdnresource_flv?gcid=";
            $url = $get_url.strtoupper($gcid);
            $video_html = Base::_cget($url);  //获得视频地址信息
            preg_match('#ip:"([^"]+)?".*path:"([^"]+)?"#',$video_html,$videos);            
            $video_url = "http://".$videos[1]."/".$videos[2];
        }
        return $video_url;
        
	}

    //获取电视剧的地址列表
    public static function getVideoList($movie_id,$subids,$video_names){
        $data = array();
        if(is_array($subids) && count($subids)>0){
            foreach($subids as $k=>$v){
                $data[$k]['name'] = iconv("gbk","utf-8",$video_names[$k]); //获得视频的名字
                $url = "http://api.movie.kankan.com/vodjs/subdata/".floor($movie_id/1000)."/".$movie_id."/".$v.".js";
                $movie_str = Base::_cget($url);
                preg_match("#surls:\s*\[([^]]+)\]#",$movie_str,$surls);
                eval('$surls_array = array('.$surls[1].');'); //转化为数组
                $surls_array = array_filter($surls_array);// 过滤数组
                preg_match("#msurls:\s*\[([^]]+)\]#",$movie_str,$msurls);
                eval('$msurls_array = array('.$msurls[1].');');
                $msurls_array = array_filter($msurls_array);
                if(is_array($surls_array)&&count($surls_array)>0){
                    foreach($surls_array as $key => $val){
                        $tmp_array = explode('/',$val);
                        $gcid = $tmp_array[4];
                        $data[$k]['flv'][self::$sharpness_array[$key]][] = self::getVideoUrl($gcid);
                    }
                }
                if(is_array($msurls_array)&&count($msurls_array)>0){
                    foreach($msurls_array as $key => $val){
                        $tmp_array = explode('/',$val);
                        $gcid = $tmp_array[4];
                        $data[$k]['mp4'][self::$sharpness_array[$key]][] = self::getVideoUrl($gcid,"mp4");
                    }
                }                                         
            }
        }
        return $data;
    }
}