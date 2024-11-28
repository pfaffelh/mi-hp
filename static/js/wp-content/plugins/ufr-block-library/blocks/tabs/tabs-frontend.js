/* https://uni-freiburg.de/math/wp-content/plugins/ufr-block-library/blocks/tabs/tab-frontend.js?ver=8d7a451100ed3322d126 */
(()=> {
		"use strict"; const t=t=> {
			const e=parseInt(t.getAttribute("data-current-tab-index")); if( !isNaN(e))return e; const r=a(t, "allTabs"), i=Array.from(r).find((t=>`#${t.id}`==`${window.location.hash}`)), s=Array.from(r).indexOf(i); return s>-1?s:0
		}

		, e= {
			tabsList:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="tabs-list"]`), tabListItems:t=>t.querySelectorAll(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="tabs-list"]>li>a`), currentTabNavigator:a=> {
				const r=e.tabListItems(a), i=t(a); return Array.from(r).at(i)
			}

			, tablistCollapseButtonMobile:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="collapse-tablist-button-mobile"]`), tablistExpandButtonMobile:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="expand-tablist-button-mobile"]`), tablistCollapseButtonScreen:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="collapse-tablist-button-screen"]`), tablistExpandButtonScreen:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="expand-tablist-button-screen"]`), tabsContainer:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="tabs-container"]`), allTabs:t=>t.querySelectorAll(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="tab-content"]`), currentOpenTab:a=> {
				const r=t(a); if(void 0===r)return; const i=e.allTabs(a); return Array.from(i).at(r)
			}

			, searchWrapper:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="search-wrapper"]`), searchOpenButton:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="tabs-search-icon"]`), searchCloseButton:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="tabs-closesearch-icon"]`), searchForm:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="tabs-search-form"]`), searchInputField:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="search-input-field"]`), searchClearButton:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="tabs-search-clearinput"]`), searchSubmitButton:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="tabs-search-submit"]`), noSearchResultsText:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="no-search-results-text"]`), scrollLeftButton:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="scroll-left-button"]`), scrollRightButton:t=>t.querySelector(`[data-tab="${t.getAttribute(" data-tab")}"][data-tab-part="scroll-right-button"]`), desktopVerticalNavigationSpacer:t=>t.querySelectorAll('[data-tab-part="desktop-vertical-spacer"]')
		}

		, a=(t, a)=>e[a](t), r=t=> {
			const e=a(t, "tablistExpandButtonMobile"), r=a(t, "tablistCollapseButtonMobile"), i=a(t, "tablistExpandButtonScreen"), s=a(t, "tablistCollapseButtonScreen"), l=a(t, "tabsList"); l.scrollLeft=0, e.parentElement.classList.add("bl-hidden"), r.parentElement.classList.remove("bl-hidden"), i?.classList.add("bl-hidden"), s?.classList.remove("bl-hidden"), l.setAttribute("aria-expanded", "true")
		}

		, i=t=> {
			const e=a(t, "tablistExpandButtonMobile"), r=a(t, "tablistCollapseButtonMobile"), i=a(t, "tablistExpandButtonScreen"), s=a(t, "tablistCollapseButtonScreen"), l=a(t, "tabsList"); e.parentElement.classList.remove("bl-hidden"), r.parentElement.classList.add("bl-hidden"), i?.classList.remove("bl-hidden"), s?.classList.add("bl-hidden"), l.setAttribute("aria-expanded", "false")
		}

		, s= {
			updateHistory: !0, animate: !0, ignoreEqualTab: !1
		}

		, l=(t, e, r)=> {
			let i, l; r= {
				...s, ...r
			}

			; try {
				({
					newTabContainer:i, newTabIndicator:l
				}

				=n(t, e))
		}

		catch(t) {
			return !1
		}

		const o=a(t, "currentOpenTab"); if(i===o&& !r.ignoreEqualTab)return !1; const b=a(t, "currentTabNavigator"); if(b?.parentElement.removeAttribute("data-active"), b?.parentElement.classList.remove("bl-block"), b?.parentElement.classList.add("bl-hidden", "group-aria-expanded:bl-block"), l?.parentElement.setAttribute("data-active", "true"), l?.parentElement.classList.remove("bl-hidden", "group-aria-expanded:bl-block"), l?.parentElement.classList.add("bl-block"), t.setAttribute("data-current-tab-index", i?.getAttribute("data-tab-index")), t.getAttribute("data-tab-vertical")) {
			const e=Array.from(a(t, "tabListItems")); e.forEach((t=> {
						t.parentElement.classList.remove("@md/tab-block:xl:!bl-border-r-4", "@md/tab-block:xl:!bl-pe-[-2px]")
					})); for(let t=0; t<=e.findIndex((t=>t===l)); t++)e[t].parentElement.classList.add("@md/tab-block:xl:!bl-border-r-4", "@md/tab-block:xl:!bl-pe-[-2px]")
		}

		return r.animate?d(o, i):(o?.classList.add("bl-hidden"), o?.setAttribute("aria-expanded", "false"), i?.classList.remove("bl-hidden"), i?.setAttribute("aria-expanded", "true")), r.updateHistory&&history.replaceState({}

		, null, l?.href),  !0
}

, n=(t, e)=> {
	if(void 0===e)return {
		newTabContainer:void 0, newTabIndicator:void 0
	}

	; const r=a(t, "allTabs"), i=a(t, "tabListItems"); let s, l; switch(typeof e) {
		case"number":s=Array.from(r).at(e), l=Array.from(i).at(e); break; case"string":e=e.replace(/^#/, ""), e=decodeURIComponent(e), s=Array.from(r).find((t=>t.getAttribute("id")===e)), l=Array.from(i).find((t=>t.getAttribute("href")===`#${e}`)); break; default:throw new TypeError(`Function parameter 'tab' must be of type number or string, but is ${typeof e}.`)
	}

	if( !l|| !s)throw new RangeError(`Tried to find tab by index or id of '${e}', but no tab was found.`); return {
		newTabContainer:s, newTabIndicator:l
	}
}

