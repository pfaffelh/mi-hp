/* https://uni-freiburg.de/math/wp-content/themes/ufr-main-theme/assets/js/frontend-header.js?ver=0.12.0 */
(()=> {
		var e= {
			357:()=> {
				const e=["dark", "bl-dark"], t=localStorage.theme, r=window.matchMedia("(prefers-color-scheme: dark)"); function o() {
					"dark"===t|| !t&&r.matches?document.documentElement.classList.add(...e):document.documentElement.classList.remove(...e)
				}

				o(), r.addEventListener("change", o)
			}
		}

		, t= {}

		; function r(o) {
			var a=t[o]; if(void 0 !==a)return a.exports; var n=t[o]= {
				exports: {}
			}

			; return e[o](n, n.exports, r), n.exports
		}

		r.n=e=> {
			var t=e&&e.__esModule?()=>e.default:()=>e; return r.d(t, {
				a:t
			}), t
	}

	, r.d=(e, t)=> {
		for(var o in t)r.o(t, o)&& !r.o(e, o)&&Object.defineProperty(e, o, {
			enumerable: !0, get:t[o]
		})
}

, r.o=(e, t)=>Object.prototype.hasOwnProperty.call(e, t), (()=> {
		"use strict"; r(357)
	})()
})();
//# sourceMappingURL=frontend-header.js.map