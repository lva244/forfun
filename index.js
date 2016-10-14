var request = require('request');  
var cheerio = require('cheerio');
var FB = require('fb');
FB.options({version: 'v2.2'});

var url_1 = 'https://www.chotot.com/tp-ho-chi-minh/mua-ban-may-tinh-laptop/i5?f=p&o=1#';

var token = "EAAAACZAVC6ygBAPbZBSRzSzZAJ1TC16wcerq9vuuLsUBmZAAaVaGEQZCgyV5EU2RuHsmC1zzB5n5rgIig2qApQOKlZCg9W3XpkYsSa4bNhyZAgnG0Nn6GNdrA78zrKL0asBFHNxxFV5dS7at1NgfarA6VhhX9M58MEhselvq9eNLAZDZD";

var arr = [];
var arr_sub = [];
var arr_temp = [];
var arr_links = [];

var query = function(){ 

	request(url_1, function(err, response, body){  
	  if (!err && response.statusCode == 200) {
	    var $ = cheerio.load(body);
	    var all = $(".chotot-list-row");

	    $('.ad-subject').each(function(i, element){
		    arr_links.push($(this).attr("href"));
		});

	    for(var i=0;i<all.length;i++)
	    {
	    	var data = $(".chotot-list-row").eq(i).text();
		    arr_sub = data.split("                 ");
		    arr_temp = arr_sub[1].split("        ");
		    arr_sub[0] = arr_temp[1];
		    arr_sub[1] = arr_temp[2];
		    for(var j=0;j<arr_sub.length;j++)
		    {
		    	arr_sub[j] = arr_sub[j].trim();
		    }
		    
		    if((arr_sub[4].includes("1 giờ") &&  !arr_sub[4].includes("phút")) || (!arr_sub[4].includes("giờ") &&  arr_sub[4].includes("phút")))
		    {
		    	var price = arr_sub[2];
				price = price.replace("đ", "");
			    price = price.split('.').join('');
			    if(price<=3500000)
			    {
			    	arr_sub.push(arr_links[i]);
			    	arr.push(arr_sub);
				}
		    }

		}

		//Outside loop
		for(var i=0;i<arr.length;i++)
		{
			FB.setAccessToken('EAAAACZAVC6ygBALZAZAuO7hXBu9CpwdhXLZCMrW1MkO3OmnyIJljUFZCYFYjrrSTEB6iQl6zZCfdFvgY19iArabs92AjoB9va4yVi5T7AxCIEj19gM6akzQUNCIdxfZA70jXUQOPXFkJyE5etnpD5dHN1eR0AKiokL5z68zzTMCiQZDZD');
 
			var body = arr[i][0] + '\r\n' + arr[i][2] + '\r\n' + arr[i][3] + '\r\n' + arr[i][4] + '\r\n' + arr[i][5];
			console.log(body);
			FB.api('135080390290309/feed', 'post', { message: body }, function (res) {
			  if(!res || res.error) {
			    console.log(!res ? 'error occurred' : res.error);
			    return;
			  }
			  console.log('Post Id: ' + res.id);
			});

		}
	  }

	  else console.log('Error');
	})
};

setInterval(function(){ query(); }, 53 * 60 * 1000);
