var casper = require('casper').create({
	verbose: 'verbose',
	logLevel: 'debug',
	pageSettings : {
		userAgent : 'Mozilla/4.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.7) Gecko/2008398325 Firefox/3.1.4'
	},
	clientScripts : ["D:/kevin/projects/production/screenshot/static/js/jquery.min.js"]
});

var utils = require("utils"),
	http = require('http'),
	fs = require('fs');

var script_name = "capture.js"; // just for logging

var USER_AGENTS = {
	"mobile" : [
		"Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
		"Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
		"Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
		"Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile"
	],
	"desktop" :[
		"Mozilla/4.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.7) Gecko/2008398325 Firefox/3.1.4",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0",
		"Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0",
		"Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
		"Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
		"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
		"Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))",
		"Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
		"Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
		"Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
		"Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
		"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
		"Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
	]
};

var rest_url_root = "http://localhost:8080/"

var app = {
	FS : null, // file system module for logging.
	OUTPUT_DIR : "save",
	IMG_EXT : ".png",
	/*
		args:
			casper - casperjs instance
			url - website url to scrape
			size - a width and height object map e.g { width: 100, height: 200 }
			isMobile - boolean : set the user agent
			filename - string : full/absolute file path without the file extension
	*/
	getScreenShot: function(casper, url, size, isMobile, filepath){
		casper.open(url, function(){})
		casper.then(function(){
			this.viewport(size.width*1, size.height*1);
		});
		casper.then(function(){
			var ua = app.getRandomUserAgent(isMobile);
			casper.userAgent(ua);
		})
		casper.thenOpen(url, function(response){
			if(response.status){
				if(response.status == 400)
					this.emit("not_found", response)
				else
					app.status_code = 1
			}else{
				this.emit("not_found", response);
			}
		});
		casper.then(function(){
			this.capture(filepath, {
				top: 0,
				left: 0,
				width : size.width*1,
				height : size.height*1
			});
		});
	},
	random : function(length){
		return Math.floor((Math.random() * length) + 1); 
	},
	getRandomUserAgent : function(isMobile){
		if(isMobile){
			return USER_AGENTS.mobile[this.random(USER_AGENTS.mobile.length)];
		}else{
			return USER_AGENTS.desktop[this.random(USER_AGENTS.desktop.length)];
		}
	},
	withHttp: function(url){
		var temp = url.replace("http://","");
		return "http://"+temp;
	},
	init : function(casper){
		app.LOG_FILE = "log/" + ((new Date()).getTime()) + ".log";
		app.FS = require('fs');

		if(casper.cli.has('help') || (casper.cli.args.length == 0 && !casper.cli.has('urls') && !casper.cli.has('file'))){
			casper.echo("");
			casper.echo("=================================================");
			casper.echo("");
			casper.echo("Usage : ");
			casper.echo("");
			casper.echo("casperjs " + script_name + " http://example.com ");
			casper.echo("casperjs " + script_name + " --urls=http://example.com,http://example2.com");	
			casper.echo("");
			casper.echo("Other arguments : ");
			casper.echo("");
			casper.echo("--mobile            - set the user agent as mobile and the min screen");
			casper.echo("                      resolution is 426 x 320 and the max screen");
			casper.echo("                      resolution is 600 x 800");
			casper.echo("--desktop           - set the user agent as desktop and the min"); 
			casper.echo("                      screen resolution is 960 x 720 and the max");
			casper.echo("                      screen resolution is 1280 x 1024");
			casper.echo("--responsive        - set the user agent as desktop and the min and");
			casper.echo("                      max screen resolution are similar to --mobile");
			casper.echo("                      and --desktop");
			casper.echo("--size              - set screen size of the viewport --sizes=w1xh1,w2xh2,...");
			casper.echo("                      e.g --size=420x600");
			casper.echo("                      Add --mobile or --web(default) to setup the user agent");
			casper.echo("--output            - path where the screenshots are saved.");
			casper.echo("                      Default is where the capture.js lies.");
			casper.echo("");
			casper.echo("=================================================");
			casper.echo("");
			return false;
		}		
		return true;
	},
	setEvents : function(casper){
		casper.on('not_found', function(resource){
			app.status_code = -1
			casper.echo('[Custom Log] - 404 status on url : ' + resource.url);
		});
	},
	getArgs : function(casper){
		var data = {
			url : '',
			domain : '',
			size : {width: 1024, height: 768},
			isMobile: false,
			filename : '',
			filesrc : '',
			status_code : '0',
			message : ''
		}

		data.url = casper.cli.get(0)
		data.domain = data.url.replace("http://", "")
		data.domain = data.domain.replace("://", "")
		data.domain = data.domain.replace("/","_")
		data.url = "http://" + data.domain;
 
		if(casper.cli.has("size")){
			temp = casper.cli.get("size").split("x")
			if(temp.length > 1){
				data.size = {width : temp[0], height: temp[1]}
			}
		}

		data.isMobile = casper.cli.has("mobile")

		if(casper.cli.has("output")){
			app.OUTPUT_DIR = casper.cli.get("output").trim();
			var lastChar = app.OUTPUT_DIR.charAt(app.OUTPUT_DIR.length - 1);
			if(lastChar !== '/' && lastChar !== '\\')
				app.OUTPUT_DIR = app.OUTPUT_DIR + "/";
		}
		data.filename = data.domain  + "_" + data.size.width + "x" + data.size.height + "_" + (new Date()).getTime() + app.IMG_EXT;
		data.filesrc = app.OUTPUT_DIR + "/" + data.filename
		
		if(casper.cli.has("filename")){
			data.filename = casper.cli.get("filename")
			data.filesrc = app.OUTPUT_DIR + "/" + data.filename 
		}

		return data
	}
}

//initialize
var bcontinue = app.init(casper);

if(!bcontinue) casper.exit();

var args = app.getArgs(casper)

app.setEvents(casper);

casper.start();

casper.echo('[Custom Log] - Start screenshot process of url : ' + args.url);

casper.then(function(){
	app.getScreenShot(casper, args.url, args.size, args.isMobile, args.filesrc)
})

casper.run(function(){
	casper.echo("[Custom Log] - End screenshot process of url : " + args.url);
	this.exit();
});
