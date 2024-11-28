/* https://uni-freiburg.de/math/wp-content/plugins/ufr-block-library/blocks/accordion/accordion-frontend.js */

(()=> {
		class t {
			constructor(t, e) {
				this.element=t, this.accordion=e; const i=Array.from(this.element.querySelectorAll("button")); if(8===i.length)this.searchEnabled= !0, [this.searchOpenButton, this.searchCloseButton, this.clearSearchButton, this.submitSearchButton, this.openAllButton, this.closeAllButton, this.openAllButtonMobile, this.closeAllButtonMobile]=i; else {
					if(4 !==i.length)return; this.searchEnabled= !1, [this.openAllButton, this.closeAllButton, this.openAllButtonMobile, this.closeAllButtonMobile]=i
				}

				this.form=this.element.querySelector("form"), this.inputField=this.element.querySelector("input[type=text]"), this.inputField&&(this.inputField.value=""), "horizontal" !==this.accordion.options.direction?(this.displayOpenAllButton=this.accordion.options.multiple, this.displayCloseAllButton=this.accordion.options.collapsible):(this.displayOpenAllButton= !0, this.displayCloseAllButton= !0), this.searchOpenButton?.addEventListener("click", (()=> {
							this.openSearch()

						})), this.searchCloseButton?.addEventListener("click", (()=> {
							this.closeSearch()

						})), this.clearSearchButton?.addEventListener("click", (t=> {
							t.preventDefault(), this.clearSearch()

						})), this.inputField?.addEventListener("keydown", (t=> {
							"Enter"===t.key&&(t.preventDefault(), this.handleInput())

						})), this.inputField?.addEventListener("input", (()=> {
							this.handleInput()

						})), this.submitSearchButton?.addEventListener("click", (t=> {
							t.preventDefault(), this.handleInput()

						})), this.displayOpenAllButton&&(this.openAllButton?.addEventListener("click", (()=> {
								this.openAll()

							})), this.openAllButtonMobile?.addEventListener("click", (()=> {
								this.openAll()

							}))), this.displayCloseAllButton&&(this.closeAllButton?.addEventListener("click", (()=> {
								this.closeAll()

							})), this.closeAllButtonMobile?.addEventListener("click", (()=> {
								this.closeAll()
							})))
			}

			updateHeaderButtonState() {
				this.accordion.items.some((t=>t.isOpen))?this.showCloseAllButton():this.showOpenAllButton()
			}

			openSearch() {
				this.searchEnabled&&(this.element.setAttribute("aria-expanded", "true"), this.searchOpenButton.setAttribute("aria-hidden", "true"), this.searchCloseButton.setAttribute("aria-hidden", "false"), this.inputField.focus())
			}

			closeSearch() {
				this.searchEnabled&&(this.element.removeAttribute("aria-expanded"), this.searchOpenButton.setAttribute("aria-hidden", "false"), this.searchCloseButton.setAttribute("aria-hidden", "true"), this.searchOpenButton.focus())
			}

			clearSearch() {
				this.searchEnabled&&(this.inputField.value="", this.inputField.dispatchEvent(new Event("input")), this.inputField.focus())
			}

			showClearInputButton() {
				this.searchEnabled&&(this.clearSearchButton.classList.remove("bl-hidden"), this.clearSearchButton.setAttribute("aria-hidden", "false"))
			}

			hideClearInputButton() {
				this.searchEnabled&&(this.clearSearchButton.classList.add("bl-hidden"), this.clearSearchButton.setAttribute("aria-hidden", "true"))
			}

			handleInput() {
				0===this.inputField.value.length?(this.hideClearInputButton(), this.submitSearchButton.setAttribute("aria-disabled", "true"), this.submitSearchButton.setAttribute("disabled", "")):(this.showClearInputButton(), this.submitSearchButton.setAttribute("aria-disabled", "false"), this.submitSearchButton.removeAttribute("disabled")), this.accordion.searchInItems(this.inputField.value)
			}

			closeAll() {
				this.accordion.closeAll(), this.updateHeaderButtonState()
			}

			openAll() {
				this.accordion.openAll(), this.updateHeaderButtonState()
			}

			showCloseAllButton() {
				this.openAllButton.classList.add("bl-hidden"), this.openAllButtonMobile.classList.add("bl-hidden"), this.displayCloseAllButton&&(this.closeAllButton.classList.remove("bl-hidden"), this.closeAllButtonMobile.classList.remove("bl-hidden"))
			}

			showOpenAllButton() {
				this.closeAllButton.classList.add("bl-hidden"), this.closeAllButtonMobile.classList.add("bl-hidden"), this.displayOpenAllButton&&(this.openAllButton.classList.remove("bl-hidden"), this.openAllButtonMobile.classList.remove("bl-hidden"))
			}

			hideAllButtons() {
				this.openAllButton.classList.add("bl-hidden"), this.closeAllButton.classList.add("bl-hidden"), this.openAllButtonMobile.classList.add("bl-hidden"), this.closeAllButtonMobile.classList.add("bl-hidden")
			}
		}

		class e {
			constructor(t, e) {
				this.element=t, this.accordion=e, void 0===this.isHeaderItem&&(this.isHeaderItem=this.element.hasAttribute("data-header"), this.isHeaderItem&& !this.accordion.options.header&&(this.accordion.options.header= !0)), this.isOpen="true"===this.element.getAttribute("aria-expanded"), this.headerDiv=this.element.firstElementChild, this.headingWrapper=this.headerDiv.querySelector("div"), this.contentDiv=this.element.lastElementChild, this.chevronDiv=this.element.querySelector(".chevron-container"), this.ciElements=this.isHeaderItem?Array.from(this.element.querySelectorAll("[data-ci-element]")):null, this.ongoingAnimation=null, this.setDirection(this.accordion.currentDirection), this.cachedText=null, this.isHidden= !1, this.headerDiv.addEventListener("click", (()=> {
							this.accordion.clickHandler(this)

						})), this.headerDiv.addEventListener("keydown", (t=> {
							"Enter" !==t.key&&" " !==t.key&&"Spacebar" !==t.key||(t.preventDefault(), this.accordion.clickHandler(this))
						})), this.#t()
			}

			#t() {
				const t=decodeURIComponent(window.location.hash); this.isHash= !( !this.element.id|| !t||`#${this.element.id}` !==t)
			}

			isAnimationRunning() {
				return null !==this.ongoingAnimation
			}

			expand(t= !0, e= !1) {
				e&&"pushState" in history&&history.pushState("", document.title, location.pathname+location.search), "horizontal"===this.direction?this.#e(t):this.#i(t)
			}

			#n() {
				this.isOpen= !0, this.element.setAttribute("aria-expanded", "true"), this.headerDiv.setAttribute("data-open", ""), this.headingWrapper?.setAttribute("data-open", ""), this.chevronDiv?.setAttribute("data-open", ""), this.headerDiv?.firstElementChild?.firstElementChild?.setAttribute("data-open", ""), this.ciElements?.forEach((t=> {
							t.setAttribute("data-open", "")
						}))
			}

			#e(t= !0) {
				var e, i; if(this.#n(), this.isHeaderItem)return; const n=[ {
					width:"0px"
				}

				, {
				width:(null !==(e=null !==(i=this.accordion.expandedItemWidth)&&void 0 !==i?i:this.contentDiv.scrollWidth)&&void 0 !==e?e:0)+"px"
			}

			], s= {
				duration:this.accordion.options.animationDuration, fill:"none", easing:"ease-in-out"
			}

			; this.#s(), this.ongoingAnimation=this.contentDiv.animate(n, s), this.ongoingAnimation.finished.then((()=> {
						this.contentDiv.style.width="auto", this.ongoingAnimation=null, "" !==this.element.id&&t&&(location.hash=this.element.id)

					})).catch((()=> {}))
		}

		#i(t= !0) {
			var e; if(this.#n(), this.isHeaderItem)return; const i=[ {
				height:"0px"
			}

			, {
			height:(null !==(e=this.contentDiv.scrollHeight)&&void 0 !==e?e:0)+"px"
		}

		], n= {
			duration:this.accordion.options.animationDuration, fill:"none", easing:"ease-in-out"
		}

		; this.#s(), this.ongoingAnimation=this.contentDiv.animate(i, n), this.ongoingAnimation.finished.then((()=> {
					this.contentDiv.style.height="auto", this.ongoingAnimation=null, "" !==this.element.id&&t&&(location.hash=this.element.id)

				})).catch((()=> {}))
	}

	collapse() {
		"horizontal"===this.direction?this.#o():this.#h()
	}

	#a() {
		this.isOpen= !1, this.element.removeAttribute("aria-expanded"), this.headerDiv.removeAttribute("data-open"), this.headingWrapper?.removeAttribute("data-open"), this.chevronDiv?.removeAttribute("data-open"), this.headerDiv?.firstElementChild?.firstElementChild?.removeAttribute("data-open"), this.ciElements?.forEach((t=> {
					t.removeAttribute("data-open")
				}))
	}

	#o() {
		var t; if(this.#a(), this.isHeaderItem)return; const e=[ {
			width:(null !==(t=this.contentDiv.scrollWidth)&&void 0 !==t?t:0)+"px"
		}

		, {
		width:"0px"
	}

	], i= {
		duration:this.accordion.options.animationDuration, fill:"none", easing:"ease-in-out"
	}

	; this.#s(), this.ongoingAnimation=this.contentDiv.animate(e, i), this.ongoingAnimation.finished.then((()=> {
				this.contentDiv.style.width="0px", this.ongoingAnimation=null

			})).catch((()=> {}))
}

