//fixed-nav
$(document).on("scroll",function(){
	if($(document).scrollTop()>100){ 
		$(".abc-01").removeClass("large").addClass("small");
	}
	else{
		$(".abc-01").removeClass("small").addClass("large");
	}
});


//back-top
$(function(){
	$(window).scroll(function(){
		var _top = $(window).scrollTop();
		if(_top>300){
			$('.back_top').fadeIn(600);
		}else{
			$('.back_top').fadeOut(600);
		}
	});
	$(".back_top").click(function(){
		$("html,body").animate({scrollTop:0},500);
	});
});


$(window).load(function(){

	$("#flexiselDemo2").flexisel({
		visibleItems: 4,
		animationSpeed: 1000,
		autoPlay: true,
		autoPlaySpeed: 5500,    		
		pauseOnHover: true,
		enableResponsiveBreakpoints: true,
    	responsiveBreakpoints: { 
    		portrait: { 
    			changePoint:405,
    			visibleItems: 1
    		}, 
    		landscape: { 
    			changePoint:620,
    			visibleItems: 2
    		},
    		tablet: { 
    			changePoint:768,
    			visibleItems: 3
    		}
    	}
    });
	
});

$(document).ready(function(){

    $("#floatShow").bind("click",function(){
	
        $("#onlineService").show();
		
        $("#floatShow").attr("style","display:none");
        $("#floatHide").attr("style","display:block");
		
        return false;
    });
	
    $("#floatHide").bind("click",function(){
	
        $("#onlineService").hide();
		
        $("#floatShow").attr("style","display:block");
        $("#floatHide").attr("style","display:none");
		
        return false;
    });
  
});

		$(document).ready(function() {
		//Horizontal Tab
	    $('#parentHorizontalTab02').easyResponsiveTabs({
	    	type: 'default', //Types: default, vertical, accordion
	        width: 'auto', //auto or any width like 600px
	        fit: true, // 100% fit in a container
	        tabidentify: 'hor_2', // The tab groups identifier
	        activate: function(event) { // Callback function if tab is switched
	        	var $tab = $(this);
	            var $info = $('#nested-tabInfo');
	            var $name = $('span', $info);
	            $name.text($tab.text());
	            $info.show();
	        }
	    });

	});
$(document).ready(function() {
		//Horizontal Tab
	    $('#parentHorizontalTab01').easyResponsiveTabs({
	    	type: 'default', //Types: default, vertical, accordion
	        width: 'auto', //auto or any width like 600px
	        fit: true, // 100% fit in a container
	        tabidentify: 'hor_1', // The tab groups identifier
	        activate: function(event) { // Callback function if tab is switched
	        	var $tab = $(this);
	            var $info = $('#nested-tabInfo');
	            var $name = $('span', $info);
	            $name.text($tab.text());
	            $info.show();
	        }
	    });

	});

	$(document).ready(function() {
		//Horizontal Tab
	    $('#parentHorizontalTab03').easyResponsiveTabs({
	    	type: 'default', //Types: default, vertical, accordion
	        width: 'auto', //auto or any width like 600px
	        fit: true, // 100% fit in a container
	        tabidentify: 'hor_3', // The tab groups identifier
	        activate: function(event) { // Callback function if tab is switched
	        	var $tab = $(this);
	            var $info = $('#nested-tabInfo');
	            var $name = $('span', $info);
	            $name.text($tab.text());
	            $info.show();
	        }
	    });

	});
