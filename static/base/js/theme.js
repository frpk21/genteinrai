;(function($) {
    "use strict";
    
    
	var nav_offset_top = $('header').height()+100; 
    /*-------------------------------------------------------------------------------
	  Navbar 
	-------------------------------------------------------------------------------*/

	//* Navbar Fixed  
    function navbarFixed(){
        if ( $('.header_menu_area, .mobile_menu').length ){ 
            $(window).scroll(function() {
                var scroll = $(window).scrollTop();   
                if (scroll >= nav_offset_top ) {
                    $(".header_menu_area, .mobile_menu").addClass("navbar_fixed");
                } else {
                    $(".header_menu_area, .mobile_menu").removeClass("navbar_fixed");
                }
            });
        };
    };
    navbarFixed();
	
	
	$('.menu-list li a').each(function () {
        var $this = $(this);
        $this.on('click', function (e) {
            var has = $this.hasClass('open');
            $('.menu-list li a').removeClass('open');
            if(has) {
                $this.removeClass('open');
            } else {
                $this.addClass('open');
            }
        });
    });
	
	
	/*-------------------------------------------------------------------------------
	  Ajax Forms
	-------------------------------------------------------------------------------*/



	if ($('.js-form').length) {
		$('.js-form').each(function(){
			$(this).validate({
				errorClass: 'error wobble-error',
			    submitHandler: function(form){
		        	$.ajax({
			            type: "POST",
			            url:"mail.php",
			            data: $(form).serialize(),
			            success: function() {
		                	$('.success-message').show();
		                },

		                error: function(){
			                $('.error-message').show();
			            }
			        });
			    }
			});
		});
	}
	
	/*-------------------------------------------------------------------------------
	  Loader
	-------------------------------------------------------------------------------*/



	$(".animsition").animsition({
	   inClass: 'fade-in',
       outClass: 'fade-out',
	   inDuration: 1000,
	   outDuration: 700,
	   linkElement: '.nav.navbar-nav li a, .menu-list li a',
	   // e.g. linkElement: 'a:not([target="_blank"]):not([href^="#"])'
	   loading:true,
	   loadingParentElement: 'body', //animsition wrapper element
	   loadingClass: 'spinner',
	   loadingInner: '<div class="double-bounce1"></div><div class="double-bounce2"></div>', // e.g '<img src="loading.svg" />'
	   timeout: false,
	   timeoutCountdown:5000,
	   onLoadEvent: true,
	   browser: [ 'animation-duration', '-webkit-animation-duration'],
	   // "browser" option allows you to disable the "animsition" in case the css property in the array is not supported by your browser.
	   // The default setting is to disable the "animsition" in a browser that does not support "animation-duration".
	   overlay : false,
	   overlayClass : 'animsition-overlay-slide',
	   overlayParentElement : 'body',
	   transition: function(url){ window.location.href = url; }
	});
	
	
    /*----------------------------------------------------*/
    /*  Main Slider js
    /*----------------------------------------------------*/
    function photography_slider(){
        if ( $('#home_full_slider').length ){
            $("#home_full_slider").revolution({
				sliderType:"standard",
				sliderLayout:"fullscreen",
				dottedOverlay:"none",
				delay:7000,
				autoHeight: 'on',
				minHeight:480,
                navigation: {
					keyboardNavigation:"off",
					keyboard_direction: "horizontal",
					onHoverStop:"off",
					mouseScrollNavigation:"off",
                    mouseScrollReverse:"default",
					touch:{
					  touchenabled:"on",
					  swipe_threshold: 75,
					  swipe_min_touches: 1,
					  swipe_direction: "horizontal",
					  drag_block_vertical: false
					},
					bullets: {
					  enable: true,
					  hide_onmobile: true,

					  direction: "vertical",
					  h_align: "right",
					  v_align: "center",
					  h_offset: 80,
					  v_offset: 0,
					  space: 27
				  	}
				},
                responsiveLevels:[1920,1199,991,768,480],
                visibilityLevels:[1920,960,991,768,480],
                gridwidth:[1170,1024,991,768,480],
                gridheight:[950,768,600,600,480],
                lazyType:"none",
                shadow:0,
                spinner:"off",
                stopLoop:"on",
                stopAfterLoops:0,
                stopAtSlide:1,
                shuffle:"off",
                autoHeight:"off",
                fullScreenAutoWidth:"off",
                fullScreenAlignForce:"off",
                fullScreenOffsetContainer: "",
                fullScreenOffset: "",
                disableProgressBar:"on",
                hideThumbsOnMobile:"off",
                hideSliderAtLimit:0,
                hideCaptionAtLimit:0,
                hideAllCaptionAtLilmit:0,
                debugMode:false,
                fallbacks: {
                    simplifyAll:"off",
                    nextSlideOnWindowFocus:"off",
                    disableFocusListener:false,
                },
				parallax: {
                    type:"mouse",
                    origo:"slidercenter",
                    speed:2000,
                    levels:[2,3,4,5,6,7,12,16,10,50],
                },
            })
        }
    }
    photography_slider();
    /*----------------------------------------------------*/
    /*  Main Slider js
    /*----------------------------------------------------*/
    function full_page_slider(){
        if ( $('#full_page_slider').length ){
            $("#full_page_slider").revolution({
				sliderType:"standard",
				sliderLayout:"fullscreen",
				dottedOverlay:"none",
				delay:7000,
				autoHeight: 'on',
				minHeight:480,
                navigation: {
					keyboardNavigation:"off",
					keyboard_direction: "horizontal",
					onHoverStop:"off",
					mouseScrollNavigation:"off",
                    mouseScrollReverse:"default",
					touch:{
					  touchenabled:"on",
					  swipe_threshold: 75,
					  swipe_min_touches: 1,
					  swipe_direction: "horizontal",
					  drag_block_vertical: false
					},
					bullets: {
					  enable: false,
					  hide_onmobile: true,

					  direction: "vertical",
					  h_align: "right",
					  v_align: "center",
					  h_offset: 80,
					  v_offset: 0,
					  space: 27
				  	},
				},
                responsiveLevels:[1920,1199,991,768,480],
                visibilityLevels:[1920,960,991,768,480],
                gridwidth:[1220,1024,991,768,480],
                gridheight:[903,800,600,700,480],
                lazyType:"none",
                shadow:0,
                spinner:"off",
                stopLoop:"on",
                stopAfterLoops:0,
                stopAtSlide:1,
                shuffle:"off",
                autoHeight:"off",
                fullScreenAutoWidth:"off",
                fullScreenAlignForce:"off",
                fullScreenOffsetContainer: "",
                fullScreenOffset: "0",
                disableProgressBar:"on",
                hideThumbsOnMobile:"off",
                hideSliderAtLimit:0,
                hideCaptionAtLimit:0,
                hideAllCaptionAtLilmit:0,
                debugMode:false,
                fallbacks: {
                    simplifyAll:"off",
                    nextSlideOnWindowFocus:"off",
                    disableFocusListener:false,
                },
            })
        }
    }
    full_page_slider();
	
	
	$(document).ready(function() {
		$('.popup-with-move-anim').magnificPopup({
			type: 'inline',

			fixedContentPos: false,
			fixedBgPos: true,

			overflowY: 'auto',

			closeBtnInside: true,
			preloader: false,

			midClick: true,
			removalDelay: 300,
			mainClass: 'my-mfp-slide-bottom'
		});
	});

    function modal_open1(item) {
        var r = $("#id-titulo-"+String(item)).val();
        var u = $("#id-url-"+String(item)).val();
        $('#id-modal1-titulo').val(r);
        $("#id-modal1-video").html('<source src='+u+'></source>' );
        $('#id-modalvideo1').modal('show')
    }
    function modal_open2(item) {
        var r = $("#id-titulo-"+String(item)).val();
        var v = $("#id-video-"+String(item)).val();
        $('#id-modal2-titulo').val(r);
        $("#id-modal2-video").html('<source src='+v+'></source>' );
        let video = document.getElementById("id-modal2-video");
        video.load();
        video.play();
        $('#id-modalvideo2').modal('show')
    }

    function buscar_tutorial() {
        var r = $("#id_buscar").val();
        var datos = {'buscar':r};
        $.get( "{% url 'generales:upd' %}", datos, function( data ) {
            if (data.errors){
              swal({
                  title: data.errors,
                  showCancelButton: false,
                  confirmButtonClass: 'btn btn-success',
                  //cancelButtonClass: 'btn btn-danger',
                  buttonsStyling: false
              }).catch(swal.noop);
            }
          else {
            var url = "{% url 'generales:updtuto' 123 %}";
            var id = data.buscar;
            document.location.href = url.replace('123', id);
          }
        } )
    }
	/*----------------------------------------------------*/
    /*  Explor Room Slider
    /*----------------------------------------------------*/
    function fillter_slider(){
        if ( $('.fillter_slider').length ){
            $('.fillter_slider').owlCarousel({
                loop:true,
                margin: 6,
                items: 4,
                nav:true,
                autoplay: true,
                smartSpeed: 1500,
                dots:true, 
                navContainer: '.fillter_slider',
                navText: ['<i class="ion-ios-arrow-left"></i>','<i class="ion-ios-arrow-right"></i>'],
                responsiveClass: true,
                responsive: {
                    0: {
                        items: 1,
                    },
                    575: {
                        items: 2,
                    },
                    800: {
                        items: 3,
                    },
                    1200: {
                        items: 4,
                    }
                }
            })
        }
    }
    fillter_slider();
	
	/*----------------------------------------------------*/
    /*  Explor Room Slider
    /*----------------------------------------------------*/
    function testimonials_slider(){
        if ( $('.testimonials_slider').length ){
            $('.testimonials_slider').owlCarousel({
                loop:true,
                margin: 30,
                items: 2,
                nav:true,
                autoplay: true,
                smartSpeed: 1500,
                dots:true, 
				navContainerClass: 'testimonials_slider',
                navText: ['<i class="ion-ios-arrow-left"></i>','<i class="ion-ios-arrow-right"></i>'],
                responsiveClass: true,
                responsive: {
                    0: {
                        items: 1,
                    },
                    768: {
                        items: 2,
                    }
                }
            })
        }
    }
    testimonials_slider();
	
	/*----------------------------------------------------*/
    /*  Explor Room Slider
    /*----------------------------------------------------*/
    function team_slider(){
        if ( $('.team_slider').length ){
            $('.team_slider').owlCarousel({
                loop:true,
                margin: 30,
                items: 4,
                nav:true,
                autoplay: true,
                smartSpeed: 1500,
                dots:true, 
				navContainerClass: 'team_slider',
                navText: ['<i class="ion-ios-arrow-left"></i>','<i class="ion-ios-arrow-right"></i>'],
                responsiveClass: true,
                responsive: {
                    0: {
                        items: 1,
                    },
                    400: {
                        items: 2,
                    },
                    768: {
                        items: 3,
                    },
                    992: {
                        items: 4,
                    }
                }
            })
        }
    }
    team_slider();
	
	/*----------------------------------------------------*/
    /*  Villa Slider
    /*----------------------------------------------------*/
    function villa_slider(){
        if ( $('.villa_slider').length ){
            $('.villa_slider').owlCarousel({
                loop:true,
                margin: 0,
                items: 1,
                nav:true,
                autoplay: true,
                smartSpeed: 1500,
                dots:true, 
				navContainer: '.villa_slider',
                navText: ['<i class="ion-ios-arrow-left"></i>','<i class="ion-ios-arrow-right"></i>'],
                responsiveClass: true,
            })
        }
    }
    villa_slider();
	
	/*----------------------------------------------------*/
    /*  Villa Slider
    /*----------------------------------------------------*/
    function single_slider(){
        if ( $('.blog_g_slider').length ){
            $('.blog_g_slider').owlCarousel({
                loop:true,
                margin: 0,
                items: 1,
                nav:true,
                autoplay: true,
                smartSpeed: 1500,
                dots:true, 
				navContainer: '.blog_g_slider',
                navText: ['<i class="ion-ios-arrow-left"></i>','<i class="ion-ios-arrow-right"></i>'],
                responsiveClass: true,
            })
        }
    }
    single_slider();
	
	
	/*----------------------------------------------------*/
    /*  Explor Room Slider
    /*----------------------------------------------------*/
    function clients_slider(){
        if ( $('.clients_slider').length ){
            $('.clients_slider').owlCarousel({
                loop:true,
                margin: 30,
                items: 5,
                nav:false,
                autoplay: true,
                smartSpeed: 1500,
                dots:true, 
                responsiveClass: true,
                responsive: {
                    0: {
                        items: 1,
                    },
                    400: {
                        items: 2,
                    },
                    575: {
                        items: 3,
                    },
                    768: {
                        items: 4,
                    },
                    1199: {
                        items: 5,
                    }
                }
            })
        }
    }
    clients_slider();
	
	
	
	/*----------------------------------------------------*/
    /* Owl Carousel Cutome Fillter js
    /*----------------------------------------------------*/
	$('.portfolio_filter li').on('click', function() {
        $('.portfolio_filter .active').removeClass('active');
        $(this).closest('li').addClass('active');
        var selector = $(this).attr('data-filter');
        $('.fillter_slider').fadeOut(300);
        $('.fillter_slider').fadeIn(300);
        setTimeout(function() {
            $('.fillter_slider .owl-item').hide();
            $(selector).closest('.fillter_slider .owl-item').show();
        }, 300);
        return false;
    });
	
	
	/*-------------------------------------------------------------------------------
	  Full screen sections 
	-------------------------------------------------------------------------------*/
    if ($('.pagepiling').length > 0){
      	$('.pagepiling').pagepiling({
    		scrollingSpeed: 280,
		    loopBottom:true,
            navigation: {
				'position': 'right_position',
			},
		    afterLoad: function(anchorLink, index){
		    	if (index == 2 || index == 4 || index == 6){   /* 2, 4, 6, - sections with white bacgkgrounds */
		            $('.full_header, .full_footer').removeClass('content-white');
		            $('#pp-nav').removeClass('white');
		    	}
		    	else{
	            	$('.full_header, .full_footer').addClass('content-white');
	            	$('#pp-nav').addClass('white');
	            }
	            
  			}
		});
    	
		
		
        
        /*-------------------------------------------------------------------------------
		   Scroll into sections 
		/-------------------------------------------------------------------------------*/

		$('.pp-scrollable').on('scroll', function () {
    		var scrollTop =$(this).scrollTop();
    		if (scrollTop > 0 ) {
    			$('.full_header, .full_footer').removeClass('content-white');
    		}
    		else{
    			$('.full_header, .full_footer').addClass('content-white');
    		}
		});



		/*-------------------------------------------------------------------------------
		   Scroller navigation
		/-------------------------------------------------------------------------------*/
		$('#pp-nav').addClass('white');

		$('.pp-nav-up').on('click', function(){
			$.fn.pagepiling.moveSectionUp();
		});

		$('.pp-nav-down').on('click', function(){
			$.fn.pagepiling.moveSectionDown();
		});
    };
	
	
	 function latest_project(){
        if ( $('.our_projects_area, .project_full_inner, .blog_inner_fillter, .blog_ms_inner').length ){
            // Activate isotope in container
            $(".projects_inner, .project_full_inner, .blog_ms_inner").imagesLoaded( function() {
                $(".projects_inner, .project_full_inner, .blog_ms_inner").isotope({
                    layoutMode: 'masonry',
                    animationOptions: {
                        duration: 750,
                        easing: 'linear'
                    }
                }); 
            });
			
			$(".blog_inner_fillter").imagesLoaded( function() {
                $(".blog_inner_fillter").isotope({
                    layoutMode: 'fitRows',
                    animationOptions: {
                        duration: 750,
                        easing: 'linear'
                    }
                }); 
            });
			
            // Add isotope click function
            $(".isotope_fillter li").on('click',function(){
                $(".isotope_fillter li").removeClass("active");
                $(this).addClass("active");

                var selector = $(this).attr("data-filter");
                $(".projects_inner, .project_full_inner, .blog_inner_fillter, .blog_ms_inner").isotope({
                    filter: selector,
                    animationOptions: {
                        duration: 450,
                        easing: "linear",
                        queue: false,
                    }
                });
                return false;
            });
        }
    }
    latest_project();
	
	
		$(".ms_project_inner").imagesLoaded( function() {
			$(".ms_project_inner").isotope({
				layoutMode: 'masonry',
				percentPosition:true,
				masonry: {
					columnWidth: '.grid_sizer',
				}      
			}); 
		});
	
	
	
	
	$('.navbar-toggle').on('click', function() {
        $('body').removeClass('menu-is-closed').addClass('menu-is-opened');
    });
    $('.close-menu, .click-capture').on('click', function() {
        $('body').removeClass('menu-is-opened').addClass('menu-is-closed');
        $('.menu-list ul').slideUp(300);
    });
    var dropToggle = $('.menu-list > li').has('ul').children('a');
    dropToggle.on('click', function() {
        dropToggle.not(this).closest('li').find('ul').slideUp(200);
        $(this).closest('li').children('ul').slideToggle(200);
        return false;
    });
	
	
	$('.bar_menu').on('click', function() {
        $('body').removeClass('menu-is-closed').addClass('menu-is-opened');
    });
	
	$('#pp-nav').remove().appendTo('.animsition').prepend('<div class="pp-nav-up icon-chevron-up"></div>').append('<div class="pp-nav-down icon-chevron-down"></div>').addClass('white right-boxed hidden-xs');
	
	
	
})(jQuery)