#h() {
	var t; if(this.#a(), this.isHeaderItem)return; const e=[ {
		height:(null !==(t=this.contentDiv.scrollHeight)&&void 0 !==t?t:0)+"px"
	}

	, {
	height:"0px"
}

], i= {
	duration:this.accordion.options.animationDuration, fill:"none", easing:"ease-in-out"
}

; this.#s(), this.ongoingAnimation=this.contentDiv.animate(e, i), this.ongoingAnimation.finished.then((()=> {
			this.contentDiv.style.height="0px", this.ongoingAnimation=null

		})).catch((()=> {}))
}

toggle() {
	this.isOpen?this.collapse():this.expand()
}

setDirection(t) {
	this.direction !==t&&(this.direction=t, this.#s(), this.isHeaderItem||("horizontal"===t?(this.contentDiv.style.height="auto", this.contentDiv.style.width=this.isOpen?"auto":"0px"):(this.contentDiv.style.width="auto", this.contentDiv.style.height=this.isOpen?"auto":"0px")))
}

#s() {
	this.ongoingAnimation&&(this.ongoingAnimation.commitStyles(), this.ongoingAnimation.cancel(), this.ongoingAnimation=null)
}

searchContent(t) {
	const e=new RegExp("\\s", "g"); if(this.cachedText||(this.cachedText=this.element.textContent.toLocaleLowerCase().replaceAll(e, "")), 0===t.length)return !0; const i=t.toLocaleLowerCase().replaceAll(e, ""); return this.cachedText.includes(i)
}