, o=t=> {
	t.style.display="block", t.setAttribute("aria-expanded", "true"), t.animate([ {
			opacity:0
		}

		, {
		opacity:1
	}

	], {
	duration:200, fill:"forwards"
})
}

, d=(t, e)=> {
	void 0 !==t?t.animate([ {
			opacity:1
		}

		, {
		opacity:0
	}

	], {
	duration:200, fill:"forwards"

}).onfinish=()=> {
	t.style.display="none", t.setAttribute("aria-expanded", "false"), e&&o(e)
}

:void 0 !==e&&o(e)
}

, b=t=> {
	const e=a(t, "tabsList"), r=a(t, "scrollLeftButton").parentElement; e.style.setProperty("--indicatorMargin", "0px"), r.classList.add("@md/tab-block:bl-hidden"), r.classList.remove("@md/tab-block:bl-flex")
}

, c=t=> {
	const e=a(t, "tabsList"), r=a(t, "scrollLeftButton").parentElement, i=a(t, "tablistExpandButtonScreen"); e.scrollWidth-r.clientWidth-2>t.clientWidth&&"true" !==e.getAttribute("aria-expanded")?((t=> {
				const e=a(t, "tabsList"), r=a(t, "scrollLeftButton").parentElement; r.classList.add("@md/tab-block:bl-flex"), r.classList.remove("@md/tab-block:bl-hidden"), e.style.setProperty("--indicatorMargin", `${r.clientWidth}px`)

			})(t), i?.removeAttribute("data-hidebutton")):(b(t), i?.setAttribute("data-hidebutton", "true")), requestAnimationFrame((()=> {
				e.style.setProperty("--tabNavFullWidth", e.clientWidth-r.clientWidth-1+"px"), requestAnimationFrame((()=>e.style.setProperty("--tabNavFullWidth", `${e.scrollWidth}px`)))
			}))
}

, u=t=> {
	const e=a(t, "tabsList"), r=a(t, "scrollLeftButton"), i=a(t, "scrollRightButton"); e.scrollLeft<1?r.setAttribute("disabled", "true"):r.removeAttribute("disabled"), e.scrollLeft>=e.scrollWidth-e.clientWidth?i.setAttribute("disabled", "true"):i.removeAttribute("disabled")
}

