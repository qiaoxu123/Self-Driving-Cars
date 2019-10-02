function flashvideo(url,width,height) {
	var newwindow2=window.open('','name','width='+(width+20)+',height='+(height+20));
	newwindow2.document.write('<html lang="en"><head><title>Autonomous Intelligent Systems - Videos</title>');
	newwindow2.document.write('<link rel="stylesheet" href="/style.css" type="text/css">');
	newwindow2.document.write('</head><body>');
	newwindow2.document.write('<embed class="extflashvid" src="http://ais.informatik.uni-freiburg.de/videos/player.swf" '+
		'width="'+width+'" height="'+height+'" allowfullscreen="true" '+
		'flashvars="width='+width+'&height='+height+'&file='+url+'&backcolor=#FFFFFF&screencolor=#FFFFFF&autostart=true" />');
	newwindow2.document.write('</body></html>');
	newwindow2.document.close();
}

 