function enterIn(evt) {
    var evt = evt ? evt : (window.event ? window.event : null);//兼容IE和FF
    if (evt.keyCode == 13) {
        $(".btn_search1").click();
    }
}
$(function () {
     $(".btn_search1").click(function () { 
        svalue = $("input[name=search_keyword]").val();
        if (svalue) {
//            svalue =  svalue.replace(/\s/g,"-");
            window.location.href = "/" + svalue + "_c0_ss";
        } else {
            return '';
        }
    });
    
    $(".btn_search2").click(function () { 
        bvalue = $("input[name=search_brand]").val();
        if (bvalue) {
            bvalue =  bvalue.replace(/\s/g,"-");
            window.location.href = "/" + bvalue + "_sbr";
        } else {
            return '';
        }
    });
});
$("#email_form").validate({
        onkeyup: false,
        rules: {
            "msg_name": {
                required: true,
                ch: true
            },
            "msg_email": {
                required: true,
                email: true,
                remote: {
                    type: "GET",
                    url: "/common/ajax/findemail",
                    data: {
                        msg_email: function () {
                            return $("#msg_email").val();
                        }
                    }
                }
            },
            "msg_title": {
                required: true,
                ch: true
            },
            "msg_content": {
                required: true,
                ch: true
            },
            "auth_code": {
                required: true,
                remote: {
                    type: "GET",
                    url: "/common/ajax/judgeauthcode",
                    data: {
                        auth_code: function () {
                            return $("#auth_code1").val();
                        }
                    }
                }
            }
        },
        messages: {
            "msg_name": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill your name',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English'
            },
            "msg_email": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill your email',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English',
                remote: jQuery.format('<img src="/images/front/error.gif" width="12" height="12" />It\'s alerdy exist!please change!')
            },
            "msg_title": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill the title',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English'
            },
            "msg_content": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill the content',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English'
            },
            "auth_code": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />The auth code is required',
                remote: jQuery.format('<img src="/images/front/error.gif" width="12" height="12" />It\'s wrong,please reset')
            }
        }
    });
    $("#email_form2").validate({
        onkeyup: false,
        rules: {
            "msg_name": {
                required: true,
                ch: true
            },
            "msg_email": {
                required: true,
                email: true,
                remote: {
                    type: "GET",
                    url: "/common/ajax/findemail",
                    data: {
                        msg_email: function () {
                            return $("#msg_email").val();
                        }
                    }
                }
            },
            "msg_title": {
                required: true,
                ch: true
            },
            "msg_content": {
                required: true,
                ch: true
            },
            "auth_code": {
                required: true,
                remote: {
                    type: "GET",
                    url: "/common/ajax/judgeauthcode",
                    data: {
                        auth_code: function () {
                            return $("#auth_code1").val();
                        }
                    }
                }
            }
        },
        messages: {
            "msg_name": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill your name',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English'
            },
            "msg_email": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill your email',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English',
                remote: jQuery.format('<img src="/images/front/error.gif" width="12" height="12" />It\'s alerdy exist!please change!')
            },
            "msg_title": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill the title',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English'
            },
            "msg_content": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill the content',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English'
            },
            "auth_code": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />The auth code is required',
                remote: jQuery.format('<img src="/images/front/error.gif" width="12" height="12" />It\'s wrong,please reset')
            }
        }
    });
    $("#email_form3").validate({
        onkeyup: false,
        rules: {
            "msg_name": {
                required: true,
                ch: true
            },
            "msg_email": {
                required: true,
                email: true,
                remote: {
                    type: "GET",
                    url: "/common/ajax/findemail",
                    data: {
                        msg_email: function () {
                            return $("#msg_email").val();
                        }
                    }
                }
            },
            "msg_title": {
                required: true,
                ch: true
            },
            "msg_content": {
                required: true,
                ch: true
            },
            "auth_code": {
                required: true,
                remote: {
                    type: "GET",
                    url: "/common/ajax/judgeauthcode",
                    data: {
                        auth_code: function () {
                            return $("#auth_code1").val();
                        }
                    }
                }
            }
        },
        messages: {
            "msg_name": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill your name',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English'
            },
            "msg_email": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill your email',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English',
                remote: jQuery.format('<img src="/images/front/error.gif" width="12" height="12" />It\'s alerdy exist!please change!')
            },
            "msg_title": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill the title',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English'
            },
            "msg_content": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />please fill the content',
                ch: '<img src="/images/front/error.gif" width="12" height="12" />please fill in English'
            },
            "auth_code": {
                required: '<img src="/images/front/error.gif" width="12" height="12" />The auth code is required',
                remote: jQuery.format('<img src="/images/front/error.gif" width="12" height="12" />It\'s wrong,please reset')
            }
        }
    });