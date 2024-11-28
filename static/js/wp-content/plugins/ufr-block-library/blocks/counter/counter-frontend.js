/* https://uni-freiburg.de/math/wp-content/plugins/ufr-block-library/blocks/counter/counter-frontend.js?ver=d9496b61ab2d7d3c0034 */

(()=> {
		"use strict"; const t=window.wp.i18n, n=((0, t._x)("Linear", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Quad", "animation easing function", "ufr-block-library"), (0, t._x)("Ease Out Quad", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Out Quad", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Cubic", "animation easing function", "ufr-block-library"), (0, t._x)("Ease Out Cubic", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Out Cubic", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Quart", "animation easing function", "ufr-block-library"), (0, t._x)("Ease Out Quart", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Out Quart", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Quint", "animation easing function", "ufr-block-library"), (0, t._x)("Ease Out Quint", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Out Quint", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Sine", "animation easing function", "ufr-block-library"), (0, t._x)("Ease Out Sine", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Out Sine", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Expo", "animation easing function", "ufr-block-library"), (0, t._x)("Ease Out Expo", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Out Expo", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Circ", "animation easing function", "ufr-block-library"), (0, t._x)("Ease Out Circ", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Out Circ", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Back", "animation easing function", "ufr-block-library"), (0, t._x)("Ease Out Back", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Out Back", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Elastic", "animation easing function", "ufr-block-library"), (0, t._x)("Ease Out Elastic", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Out Elastic", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Bounce", "animation easing function", "ufr-block-library"), (0, t._x)("Ease Out Bounce", "animation easing function", "ufr-block-library"), (0, t._x)("Ease In Out Bounce", "animation easing function", "ufr-block-library"), Math.PI/2), i=t=>1-e(1-t), e=t=>t<4/11?121*t*t/16:t<8/11?9.075*t*t-9.9*t+3.4:t<.9?4356/361*t*t-35442/1805*t+16061/1805:10.8*t*t-20.52*t+10.72, a= {
			linear:t=>t, easeInQuad:t=>t*t, easeOutQuad:t=>-t*(t-2), easeInOutQuad:t=>t<.5?2*t*t:-2*t*t+4*t-1, easeInCubic:t=>t*t*t, easeOutCubic:t=> {
				const n=t-1; return n*n*n+1
			}

			, easeInOutCubic:t=> {
				if(t<.5)return 4*t*t*t; const n=2*t-2; return.5*n*n*n+1
			}

			, easeInQuart:t=>t*t*t*t, easeOutQuart:t=> {
				const n=t-1; return n*n*n*(1-t)+1
			}

			, easeInOutQuart:t=> {
				if(t<.5)return 8*t*t*t*t; const n=t-1; return-8*n*n*n*n+1
			}

			, easeInQuint:t=>t*t*t*t*t, easeOutQuint:t=> {
				const n=t-1; return n*n*n*n*n+1
			}

			, easeInOutQuint:t=> {
				if(t<.5)return 16*t*t*t*t*t; const n=2*t-2; return.5*n*n*n*n*n+1
			}

			, easeInSine:t=>Math.sin((t-1)*n)+1, easeOutSine:t=>Math.sin(t*n), easeInOutSine:t=>.5*(1-Math.cos(t*Math.PI)), easeInExpo:t=>0===t?t:Math.pow(2, 10*(t-1)), easeOutExpo:t=>1===t?t:1-Math.pow(2, -10*t), easeInOutExpo:t=>0===t||1===t?t:t<.5?.5*Math.pow(2, 20*t-10):-.5*Math.pow(2, -20*t+10)+1, easeInCirc:t=>1-Math.sqrt(1-t*t), easeOutCirc:t=>Math.sqrt((2-t)*t), easeInOutCirc:t=>t<.5?.5*(1-Math.sqrt(1-t*t*4)):.5*(Math.sqrt(-(2*t-3)*(2*t-1))+1), easeInBack:t=>t*t*t-t*Math.sin(t*Math.PI), easeOutBack:t=> {
				const n=1-t; return 1-(n*n*n-n*Math.sin(n*Math.PI))
			}

			, easeInOutBack:t=> {
				if(t<.5) {
					const n=2*t; return.5*(n*n*n-n*Math.sin(n*Math.PI))
				}

				const n=1-(2*t-1); return.5*(1-(n*n*n-n*Math.sin(n*Math.PI)))+.5
			}

			, easeInElastic:t=>Math.sin(13*n*t)*Math.pow(2, 10*(t-1)), easeOutElastic:t=>Math.sin(-13*n*(t+1))*Math.pow(2, -10*t)+1, easeInOutElastic:t=>t<.5?.5*Math.sin(13*n*(2*t))*Math.pow(2, 10*(2*t-1)):.5*(Math.sin(-13*n*(2*t-1+1))*Math.pow(2, -10*(2*t-1))+2), easeInBounce:i, easeOutBounce:e, easeInOutBounce:t=>t<.5?.5*i(2*t):.5*e(2*t-1)+.5
		}

		; class s {
			#t; #n; #i; #e; #a; #s; #o; #r=1e3/75; #u=0; debug= !1; debugValues= {
				outputTimelineTimestamps:[], outputTimelineProgress:[], outputTimelineValues:[]
			}

			; constructor(t, n, i) {
				var e, a; if(this.#t=t, this.#n=t.querySelector("div :first-child > span:nth-child(2)"), this.#e=this.#c(), this.#s=i, void 0===this.#e.precision||isNaN(this.#e.precision)) {
					var s, o; const t=null !==(s=this.#e.start.toString().split(".")[1]?.length)&&void 0 !==s?s:0, n=null !==(o=this.#e.end.toString().split(".")[1]?.length)&&void 0 !==o?o:0; this.#e.precision=Math.max(t, n)
				}

				n?this.#n.textContent=this.#e.end.toString():(this.#o=new Intl.NumberFormat(this.#s, {
						minimumFractionDigits:null !==(e=this.#e.precision)&&void 0 !==e?e:0, maximumFractionDigits:null !==(a=this.#e.precision)&&void 0 !==a?a:0
					}), this.#l(), this.#n.style.display="inline-block", this.#h())
		}

		#h() {
			this.#n.textContent=this.#e.start.toString(); const t=new IntersectionObserver((n=> {
						n.forEach((n=> {
									n.isIntersecting&&(this.#a=window.setInterval((()=> {
													this.#p()
												}), this.#r), t.unobserve(this.#n))
								}))
					})); t.observe(this.#n)
		}

		#p() {
			if(this.#u+=this.#r, this.#u<this.#e.delay)return; const t=this.#u-this.#e.delay; if(t>this.#e.duration)return this.#n.textContent=this.#o.format(this.#e.end), this.#n.style.width="auto", void 0 !==this.#a&&window.clearInterval(this.#a), void( !0===this.debug&&this.debugValues.outputTimelineValues.map(((t, n)=>console.log(`${t} at progress ${this.debugValues.outputTimelineProgress[n]} after ${this.debugValues.outputTimelineTimestamps[n]}ms`)))); const n=((t, n, i, e)=>n+(i-n)*((t, n)=>(0, a[t])(n))(t, e))(this.#e.easing, this.#e.start, this.#e.end, t/this.#e.duration); this.#n.textContent=this.#o.format(n); const i=this.#n.textContent.replaceAll(/\d/g, "0"); this.#i.textContent=i, this.#n.style.width=`${this.#i.offsetWidth}px`,  !0===this.debug&&(this.debugValues.outputTimelineTimestamps.push(this.#u), this.debugValues.outputTimelineProgress.push(t), this.debugValues.outputTimelineValues.push(n))
		}

		#l() {
			this.#i=this.#n.cloneNode( !0), this.#i.textContent="", this.#i.style.visibility="hidden", this.#i.style.position="absolute", this.#i.style.zIndex="-1", this.#i.style.whiteSpace="nowrap", this.#n.parentElement?.appendChild(this.#i)
		}

		#c() {
			var t; const n= {}

			, i=(null !==(t=this.#t.dataset.counter)&&void 0 !==t?t:"").split(";").map((t=>t.trim())).filter((t=>t)); for(const t of i) {
				const[i, e]=t.split(":").map((t=>t.trim())); if("duration" !==i&&"delay" !==i)if("easing" !==i)if("start" !==i&&"end" !==i)if("precision" !==i)n[i]=e; else {
					const t=parseInt(e); if(t<0||t>100)continue; n[i]=t
				}

				else n[i]=parseFloat(e); else n[i]=e; else n[i]=this.#d(e)
			}

			return n
		}

		#d(t) {
			const n=t.endsWith("ms")?"ms":"s", i=parseFloat(t); return"ms"===n?i:1e3*i
		}
	}

	class o {
		static#f=null; #m; constructor() {
			var t; if(o.#f)throw new Error("CounterManager is a singleton class and already has an instance. Use .getInstance() instead."); this.#m=[], this.prefersReducedMotion=null !==(t=window.matchMedia("(prefers-reduced-motion: reduce)")?.matches)&&void 0 !==t&&t, this.languageCode=document.documentElement.lang||"en-US", this.#m=Array.from(document.querySelectorAll("[data-counter]")).map((t=>new s(t, this.prefersReducedMotion, this.languageCode)))
		}

		static getInstance() {
			return o.#f||(o.#f=new o), o.#f
		}
	}

	document.addEventListener("DOMContentLoaded", (()=> {
				o.getInstance()
			}))
})();