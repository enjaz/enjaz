/**
 *	SimpleSlider
 *
 *	Plugin by: Arlind Nushi
 *	www.arlindnushi.com
 *
 *	Version: 1.0
 *	Date: 2/11/14
 */

;(function($, window, undefined){
	
	$.fn.neonSlider = function(opts)
	{
		return this.each(function(i)
		{
			var 
			// public properties
			def = {
				itemSelector: '> .item',
				activeClass: 'active',
				autoSwitch: 0,
				resizeContainerDuration: .5,
				outDuration: .4,
				inDuration: .7,
				outAnimation: {
					small: {
						top: -25,
						opacity: 0
					},
					
					h2: {
						opacity: 0,
						scale: .8
					},
					
					p: {
						top: 25,
						opacity: 0
					},
					
					img: {
						opacity: 0
					}
				},
				inAnimation: {
					small: {
						top: -40,
						opacity: 0
					},
					
					h2: {
						top: -25,
						opacity: 0
					},
					
					p: {
						top: -50,
						opacity: 0
					},
					
					img: {
						opacity: 0,
						scale: .8
					}
				},
				
				prev: '.prev',
				next: '.next'
			},
			// private properties
			p = {
				items: null,
				items_length: 0,
				current: 0,
				as: {pct: 0},
				asInstance: null
			},
			methods = {
				init: function(opts)
				{
					// Extend Options
					$.extend(def, opts);
					
					// Set Container
					p.container = $(this);
					
					p.items = p.container.find(def.itemSelector);
					p.items_length = p.items.length;
					
					p.current = p.items.filter('.' + def.activeClass).index();
					
					if(p.current < 0)
						p.current = 0;
					
					p.items.removeClass(def.activeClass);
					p.items.eq(p.current).addClass(def.activeClass);
					
					// Set Heights
					p.items.each(function(i, el)
					{
						var $slide = $(el);
						
						if( ! $slide.hasClass(def.activeClass))
						{
							$slide.data('height', $slide.outerHeight());
							$slide.removeClass(def.activeClass);
						}
						else
						{
							$slide.data('height', $slide.outerHeight());
						}
					});
					
					
					// Next Prev
					p.container.find(def.next).on('click', function(ev)
					{
						ev.preventDefault();
						
						methods.next();
					});
					
					p.container.find(def.prev).on('click', function(ev)
					{
						ev.preventDefault();
						
						methods.next(-1);
					});
					
					
					// Auto Switch
					if(def.autoSwitch && typeof def.autoSwitch == 'number')
					{
						methods.autoswitch(def.autoSwitch);
					}
				},
				
				goTo: function(index)
				{
					index = Math.abs(index) % p.items_length;
					
					if(index == p.current || p.container.data('is-busy'))
						return false;
					
					var $current = p.items.eq(p.current),
						$next = p.items.eq(index),
						
						_ch = $current.data('height'),
						_nh = $next.data('height');
					
					p.container.data('is-busy', 1);
					p.container.height( _ch );
					
					// Resize Container
					TweenMax.to(p.container, def.resizeContainerDuration, {css: {height: _nh}});
					
					// Hide Slide
					var $small = $current.find('small'),
						$h2    = $current.find('h2'),
						$p     = $current.find('p'),
						$img   = $current.find('.slide-image img');
					
					TweenMax.to($small, def.outDuration, {css: def.outAnimation.small, delay: def.inDuration/2});
					TweenMax.to($h2, def.outDuration, {css: def.outAnimation.h2, delay: def.inDuration/2});
					TweenMax.to($p, def.outDuration, {css: def.outAnimation.p, delay: def.inDuration/2});
					TweenMax.to($img, def.outDuration, {css: def.outAnimation.img});
					
					// Next Slide
					setTimeout(function()
					{
						$current.removeClass(def.activeClass);
						$small.add($h2).add($p).add($img).attr('style', '');
						
						$small = $next.find('small'),
						$h2    = $next.find('h2'),
						$p     = $next.find('p'),
						$img   = $next.find('.slide-image img');
						
						$next.addClass(def.activeClass);
											
						TweenMax.from($small, def.inDuration, {css: def.inAnimation.small, delay: def.inDuration/2});
						TweenMax.from($h2, def.inDuration, {css: def.inAnimation.h2, delay: def.inDuration/2});
						TweenMax.from($p, def.inDuration, {css: def.inAnimation.p, delay: def.inDuration/2});
						TweenMax.from($img, def.inDuration, {css: def.inAnimation.img});
						
						// Animation End
						setTimeout(function()
						{
							p.container.data('is-busy', 0);
							
							$small.add($h2).add($p).add($img).attr('style', '');
							p.container.css('height', '');
							
							p.current = $next.index();
							
						}, 1000 * (def.inDuration + def.inDuration/2));
						
					}, 1000 * (def.inDuration + .3));
					
					return true;
				},
				
				
				next: function(rev)
				{
					var next = p.current + 1;
					
					if(rev)
					{
						next = p.current - 1;
						
						if(next < 0)
							next = p.items_length - 1;
					}
					
					methods.goTo(next);
				},
				
				
				autoswitch: function(length)
				{
					p.asInstance = TweenMax.to(p.as, length, {pct: 100, onComplete: function()
						{
							p.as.pct = 0;
							p.asInstance.restart();
							
							methods.next();
						}
					});
					
					p.container.hover(function()
					{
						p.asInstance.pause();
					}, 
					function()
					{
						p.asInstance.resume();
					});
					
				}
			};
			
			
			if(typeof opts == 'object')
			{				
				methods.init.apply(this, [opts]);
			}
			
		});
	}
	
})(jQuery, window);