hide() {
	this.element.setAttribute("hidden", ""), this.isHidden= !0
}

show() {
	this.element.removeAttribute("hidden"), this.isHidden= !1
}
}

class i {
	minimumHorizontalHeight=800; currentBreakpoint=""; constructor(i, n) {
		var s; this.element=i, this.options= {
			direction:"vertical", active: !1, animationDuration:400, collapsible: !0, multiple: !1, header: !1, numbered: !1
		}

		, this.options= {
			...this.options, ...this.#l(null !==(s=this.element.dataset.accordion)&&void 0 !==s?s:"")
		}

		, n&&(this.options.animationDuration=0), this.currentDirection="horizontal"===this.options.direction&&this.element.getBoundingClientRect().width>=1008&&window.matchMedia("(min-width: 1080px)").matches?"horizontal":"vertical"; const o=this.element.previousElementSibling; o&&"SEARCH"===o.tagName&&(this.search=new t(o, this), this.searchNotFoundText=o.querySelector(".search-not-found")), this.items=Array.from(this.element.querySelectorAll(":scope > div > section")).map((t=>new e(t, this))), "horizontal" !==this.options.direction||this.items[0].isHeaderItem||(this.items[0].isHeaderItem= !0), "horizontal"===this.options.direction?(this.lastResizeWidth=0, this.resizeObserver=new ResizeObserver((()=> {
						this.resizeHandlerHorizontal()

					})), this.resizeObserver.observe(document.body), this.resizeHandlerHorizontal(), this.debouncedUpdateExpandedItemWidth()):(this.resizeObserver=new ResizeObserver((()=> {
						this.resizeHandlerVertical()
					})), this.resizeObserver.observe(document.body), this.resizeHandlerVertical()), this.#r()
	}