; document.addEventListener("DOMContentLoaded", (function(e) {
			const s=document.querySelectorAll('[data-role="tabs-wrapper"]'); s.forEach((e=> {
						const s=a(e, "tablistCollapseButtonMobile"), n=a(e, "tablistExpandButtonMobile"), o=a(e, "tablistCollapseButtonScreen"), d=a(e, "tablistExpandButtonScreen"), p=a(e, "tabsList"), h=a(e, "tabListItems"), m=a(e, "scrollLeftButton"), f=a(e, "scrollRightButton"); ((e, r)=> {
								if( !r)return; const i=a(e, "searchOpenButton"), s=a(e, "searchCloseButton"), n=a(e, "searchInputField"), o=a(e, "searchClearButton"), d=a(e, "searchSubmitButton"), b=a(e, "searchForm"), u=a(e, "allTabs"), p=a(e, "tabsList"), h=a(e, "tabListItems"), m=a(e, "noSearchResultsText"), f=a(e, "desktopVerticalNavigationSpacer"); i.addEventListener("click", (()=> {
											r.setAttribute("aria-expanded", "true"), n.removeAttribute("tabindex"), o.removeAttribute("tabindex"), d.removeAttribute("tabindex"), n.focus()

										})), s.addEventListener("click", (()=> {
											r.setAttribute("aria-expanded", "false"), n.setAttribute("tabindex", "-1"), o.setAttribute("tabindex", "-1"), d.setAttribute("tabindex", "-1")

										})), o.addEventListener("click", (t=> {
											t.preventDefault(), n.value="", n.dispatchEvent(new Event("input")), n.focus()

										})), n.value.length>0&&(o.classList.remove("bl-hidden"), d.removeAttribute("disabled")), n.addEventListener("input", (()=> {
											var t; 0===n.value.length?((t=o).classList.contains("bl-hidden")||(t.animate([ {
															opacity:getComputedStyle(t).opacity
														}

														, {
														opacity:0
													}

													], {
													duration:200, fill:"forwards"

												}).onfinish=()=> {
												t.classList.add("bl-hidden"), t.animate([ {
														opacity:0
													}

													, {
													opacity:1
												}

												], {
												duration:0, fill:"forwards"
											})

									}), d.setAttribute("disabled", "true")):((t=> {
										t.classList.contains("bl-hidden")&&(t.animate([ {
													opacity:getComputedStyle(t).opacity
												}

												, {
												opacity:0
											}

											], {
											duration:0, fill:"forwards"

										}).onfinish=()=> {
										t.classList.remove("bl-hidden"), t.animate([ {
												opacity:0
											}

											, {
											opacity:1
										}

										], {
										duration:200, fill:"forwards"
									})
							})
					})(o), d.removeAttribute("disabled")), L()

		})), b.addEventListener("submit", (t=> {
			L()

		})); const L=()=> {
	if(0===n.value.length)return A(); v()
}

, v=((t, e=300)=> {
		let a; return(...r)=> {
			clearTimeout(a), a=setTimeout((()=> {
						t.apply(void 0, r)
					}), e)
		}

	})((()=> {
			const a=n.value.toLocaleLowerCase(); let r= !1; const i=[]; if(Array.from(u).forEach(((t, s)=> {
							const l=parseInt(t.getAttribute("data-tab-index")), n=Array.from(h).at(l), o=t.textContent.toLocaleLowerCase().replaceAll("\t", "").replaceAll("\n", ""), d=n.textContent.toLocaleLowerCase(), b=-1 !==o.indexOf(a)||-1 !==d.indexOf(a); t.setAttribute("data-search-result", `${b}`), n.parentElement.setAttribute("data-search-result", `${b}`), b&& !r&&n.parentElement.setAttribute("data-first-visible-tab", "true"), b&&(r= !0), b&&i.push(l), c(e)

						})),  !r)return m.classList.remove("bl-hidden"), m.classList.add("bl-inline-block"), p.classList.add("bl-hidden"), f.forEach((t=> {
						t.classList.remove("@md/tab-block:xl:bl-block")

					})), void l(e, void 0); m.classList.remove("bl-inline-block"), m.classList.add("bl-hidden"), p.classList.remove("bl-hidden"), f.forEach((t=> {
						t.classList.add("@md/tab-block:xl:bl-block")
					})), void 0===i.find((a=>a===t(e)))&&l(e, i[0])

		})), A=()=> {
	Array.from(u).forEach((t=> {
				t.setAttribute("data-search-result", "true")

			})), Array.from(h).forEach(((t, e)=> {
				t.parentElement.setAttribute("data-search-result", "true"), 0 !==e&&t.parentElement.setAttribute("data-first-visible-tab", "false")

			})), m.classList.add("bl-hidden"), p.classList.remove("bl-hidden"), f.forEach((t=> {
				t.classList.add("@md/tab-block:xl:bl-block")
			})), c(e), void 0===t(e)&&l(e, void 0)
}

})(e, a(e, "searchWrapper")), l(e, window.location.hash, {
	updateHistory: !1, ignoreEqualTab: !0, animate: !1

})||l(e, 0, {
	updateHistory: !1, ignoreEqualTab: !0, animate: !1

}), h.forEach((t=> {
			t.addEventListener("click", (t=>((t, e)=> {
							t.preventDefault(); const a=t.target; l(e, a.getAttribute("href"))
						})(t, e)))

		})), n.addEventListener("click", (()=> {
			r(e), c(e)

		})), d?.addEventListener("click", (()=> {
			r(e), b(e)

		})), s.addEventListener("click", (()=> {
			i(e), b(e)

		})), o?.addEventListener("click", (()=> {
			i(e), c(e)

		})), m.addEventListener("click", (()=> {
			p.scrollBy({
				left:-p.clientWidth/2, behavior:"smooth"
			})

	})), f.addEventListener("click", (()=> {
			p.scrollBy({
				left:p.clientWidth/2, behavior:"smooth"
			})

	})), p.addEventListener("scroll", (()=> {
			u(e)

		})), c(e), u(e), window.addEventListener("resize", ((t, e=50)=> {
			let a= !1; return(...r)=> {
				a||(t(...r), a= !0, setTimeout((()=> {
								a= !1
							}), e))
			}

		})((()=>c(e)))), new IntersectionObserver((()=> {
			c(e)

		}), {
	root:document.body, threshold:1e-5, rootMargin:"0px"
}).observe(e)

})), window.addEventListener("hashchange", (t=> {
			s.forEach((t=> {
						l(t, window.location.hash, {
							updateHistory: !1, ignoreEqualTab: !0, animate: !1

						})&&t.scrollIntoView({
						behavior:"instant", block:"start"
					})
			}))
}))
}))
})();