	#r() {
		let t=null; if("number"==typeof this.options?.active&&this.items[this.options?.active]&&"horizontal" !==this.options.direction&&(t=this.items[this.options.active]), window.location.hash) {
			const e=this.items.find((t=>t.isHash)); e&&(t=e)
		}

		null !==t&&(t.expand( !1), this.closeItems(t), this.search.updateHeaderButtonState())
	}

	resizeHandlerVertical() {
		let t="sm"; window.matchMedia("(min-width: 768px)").matches&&(t="md"), window.matchMedia("(min-width: 1280px)").matches&&(t="xl"), this.currentBreakpoint !==t&&(this.currentBreakpoint=t, this.updateNumberWidths())
	}

	updateNumberWidths() {
		if( !this.options.numbered)return; const t=this.items.reduce(((t, e)=> {
					const i=e.headingWrapper.firstElementChild; i.style.paddingRight=""; const n=i.getBoundingClientRect().width; return Math.max(t, n)

				}), 0); this.items.forEach((e=> {
					var i; const n=e.headingWrapper.firstElementChild, s=e.contentDiv.querySelector(":scope > .spacer"), o=null !==(i=parseInt(getComputedStyle(n).paddingRight))&&void 0 !==i?i:50, h=`${t-n.getBoundingClientRect().width+o}px`; n.style.paddingRight=h, s&&(s.style.paddingRight=h)
				}))
	}

	resizeHandlerHorizontal() {
		if(0===Math.abs(window.innerWidth-this.lastResizeWidth))return; this.lastResizeWidth=window.innerWidth; const t=this.element.getBoundingClientRect().width>=1008&&window.matchMedia("(min-width: 1080px)").matches?"horizontal":"vertical"; if("horizontal"===t&&this.debouncedUpdateExpandedItemWidth(), t !==this.currentDirection) {
			this.currentDirection=t; for(const t of this.items)t.setDirection(this.currentDirection)
		}
	}

	clickHandler(t) {
		t.isOpen?this.clickHandlerCollapse(t):this.clickHandlerExpand(t)
	}

	clickHandlerExpand(t, e= !0) {
		if(this.options.multiple&&"horizontal" !==this.currentDirection||(this.debouncedUpdateExpandedItemWidth(), this.closeItems(t)), "horizontal"===this.options.direction&&"vertical"===this.currentDirection) {
			if(t.isHeaderItem)return; this.items[0].collapse()
		}

		t?.expand(e), this.search?.showCloseAllButton()
	}

	clickHandlerCollapse(t) {
		if( !(this.items.filter((t=> !t.isHidden)).length<2)||this.options.collapsible&&"horizontal" !==this.currentDirection) {
			if("horizontal"===this.options.direction) {
				if(t.isHeaderItem)return; return t.collapse(), this.items.find((t=>t.isOpen&& !t.isHeaderItem))||this.search.showOpenAllButton(), void this.items[0].expand()
			}

			 !this.options.collapsible&&this.items.filter((t=>t.isOpen)).length<2?t !==this.items[0]&&(t.collapse(), this.items[0].expand( !1,  !0)):t.isHeaderItem||(t.collapse(), this.items.find((t=>t.isOpen))||this.search.showOpenAllButton())
		}
	}

	closeItems(t=null) {
		( !(this.items.filter((t=> !t.isHidden)).length<2)||t||this.options.collapsible&&"horizontal" !==this.currentDirection)&&this.items.forEach((e=> {
					e !==t&&e.isOpen&&e.collapse()
				}))
	}

	debouncedUpdateExpandedItemWidth(t=50) {
		this.itemWidthTimeout&&clearTimeout(this.itemWidthTimeout), this.itemWidthTimeout=window.setTimeout((()=> {
					this.updateExpandedItemWidth()
				}), t)
	}

	updateExpandedItemWidth() {
		if(this.hasAnimatingItems())return void this.debouncedUpdateExpandedItemWidth(); let t=null; if(this.items.forEach((e=> {
						e.isOpen&&(t=e)

					})), t) {
			const e=window.getComputedStyle(t.headerDiv); this.expandedItemWidth=parseFloat(e.width), this.element.style.setProperty("--expanded-item-width", this.expandedItemWidth+"px")
		}
	}

	#l(t) {
		const e= {}

		; return t.split(";").map((t=>t.trim())).filter((t=>t)).forEach((t=> {
					const[i, n]=t.split(":").map((t=>t.trim())), s=i; switch(s) {
						case"direction":e[s]=n; break; case"active":e[s]="false" !==n&&parseInt(n)-1; break; case"animationDuration":e[s]=parseInt(n); break; case"collapsible":case"multiple":case"numbered":case"header":e[s]="true"===n
					}
				})), e
	}

	hasOpenItems() {
		return this.items.filter((t=>t.isOpen)).length>0
	}

	hasAnimatingItems() {
		return this.items.filter((t=>t.isAnimationRunning())).length>0
	}

	searchInItems(t, e=300) {
		this.searchTimeout&&clearTimeout(this.searchTimeout), this.searchTimeout=window.setTimeout((()=> {
					this.#d(t)
				}), e)
	}

	#d(t) {
		let e= !1, i=null; const n=[]; this.items.forEach((s=> {
					s.isHeaderItem?i=s:s.searchContent(t)?(s.show(), e= !0, n.push(s)):s.hide()
				})), n.length>0&& !n.some((t=>t.isOpen))&&this.clickHandlerExpand(n[0],  !1), e?(this.searchNotFoundText?.setAttribute("hidden", ""), this.debouncedUpdateExpandedItemWidth(), this.search.updateHeaderButtonState()):(this.searchNotFoundText?.removeAttribute("hidden"), this.clickHandlerExpand(i,  !1), this.search.hideAllButtons())
	}

	openAll() {
		"horizontal" !==this.currentDirection&&this.options.multiple&&(this.items.filter((t=> !t.isOpen)).forEach((t=> {
						t.expand( !1)
					})), "horizontal"===this.options.direction&&this.items[0].collapse())
	}

	closeAll() {
		"horizontal" !==this.currentDirection&&this.options.collapsible&&(this.items.filter((t=>t.isOpen)).forEach((t=> {
						t.collapse()
					})), "horizontal"===this.options.direction&&this.items[0].expand())
	}
}

class n {
	static#c=null; constructor() {
		var t; if(n.#c)throw new Error("AccordionManager is a singleton class and already has an instance. Use .getInstance() instead."); this.prefersReducedMotion=null !==(t=window.matchMedia("(prefers-reduced-motion: reduce)")?.matches)&&void 0 !==t&&t, this.defaultAnimationDuration=400, this.accordions=Array.from(document.querySelectorAll("[data-accordion]")).map((t=>new i(t, this.prefersReducedMotion))), n.#c=this
	}

	static getInstance() {
		return n.#c||new n, n.#c
	}
}

document.addEventListener("DOMContentLoaded", (()=> {
			n.getInstance()
		}))
})();