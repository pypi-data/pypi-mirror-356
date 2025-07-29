var _JUPYTERLAB;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "webpack/container/entry/runcell":
/*!***********************!*\
  !*** container entry ***!
  \***********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

var moduleMap = {
	"./index": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_codemirror_autocomplete_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_commands_dist_index_js-node_modules_codemirror_lint_dist_inde-c2dd10"), __webpack_require__.e("vendors-node_modules_codemirror_dist_index_js-node_modules_css-loader_dist_runtime_getUrl_js--0aabd4"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_codemirro-44efd7"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("webpack_sharing_consume_default_lezer_common"), __webpack_require__.e("node_modules_css-loader_dist_cjs_js_style_base_css"), __webpack_require__.e("webpack_sharing_consume_default_clsx_clsx"), __webpack_require__.e("lib_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./extension": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_codemirror_autocomplete_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_commands_dist_index_js-node_modules_codemirror_lint_dist_inde-c2dd10"), __webpack_require__.e("vendors-node_modules_codemirror_dist_index_js-node_modules_css-loader_dist_runtime_getUrl_js--0aabd4"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_codemirro-44efd7"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("webpack_sharing_consume_default_lezer_common"), __webpack_require__.e("node_modules_css-loader_dist_cjs_js_style_base_css"), __webpack_require__.e("webpack_sharing_consume_default_clsx_clsx"), __webpack_require__.e("lib_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./style": () => {
		return Promise.all([__webpack_require__.e("node_modules_css-loader_dist_cjs_js_style_base_css"), __webpack_require__.e("node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_getUrl_js-no-70179a")]).then(() => (() => ((__webpack_require__(/*! ./style/index.js */ "./style/index.js")))));
	}
};
var get = (module, getScope) => {
	__webpack_require__.R = getScope;
	getScope = (
		__webpack_require__.o(moduleMap, module)
			? moduleMap[module]()
			: Promise.resolve().then(() => {
				throw new Error('Module "' + module + '" does not exist in container.');
			})
	);
	__webpack_require__.R = undefined;
	return getScope;
};
var init = (shareScope, initScope) => {
	if (!__webpack_require__.S) return;
	var name = "default"
	var oldScope = __webpack_require__.S[name];
	if(oldScope && oldScope !== shareScope) throw new Error("Container initialization failed as it has already been initialized with a different share scope");
	__webpack_require__.S[name] = shareScope;
	return __webpack_require__.I(name, initScope);
};

// This exports getters to disallow modifications
__webpack_require__.d(exports, {
	get: () => (get),
	init: () => (init)
});

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = __webpack_module_cache__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	(() => {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = (chunkId) => {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce((promises, key) => {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + "." + {"vendors-node_modules_codemirror_autocomplete_dist_index_js":"73e278eaa5c1135f8746","vendors-node_modules_codemirror_commands_dist_index_js-node_modules_codemirror_lint_dist_inde-c2dd10":"894e428f31211542dc20","vendors-node_modules_codemirror_dist_index_js-node_modules_css-loader_dist_runtime_getUrl_js--0aabd4":"e07f32c3ea3aa27f0a56","node_modules_css-loader_dist_cjs_js_style_base_css":"1b57f9d07b3efb0ab94c","lib_index_js":"2f0e494cf8fe3988d09f","node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_getUrl_js-no-70179a":"dda4252e189739f43896","vendors-node_modules_lezer_lr_dist_index_js":"764bf288e8bc845b937a","vendors-node_modules_codemirror_lang-javascript_dist_index_js":"03bf41ebcb294c3a2e53","vendors-node_modules_codemirror_lang-markdown_dist_index_js":"35cdfefcd5fce65249c6","vendors-node_modules_codemirror_lang-python_dist_index_js":"9da54cabda7c1f601c7b","vendors-node_modules_codemirror_merge_dist_index_js":"f5059a722c3a884b02bc","vendors-node_modules_react_jsx-runtime_js":"3ebe566017b59fbeb188","vendors-node_modules_radix-ui_react-avatar_dist_index_mjs":"72cdd72f887cfafdd91a","vendors-node_modules_radix-ui_primitive_dist_index_mjs-node_modules_radix-ui_react-context_di-836b8c":"ef0148543619ca5eb7d5","vendors-node_modules_radix-ui_react-scroll-area_dist_index_mjs":"b54bb0505a5105e804c9","node_modules_radix-ui_react-slot_dist_index_mjs-_dfa40":"8bc75b03b32ac5a72dfb","vendors-node_modules_radix-ui_react-tooltip_dist_index_mjs":"b9f7bf2f09abadafc2b6","vendors-node_modules_uiw_react-codemirror_esm_index_js":"00479affedaee92fc40f","node_modules_class-variance-authority_dist_index_mjs-_b7ca0":"177c471d759cbf56cdcb","node_modules_clsx_dist_clsx_mjs":"7da1cca542ecaf685e8b","vendors-node_modules_embla-carousel-react_esm_embla-carousel-react_esm_js":"3a082b457a63f5c2ba19","vendors-node_modules_lucide-react_dist_esm_lucide-react_js":"13265d1cfed5ded2eb8b","vendors-node_modules_mobx-react-lite_es_index_js":"f112304171c62ae117f2","vendors-node_modules_mobx_dist_mobx_esm_js":"a7af4637adf9aa41ceab","node_modules_nanoid_index_browser_js":"8bc9755247a9b1ba2534","node_modules_next-themes_dist_index_mjs-_548d0":"ed82ca413500f2bfe72a","vendors-node_modules_react-markdown_index_js":"e185e30f06d5d2fe0ea2","vendors-node_modules_sonner_dist_index_mjs":"8143cf634dd421c26deb","vendors-node_modules_tailwind-merge_dist_bundle-mjs_mjs":"8d7388192deefd4767ab","node_modules_radix-ui_react-slot_dist_index_mjs-_dfa41":"664b117765986201fc37","node_modules_class-variance-authority_dist_index_mjs-_b7ca1":"0d5230f6fb9f63e18c0e","node_modules_next-themes_dist_index_mjs-_548d1":"da1577c7a4b0dc61aa31","node_modules_radix-ui_react-slot_dist_index_mjs-_dfa42":"900bc1bcfa8abfb0187e"}[chunkId] + ".js";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/load script */
/******/ 	(() => {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "runcell:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = (url, done, key, chunkId) => {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 		
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = (prev, event) => {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach((fn) => (fn(event)));
/******/ 				if(prev) return prev(event);
/******/ 			}
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/sharing */
/******/ 	(() => {
/******/ 		__webpack_require__.S = {};
/******/ 		var initPromises = {};
/******/ 		var initTokens = {};
/******/ 		__webpack_require__.I = (name, initScope) => {
/******/ 			if(!initScope) initScope = [];
/******/ 			// handling circular init calls
/******/ 			var initToken = initTokens[name];
/******/ 			if(!initToken) initToken = initTokens[name] = {};
/******/ 			if(initScope.indexOf(initToken) >= 0) return;
/******/ 			initScope.push(initToken);
/******/ 			// only runs once
/******/ 			if(initPromises[name]) return initPromises[name];
/******/ 			// creates a new share scope if needed
/******/ 			if(!__webpack_require__.o(__webpack_require__.S, name)) __webpack_require__.S[name] = {};
/******/ 			// runs all init snippets from all modules reachable
/******/ 			var scope = __webpack_require__.S[name];
/******/ 			var warn = (msg) => {
/******/ 				if (typeof console !== "undefined" && console.warn) console.warn(msg);
/******/ 			};
/******/ 			var uniqueName = "runcell";
/******/ 			var register = (name, version, factory, eager) => {
/******/ 				var versions = scope[name] = scope[name] || {};
/******/ 				var activeVersion = versions[version];
/******/ 				if(!activeVersion || (!activeVersion.loaded && (!eager != !activeVersion.eager ? eager : uniqueName > activeVersion.from))) versions[version] = { get: factory, from: uniqueName, eager: !!eager };
/******/ 			};
/******/ 			var initExternal = (id) => {
/******/ 				var handleError = (err) => (warn("Initialization of sharing external failed: " + err));
/******/ 				try {
/******/ 					var module = __webpack_require__(id);
/******/ 					if(!module) return;
/******/ 					var initFn = (module) => (module && module.init && module.init(__webpack_require__.S[name], initScope))
/******/ 					if(module.then) return promises.push(module.then(initFn, handleError));
/******/ 					var initResult = initFn(module);
/******/ 					if(initResult && initResult.then) return promises.push(initResult['catch'](handleError));
/******/ 				} catch(err) { handleError(err); }
/******/ 			}
/******/ 			var promises = [];
/******/ 			switch(name) {
/******/ 				case "default": {
/******/ 					register("@codemirror/lang-javascript", "6.2.4", () => (Promise.all([__webpack_require__.e("vendors-node_modules_lezer_lr_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_autocomplete_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_lang-javascript_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_codemirro-44efd7"), __webpack_require__.e("webpack_sharing_consume_default_lezer_common")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/@codemirror/lang-javascript/dist/index.js */ "../../node_modules/@codemirror/lang-javascript/dist/index.js"))))));
/******/ 					register("@codemirror/lang-markdown", "6.3.3", () => (Promise.all([__webpack_require__.e("vendors-node_modules_lezer_lr_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_autocomplete_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_lang-markdown_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_codemirro-44efd7"), __webpack_require__.e("webpack_sharing_consume_default_lezer_common"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_lang-javascript_codemirror_lang-javascript")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/@codemirror/lang-markdown/dist/index.js */ "../../node_modules/@codemirror/lang-markdown/dist/index.js"))))));
/******/ 					register("@codemirror/lang-python", "6.2.1", () => (Promise.all([__webpack_require__.e("vendors-node_modules_lezer_lr_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_autocomplete_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_lang-python_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_codemirro-44efd7"), __webpack_require__.e("webpack_sharing_consume_default_lezer_common")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/@codemirror/lang-python/dist/index.js */ "../../node_modules/@codemirror/lang-python/dist/index.js"))))));
/******/ 					register("@codemirror/merge", "6.10.2", () => (Promise.all([__webpack_require__.e("vendors-node_modules_codemirror_merge_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_codemirro-44efd7")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/@codemirror/merge/dist/index.js */ "../../node_modules/@codemirror/merge/dist/index.js"))))));
/******/ 					register("@radix-ui/react-avatar", "1.1.10", () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("vendors-node_modules_radix-ui_react-avatar_dist_index_mjs"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("webpack_sharing_consume_default_radix-ui_react-slot_radix-ui_react-slot")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/@radix-ui/react-avatar/dist/index.mjs */ "../../node_modules/@radix-ui/react-avatar/dist/index.mjs"))))));
/******/ 					register("@radix-ui/react-scroll-area", "1.2.9", () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("vendors-node_modules_radix-ui_primitive_dist_index_mjs-node_modules_radix-ui_react-context_di-836b8c"), __webpack_require__.e("vendors-node_modules_radix-ui_react-scroll-area_dist_index_mjs"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("webpack_sharing_consume_default_radix-ui_react-slot_radix-ui_react-slot")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/@radix-ui/react-scroll-area/dist/index.mjs */ "../../node_modules/@radix-ui/react-scroll-area/dist/index.mjs"))))));
/******/ 					register("@radix-ui/react-slot", "1.2.3", () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("node_modules_radix-ui_react-slot_dist_index_mjs-_dfa40")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/@radix-ui/react-slot/dist/index.mjs */ "../../node_modules/@radix-ui/react-slot/dist/index.mjs"))))));
/******/ 					register("@radix-ui/react-tooltip", "1.2.7", () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("vendors-node_modules_radix-ui_primitive_dist_index_mjs-node_modules_radix-ui_react-context_di-836b8c"), __webpack_require__.e("vendors-node_modules_radix-ui_react-tooltip_dist_index_mjs"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("webpack_sharing_consume_default_radix-ui_react-slot_radix-ui_react-slot")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/@radix-ui/react-tooltip/dist/index.mjs */ "../../node_modules/@radix-ui/react-tooltip/dist/index.mjs"))))));
/******/ 					register("@uiw/react-codemirror", "0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("vendors-node_modules_codemirror_autocomplete_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_commands_dist_index_js-node_modules_codemirror_lint_dist_inde-c2dd10"), __webpack_require__.e("vendors-node_modules_uiw_react-codemirror_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_codemirro-44efd7"), __webpack_require__.e("webpack_sharing_consume_default_lezer_common")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/@uiw/react-codemirror/esm/index.js */ "../../node_modules/@uiw/react-codemirror/esm/index.js"))))));
/******/ 					register("class-variance-authority", "0.7.1", () => (Promise.all([__webpack_require__.e("webpack_sharing_consume_default_clsx_clsx"), __webpack_require__.e("node_modules_class-variance-authority_dist_index_mjs-_b7ca0")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/class-variance-authority/dist/index.mjs */ "../../node_modules/class-variance-authority/dist/index.mjs"))))));
/******/ 					register("clsx", "2.1.1", () => (__webpack_require__.e("node_modules_clsx_dist_clsx_mjs").then(() => (() => (__webpack_require__(/*! ../../node_modules/clsx/dist/clsx.mjs */ "../../node_modules/clsx/dist/clsx.mjs"))))));
/******/ 					register("embla-carousel-react", "8.6.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_embla-carousel-react_esm_embla-carousel-react_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_react")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/embla-carousel-react/esm/embla-carousel-react.esm.js */ "../../node_modules/embla-carousel-react/esm/embla-carousel-react.esm.js"))))));
/******/ 					register("lucide-react", "0.507.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_lucide-react_dist_esm_lucide-react_js"), __webpack_require__.e("webpack_sharing_consume_default_react")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/lucide-react/dist/esm/lucide-react.js */ "../../node_modules/lucide-react/dist/esm/lucide-react.js"))))));
/******/ 					register("mobx-react-lite", "4.1.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_mobx-react-lite_es_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("webpack_sharing_consume_default_mobx_mobx")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/mobx-react-lite/es/index.js */ "../../node_modules/mobx-react-lite/es/index.js"))))));
/******/ 					register("mobx", "6.13.7", () => (__webpack_require__.e("vendors-node_modules_mobx_dist_mobx_esm_js").then(() => (() => (__webpack_require__(/*! ../../node_modules/mobx/dist/mobx.esm.js */ "../../node_modules/mobx/dist/mobx.esm.js"))))));
/******/ 					register("nanoid", "5.1.5", () => (__webpack_require__.e("node_modules_nanoid_index_browser_js").then(() => (() => (__webpack_require__(/*! ./node_modules/nanoid/index.browser.js */ "./node_modules/nanoid/index.browser.js"))))));
/******/ 					register("next-themes", "0.4.6", () => (Promise.all([__webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("node_modules_next-themes_dist_index_mjs-_548d0")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/next-themes/dist/index.mjs */ "../../node_modules/next-themes/dist/index.mjs"))))));
/******/ 					register("react-markdown", "10.1.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("vendors-node_modules_react-markdown_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/react-markdown/index.js */ "../../node_modules/react-markdown/index.js"))))));
/******/ 					register("runcell", "0.1.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_codemirror_autocomplete_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_commands_dist_index_js-node_modules_codemirror_lint_dist_inde-c2dd10"), __webpack_require__.e("vendors-node_modules_codemirror_dist_index_js-node_modules_css-loader_dist_runtime_getUrl_js--0aabd4"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_codemirro-44efd7"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("webpack_sharing_consume_default_lezer_common"), __webpack_require__.e("node_modules_css-loader_dist_cjs_js_style_base_css"), __webpack_require__.e("webpack_sharing_consume_default_clsx_clsx"), __webpack_require__.e("lib_index_js")]).then(() => (() => (__webpack_require__(/*! ./lib/index.js */ "./lib/index.js"))))));
/******/ 					register("sonner", "2.0.5", () => (Promise.all([__webpack_require__.e("vendors-node_modules_sonner_dist_index_mjs"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom")]).then(() => (() => (__webpack_require__(/*! ../../node_modules/sonner/dist/index.mjs */ "../../node_modules/sonner/dist/index.mjs"))))));
/******/ 					register("tailwind-merge", "3.3.1", () => (__webpack_require__.e("vendors-node_modules_tailwind-merge_dist_bundle-mjs_mjs").then(() => (() => (__webpack_require__(/*! ../../node_modules/tailwind-merge/dist/bundle-mjs.mjs */ "../../node_modules/tailwind-merge/dist/bundle-mjs.mjs"))))));
/******/ 				}
/******/ 				break;
/******/ 			}
/******/ 			if(!promises.length) return initPromises[name] = 1;
/******/ 			return initPromises[name] = Promise.all(promises).then(() => (initPromises[name] = 1));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		var scriptUrl;
/******/ 		if (__webpack_require__.g.importScripts) scriptUrl = __webpack_require__.g.location + "";
/******/ 		var document = __webpack_require__.g.document;
/******/ 		if (!scriptUrl && document) {
/******/ 			if (document.currentScript && document.currentScript.tagName.toUpperCase() === 'SCRIPT')
/******/ 				scriptUrl = document.currentScript.src;
/******/ 			if (!scriptUrl) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				if(scripts.length) {
/******/ 					var i = scripts.length - 1;
/******/ 					while (i > -1 && (!scriptUrl || !/^http(s?):/.test(scriptUrl))) scriptUrl = scripts[i--].src;
/******/ 				}
/******/ 			}
/******/ 		}
/******/ 		// When supporting browsers where an automatic publicPath is not supported you must specify an output.publicPath manually via configuration
/******/ 		// or pass an empty string ("") and set the __webpack_public_path__ variable from your code to use your own logic.
/******/ 		if (!scriptUrl) throw new Error("Automatic publicPath is not supported in this browser");
/******/ 		scriptUrl = scriptUrl.replace(/^blob:/, "").replace(/#.*$/, "").replace(/\?.*$/, "").replace(/\/[^\/]+$/, "/");
/******/ 		__webpack_require__.p = scriptUrl;
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/consumes */
/******/ 	(() => {
/******/ 		var parseVersion = (str) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var p=p=>{return p.split(".").map((p=>{return+p==p?+p:p}))},n=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(str),r=n[1]?p(n[1]):[];return n[2]&&(r.length++,r.push.apply(r,p(n[2]))),n[3]&&(r.push([]),r.push.apply(r,p(n[3]))),r;
/******/ 		}
/******/ 		var versionLt = (a, b) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			a=parseVersion(a),b=parseVersion(b);for(var r=0;;){if(r>=a.length)return r<b.length&&"u"!=(typeof b[r])[0];var e=a[r],n=(typeof e)[0];if(r>=b.length)return"u"==n;var t=b[r],f=(typeof t)[0];if(n!=f)return"o"==n&&"n"==f||("s"==f||"u"==n);if("o"!=n&&"u"!=n&&e!=t)return e<t;r++}
/******/ 		}
/******/ 		var rangeToString = (range) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var r=range[0],n="";if(1===range.length)return"*";if(r+.5){n+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var e=1,a=1;a<range.length;a++){e--,n+="u"==(typeof(t=range[a]))[0]?"-":(e>0?".":"")+(e=2,t)}return n}var g=[];for(a=1;a<range.length;a++){var t=range[a];g.push(0===t?"not("+o()+")":1===t?"("+o()+" || "+o()+")":2===t?g.pop()+" "+g.pop():rangeToString(t))}return o();function o(){return g.pop().replace(/^\((.+)\)$/,"$1")}
/******/ 		}
/******/ 		var satisfy = (range, version) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			if(0 in range){version=parseVersion(version);var e=range[0],r=e<0;r&&(e=-e-1);for(var n=0,i=1,a=!0;;i++,n++){var f,s,g=i<range.length?(typeof range[i])[0]:"";if(n>=version.length||"o"==(s=(typeof(f=version[n]))[0]))return!a||("u"==g?i>e&&!r:""==g!=r);if("u"==s){if(!a||"u"!=g)return!1}else if(a)if(g==s)if(i<=e){if(f!=range[i])return!1}else{if(r?f>range[i]:f<range[i])return!1;f!=range[i]&&(a=!1)}else if("s"!=g&&"n"!=g){if(r||i<=e)return!1;a=!1,i--}else{if(i<=e||s<g!=r)return!1;a=!1}else"s"!=g&&"n"!=g&&(a=!1,i--)}}var t=[],o=t.pop.bind(t);for(n=1;n<range.length;n++){var u=range[n];t.push(1==u?o()|o():2==u?o()&o():u?satisfy(u,version):!o())}return!!o();
/******/ 		}
/******/ 		var exists = (scope, key) => {
/******/ 			return scope && __webpack_require__.o(scope, key);
/******/ 		}
/******/ 		var get = (entry) => {
/******/ 			entry.loaded = 1;
/******/ 			return entry.get()
/******/ 		};
/******/ 		var eagerOnly = (versions) => {
/******/ 			return Object.keys(versions).reduce((filtered, version) => {
/******/ 					if (versions[version].eager) {
/******/ 						filtered[version] = versions[version];
/******/ 					}
/******/ 					return filtered;
/******/ 			}, {});
/******/ 		};
/******/ 		var findLatestVersion = (scope, key, eager) => {
/******/ 			var versions = eager ? eagerOnly(scope[key]) : scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key];
/******/ 		};
/******/ 		var findSatisfyingVersion = (scope, key, requiredVersion, eager) => {
/******/ 			var versions = eager ? eagerOnly(scope[key]) : scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				if (!satisfy(requiredVersion, b)) return a;
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var findSingletonVersionKey = (scope, key, eager) => {
/******/ 			var versions = eager ? eagerOnly(scope[key]) : scope[key];
/******/ 			return Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || (!versions[a].loaded && versionLt(a, b)) ? b : a;
/******/ 			}, 0);
/******/ 		};
/******/ 		var getInvalidSingletonVersionMessage = (scope, key, version, requiredVersion) => {
/******/ 			return "Unsatisfied version " + version + " from " + (version && scope[key][version].from) + " of shared singleton module " + key + " (required " + rangeToString(requiredVersion) + ")"
/******/ 		};
/******/ 		var getInvalidVersionMessage = (scope, scopeName, key, requiredVersion, eager) => {
/******/ 			var versions = scope[key];
/******/ 			return "No satisfying version (" + rangeToString(requiredVersion) + ")" + (eager ? " for eager consumption" : "") + " of shared module " + key + " found in shared scope " + scopeName + ".\n" +
/******/ 				"Available versions: " + Object.keys(versions).map((key) => {
/******/ 				return key + " from " + versions[key].from;
/******/ 			}).join(", ");
/******/ 		};
/******/ 		var fail = (msg) => {
/******/ 			throw new Error(msg);
/******/ 		}
/******/ 		var failAsNotExist = (scopeName, key) => {
/******/ 			return fail("Shared module " + key + " doesn't exist in shared scope " + scopeName);
/******/ 		}
/******/ 		var warn = /*#__PURE__*/ (msg) => {
/******/ 			if (typeof console !== "undefined" && console.warn) console.warn(msg);
/******/ 		};
/******/ 		var init = (fn) => (function(scopeName, key, eager, c, d) {
/******/ 			var promise = __webpack_require__.I(scopeName);
/******/ 			if (promise && promise.then && !eager) {
/******/ 				return promise.then(fn.bind(fn, scopeName, __webpack_require__.S[scopeName], key, false, c, d));
/******/ 			}
/******/ 			return fn(scopeName, __webpack_require__.S[scopeName], key, eager, c, d);
/******/ 		});
/******/ 		
/******/ 		var useFallback = (scopeName, key, fallback) => {
/******/ 			return fallback ? fallback() : failAsNotExist(scopeName, key);
/******/ 		}
/******/ 		var load = /*#__PURE__*/ init((scopeName, scope, key, eager, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			return get(findLatestVersion(scope, key, eager));
/******/ 		});
/******/ 		var loadVersion = /*#__PURE__*/ init((scopeName, scope, key, eager, requiredVersion, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			var satisfyingVersion = findSatisfyingVersion(scope, key, requiredVersion, eager);
/******/ 			if (satisfyingVersion) return get(satisfyingVersion);
/******/ 			warn(getInvalidVersionMessage(scope, scopeName, key, requiredVersion, eager))
/******/ 			return get(findLatestVersion(scope, key, eager));
/******/ 		});
/******/ 		var loadStrictVersion = /*#__PURE__*/ init((scopeName, scope, key, eager, requiredVersion, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			var satisfyingVersion = findSatisfyingVersion(scope, key, requiredVersion, eager);
/******/ 			if (satisfyingVersion) return get(satisfyingVersion);
/******/ 			if (fallback) return fallback();
/******/ 			fail(getInvalidVersionMessage(scope, scopeName, key, requiredVersion, eager));
/******/ 		});
/******/ 		var loadSingleton = /*#__PURE__*/ init((scopeName, scope, key, eager, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			var version = findSingletonVersionKey(scope, key, eager);
/******/ 			return get(scope[key][version]);
/******/ 		});
/******/ 		var loadSingletonVersion = /*#__PURE__*/ init((scopeName, scope, key, eager, requiredVersion, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			var version = findSingletonVersionKey(scope, key, eager);
/******/ 			if (!satisfy(requiredVersion, version)) {
/******/ 				warn(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			}
/******/ 			return get(scope[key][version]);
/******/ 		});
/******/ 		var loadStrictSingletonVersion = /*#__PURE__*/ init((scopeName, scope, key, eager, requiredVersion, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			var version = findSingletonVersionKey(scope, key, eager);
/******/ 			if (!satisfy(requiredVersion, version)) {
/******/ 				fail(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			}
/******/ 			return get(scope[key][version]);
/******/ 		});
/******/ 		var installedModules = {};
/******/ 		var moduleToHandlerMapping = {
/******/ 			"webpack/sharing/consume/default/react": () => (loadSingletonVersion("default", "react", false, [1,18,2,0])),
/******/ 			"webpack/sharing/consume/default/@codemirror/view": () => (loadSingletonVersion("default", "@codemirror/view", false, [1,6,9,6])),
/******/ 			"webpack/sharing/consume/default/@codemirror/state": () => (loadSingletonVersion("default", "@codemirror/state", false, [1,6,2,0])),
/******/ 			"webpack/sharing/consume/default/@codemirror/language": () => (loadSingletonVersion("default", "@codemirror/language", false, [1,6,0,0])),
/******/ 			"webpack/sharing/consume/default/@lezer/highlight": () => (loadSingletonVersion("default", "@lezer/highlight", false, [1,1,0,0])),
/******/ 			"webpack/sharing/consume/default/react-dom": () => (loadSingletonVersion("default", "react-dom", false, [1,18,2,0])),
/******/ 			"webpack/sharing/consume/default/@lezer/common": () => (loadSingletonVersion("default", "@lezer/common", false, [1,1,0,0])),
/******/ 			"webpack/sharing/consume/default/clsx/clsx": () => (loadStrictVersion("default", "clsx", false, [1,2,1,1], () => (__webpack_require__.e("node_modules_clsx_dist_clsx_mjs").then(() => (() => (__webpack_require__(/*! clsx */ "../../node_modules/clsx/dist/clsx.mjs"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/apputils": () => (loadSingletonVersion("default", "@jupyterlab/apputils", false, [1,4,3,0])),
/******/ 			"webpack/sharing/consume/default/@lumino/widgets": () => (loadSingletonVersion("default", "@lumino/widgets", false, [1,2,3,1,,"alpha",0])),
/******/ 			"webpack/sharing/consume/default/lucide-react/lucide-react": () => (loadStrictVersion("default", "lucide-react", false, [2,0,507,0], () => (__webpack_require__.e("vendors-node_modules_lucide-react_dist_esm_lucide-react_js").then(() => (() => (__webpack_require__(/*! lucide-react */ "../../node_modules/lucide-react/dist/esm/lucide-react.js"))))))),
/******/ 			"webpack/sharing/consume/default/@radix-ui/react-slot/@radix-ui/react-slot?3429": () => (loadStrictVersion("default", "@radix-ui/react-slot", false, [1,1,2,2], () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("node_modules_radix-ui_react-slot_dist_index_mjs-_dfa41")]).then(() => (() => (__webpack_require__(/*! @radix-ui/react-slot */ "../../node_modules/@radix-ui/react-slot/dist/index.mjs"))))))),
/******/ 			"webpack/sharing/consume/default/class-variance-authority/class-variance-authority": () => (loadStrictVersion("default", "class-variance-authority", false, [2,0,7,1], () => (__webpack_require__.e("node_modules_class-variance-authority_dist_index_mjs-_b7ca1").then(() => (() => (__webpack_require__(/*! class-variance-authority */ "../../node_modules/class-variance-authority/dist/index.mjs"))))))),
/******/ 			"webpack/sharing/consume/default/tailwind-merge/tailwind-merge": () => (loadStrictVersion("default", "tailwind-merge", false, [1,3,2,0], () => (__webpack_require__.e("vendors-node_modules_tailwind-merge_dist_bundle-mjs_mjs").then(() => (() => (__webpack_require__(/*! tailwind-merge */ "../../node_modules/tailwind-merge/dist/bundle-mjs.mjs"))))))),
/******/ 			"webpack/sharing/consume/default/mobx-react-lite/mobx-react-lite": () => (loadStrictVersion("default", "mobx-react-lite", false, [1,4,1,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_mobx-react-lite_es_index_js"), __webpack_require__.e("webpack_sharing_consume_default_mobx_mobx")]).then(() => (() => (__webpack_require__(/*! mobx-react-lite */ "../../node_modules/mobx-react-lite/es/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/mobx/mobx?9c47": () => (loadStrictVersion("default", "mobx", false, [1,6,13,7], () => (__webpack_require__.e("vendors-node_modules_mobx_dist_mobx_esm_js").then(() => (() => (__webpack_require__(/*! mobx */ "../../node_modules/mobx/dist/mobx.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/services": () => (loadSingletonVersion("default", "@jupyterlab/services", false, [1,7,2,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/coreutils": () => (loadSingletonVersion("default", "@jupyterlab/coreutils", false, [1,6,2,0])),
/******/ 			"webpack/sharing/consume/default/nanoid/nanoid": () => (loadStrictVersion("default", "nanoid", false, [1,5,1,5], () => (__webpack_require__.e("node_modules_nanoid_index_browser_js").then(() => (() => (__webpack_require__(/*! nanoid */ "./node_modules/nanoid/index.browser.js"))))))),
/******/ 			"webpack/sharing/consume/default/@radix-ui/react-scroll-area/@radix-ui/react-scroll-area": () => (loadStrictVersion("default", "@radix-ui/react-scroll-area", false, [1,1,2,8], () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("vendors-node_modules_radix-ui_primitive_dist_index_mjs-node_modules_radix-ui_react-context_di-836b8c"), __webpack_require__.e("vendors-node_modules_radix-ui_react-scroll-area_dist_index_mjs"), __webpack_require__.e("webpack_sharing_consume_default_radix-ui_react-slot_radix-ui_react-slot")]).then(() => (() => (__webpack_require__(/*! @radix-ui/react-scroll-area */ "../../node_modules/@radix-ui/react-scroll-area/dist/index.mjs"))))))),
/******/ 			"webpack/sharing/consume/default/react-markdown/react-markdown": () => (loadStrictVersion("default", "react-markdown", false, [1,10,1,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("vendors-node_modules_react-markdown_index_js")]).then(() => (() => (__webpack_require__(/*! react-markdown */ "../../node_modules/react-markdown/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@uiw/react-codemirror/@uiw/react-codemirror": () => (loadStrictVersion("default", "@uiw/react-codemirror", false, [1,4,23,11], () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("vendors-node_modules_uiw_react-codemirror_esm_index_js")]).then(() => (() => (__webpack_require__(/*! @uiw/react-codemirror */ "../../node_modules/@uiw/react-codemirror/esm/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@codemirror/lang-python/@codemirror/lang-python": () => (loadStrictVersion("default", "@codemirror/lang-python", false, [1,6,2,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_lezer_lr_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_lang-python_dist_index_js")]).then(() => (() => (__webpack_require__(/*! @codemirror/lang-python */ "../../node_modules/@codemirror/lang-python/dist/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@codemirror/lang-javascript/@codemirror/lang-javascript?a422": () => (loadStrictVersion("default", "@codemirror/lang-javascript", false, [1,6,2,3], () => (Promise.all([__webpack_require__.e("vendors-node_modules_lezer_lr_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_lang-javascript_dist_index_js")]).then(() => (() => (__webpack_require__(/*! @codemirror/lang-javascript */ "../../node_modules/@codemirror/lang-javascript/dist/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@codemirror/lang-markdown/@codemirror/lang-markdown": () => (loadStrictVersion("default", "@codemirror/lang-markdown", false, [1,6,3,2], () => (Promise.all([__webpack_require__.e("vendors-node_modules_lezer_lr_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_lang-markdown_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_lang-javascript_codemirror_lang-javascript")]).then(() => (() => (__webpack_require__(/*! @codemirror/lang-markdown */ "../../node_modules/@codemirror/lang-markdown/dist/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@radix-ui/react-tooltip/@radix-ui/react-tooltip": () => (loadStrictVersion("default", "@radix-ui/react-tooltip", false, [1,1,2,6], () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("vendors-node_modules_radix-ui_primitive_dist_index_mjs-node_modules_radix-ui_react-context_di-836b8c"), __webpack_require__.e("vendors-node_modules_radix-ui_react-tooltip_dist_index_mjs"), __webpack_require__.e("webpack_sharing_consume_default_radix-ui_react-slot_radix-ui_react-slot")]).then(() => (() => (__webpack_require__(/*! @radix-ui/react-tooltip */ "../../node_modules/@radix-ui/react-tooltip/dist/index.mjs"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/ui-components": () => (loadSingletonVersion("default", "@jupyterlab/ui-components", false, [1,4,2,0])),
/******/ 			"webpack/sharing/consume/default/sonner/sonner": () => (loadStrictVersion("default", "sonner", false, [1,2,0,3], () => (__webpack_require__.e("vendors-node_modules_sonner_dist_index_mjs").then(() => (() => (__webpack_require__(/*! sonner */ "../../node_modules/sonner/dist/index.mjs"))))))),
/******/ 			"webpack/sharing/consume/default/@codemirror/merge/@codemirror/merge": () => (loadStrictVersion("default", "@codemirror/merge", false, [1,6,10,1], () => (__webpack_require__.e("vendors-node_modules_codemirror_merge_dist_index_js").then(() => (() => (__webpack_require__(/*! @codemirror/merge */ "../../node_modules/@codemirror/merge/dist/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/next-themes/next-themes": () => (loadStrictVersion("default", "next-themes", false, [2,0,4,6], () => (__webpack_require__.e("node_modules_next-themes_dist_index_mjs-_548d1").then(() => (() => (__webpack_require__(/*! next-themes */ "../../node_modules/next-themes/dist/index.mjs"))))))),
/******/ 			"webpack/sharing/consume/default/@radix-ui/react-avatar/@radix-ui/react-avatar": () => (loadStrictVersion("default", "@radix-ui/react-avatar", false, [1,1,1,9], () => (Promise.all([__webpack_require__.e("vendors-node_modules_react_jsx-runtime_js"), __webpack_require__.e("vendors-node_modules_radix-ui_react-avatar_dist_index_mjs"), __webpack_require__.e("webpack_sharing_consume_default_radix-ui_react-slot_radix-ui_react-slot")]).then(() => (() => (__webpack_require__(/*! @radix-ui/react-avatar */ "../../node_modules/@radix-ui/react-avatar/dist/index.mjs"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/rendermime": () => (loadSingletonVersion("default", "@jupyterlab/rendermime", false, [1,4,2,0])),
/******/ 			"webpack/sharing/consume/default/embla-carousel-react/embla-carousel-react": () => (loadStrictVersion("default", "embla-carousel-react", false, [1,8,6,0], () => (__webpack_require__.e("vendors-node_modules_embla-carousel-react_esm_embla-carousel-react_esm_js").then(() => (() => (__webpack_require__(/*! embla-carousel-react */ "../../node_modules/embla-carousel-react/esm/embla-carousel-react.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/notebook": () => (loadSingletonVersion("default", "@jupyterlab/notebook", false, [1,4,2,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/settingregistry": () => (loadSingletonVersion("default", "@jupyterlab/settingregistry", false, [1,4,2,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/completer": () => (loadSingletonVersion("default", "@jupyterlab/completer", false, [1,4,2,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/codemirror": () => (loadSingletonVersion("default", "@jupyterlab/codemirror", false, [1,4,2,0])),
/******/ 			"webpack/sharing/consume/default/@lumino/coreutils": () => (loadSingletonVersion("default", "@lumino/coreutils", false, [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@lumino/signaling": () => (loadSingletonVersion("default", "@lumino/signaling", false, [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/docregistry": () => (loadVersion("default", "@jupyterlab/docregistry", false, [1,4,2,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/statusbar": () => (loadSingletonVersion("default", "@jupyterlab/statusbar", false, [1,4,2,0])),
/******/ 			"webpack/sharing/consume/default/@codemirror/lang-javascript/@codemirror/lang-javascript?4e87": () => (loadStrictVersion("default", "@codemirror/lang-javascript", false, [1,6,0,0], () => (__webpack_require__.e("vendors-node_modules_codemirror_lang-javascript_dist_index_js").then(() => (() => (__webpack_require__(/*! @codemirror/lang-javascript */ "../../node_modules/@codemirror/lang-javascript/dist/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@radix-ui/react-slot/@radix-ui/react-slot?bbd5": () => (loadStrictVersion("default", "@radix-ui/react-slot", false, [4,1,2,3], () => (__webpack_require__.e("node_modules_radix-ui_react-slot_dist_index_mjs-_dfa42").then(() => (() => (__webpack_require__(/*! @radix-ui/react-slot */ "../../node_modules/@radix-ui/react-slot/dist/index.mjs"))))))),
/******/ 			"webpack/sharing/consume/default/mobx/mobx?9232": () => (loadStrictVersion("default", "mobx", false, [1,6,9,0], () => (__webpack_require__.e("vendors-node_modules_mobx_dist_mobx_esm_js").then(() => (() => (__webpack_require__(/*! mobx */ "../../node_modules/mobx/dist/mobx.esm.js")))))))
/******/ 		};
/******/ 		// no consumes in initial chunks
/******/ 		var chunkMapping = {
/******/ 			"webpack_sharing_consume_default_react": [
/******/ 				"webpack/sharing/consume/default/react"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_codemirro-44efd7": [
/******/ 				"webpack/sharing/consume/default/@codemirror/view",
/******/ 				"webpack/sharing/consume/default/@codemirror/state",
/******/ 				"webpack/sharing/consume/default/@codemirror/language",
/******/ 				"webpack/sharing/consume/default/@lezer/highlight"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_react-dom": [
/******/ 				"webpack/sharing/consume/default/react-dom"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_lezer_common": [
/******/ 				"webpack/sharing/consume/default/@lezer/common"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_clsx_clsx": [
/******/ 				"webpack/sharing/consume/default/clsx/clsx"
/******/ 			],
/******/ 			"lib_index_js": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/apputils",
/******/ 				"webpack/sharing/consume/default/@lumino/widgets",
/******/ 				"webpack/sharing/consume/default/lucide-react/lucide-react",
/******/ 				"webpack/sharing/consume/default/@radix-ui/react-slot/@radix-ui/react-slot?3429",
/******/ 				"webpack/sharing/consume/default/class-variance-authority/class-variance-authority",
/******/ 				"webpack/sharing/consume/default/tailwind-merge/tailwind-merge",
/******/ 				"webpack/sharing/consume/default/mobx-react-lite/mobx-react-lite",
/******/ 				"webpack/sharing/consume/default/mobx/mobx?9c47",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/services",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/coreutils",
/******/ 				"webpack/sharing/consume/default/nanoid/nanoid",
/******/ 				"webpack/sharing/consume/default/@radix-ui/react-scroll-area/@radix-ui/react-scroll-area",
/******/ 				"webpack/sharing/consume/default/react-markdown/react-markdown",
/******/ 				"webpack/sharing/consume/default/@uiw/react-codemirror/@uiw/react-codemirror",
/******/ 				"webpack/sharing/consume/default/@codemirror/lang-python/@codemirror/lang-python",
/******/ 				"webpack/sharing/consume/default/@codemirror/lang-javascript/@codemirror/lang-javascript?a422",
/******/ 				"webpack/sharing/consume/default/@codemirror/lang-markdown/@codemirror/lang-markdown",
/******/ 				"webpack/sharing/consume/default/@radix-ui/react-tooltip/@radix-ui/react-tooltip",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/ui-components",
/******/ 				"webpack/sharing/consume/default/sonner/sonner",
/******/ 				"webpack/sharing/consume/default/@codemirror/merge/@codemirror/merge",
/******/ 				"webpack/sharing/consume/default/next-themes/next-themes",
/******/ 				"webpack/sharing/consume/default/@radix-ui/react-avatar/@radix-ui/react-avatar",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/rendermime",
/******/ 				"webpack/sharing/consume/default/embla-carousel-react/embla-carousel-react",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/notebook",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/settingregistry",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/completer",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/codemirror",
/******/ 				"webpack/sharing/consume/default/@lumino/coreutils",
/******/ 				"webpack/sharing/consume/default/@lumino/signaling",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/docregistry",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/statusbar"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_codemirror_lang-javascript_codemirror_lang-javascript": [
/******/ 				"webpack/sharing/consume/default/@codemirror/lang-javascript/@codemirror/lang-javascript?4e87"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_radix-ui_react-slot_radix-ui_react-slot": [
/******/ 				"webpack/sharing/consume/default/@radix-ui/react-slot/@radix-ui/react-slot?bbd5"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_mobx_mobx": [
/******/ 				"webpack/sharing/consume/default/mobx/mobx?9232"
/******/ 			]
/******/ 		};
/******/ 		var startedInstallModules = {};
/******/ 		__webpack_require__.f.consumes = (chunkId, promises) => {
/******/ 			if(__webpack_require__.o(chunkMapping, chunkId)) {
/******/ 				chunkMapping[chunkId].forEach((id) => {
/******/ 					if(__webpack_require__.o(installedModules, id)) return promises.push(installedModules[id]);
/******/ 					if(!startedInstallModules[id]) {
/******/ 					var onFactory = (factory) => {
/******/ 						installedModules[id] = 0;
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							module.exports = factory();
/******/ 						}
/******/ 					};
/******/ 					startedInstallModules[id] = true;
/******/ 					var onError = (error) => {
/******/ 						delete installedModules[id];
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							throw error;
/******/ 						}
/******/ 					};
/******/ 					try {
/******/ 						var promise = moduleToHandlerMapping[id]();
/******/ 						if(promise.then) {
/******/ 							promises.push(installedModules[id] = promise.then(onFactory)['catch'](onError));
/******/ 						} else onFactory(promise);
/******/ 					} catch(e) { onError(e); }
/******/ 					}
/******/ 				});
/******/ 			}
/******/ 		}
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		__webpack_require__.b = document.baseURI || self.location.href;
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"runcell": 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.j = (chunkId, promises) => {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if(!/^webpack_sharing_consume_default_(c(odemirror_lang(\-javascript_codemirror_lang\-javascript|uage\-webpack_sharing_consume_default_codemirro\-44efd7)|lsx_clsx)|r(eact(|\-dom)|adix\-ui_react\-slot_radix\-ui_react\-slot)|lezer_common|mobx_mobx)$/.test(chunkId)) {
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise((resolve, reject) => (installedChunkData = installedChunks[chunkId] = [resolve, reject]));
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = (event) => {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		// no on chunks loaded
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 		
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkruncell"] = self["webpackChunkruncell"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/nonce */
/******/ 	(() => {
/******/ 		__webpack_require__.nc = undefined;
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// module cache are used so entry inlining is disabled
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	var __webpack_exports__ = __webpack_require__("webpack/container/entry/runcell");
/******/ 	(_JUPYTERLAB = typeof _JUPYTERLAB === "undefined" ? {} : _JUPYTERLAB).runcell = __webpack_exports__;
/******/ 	
/******/ })()
;
//# sourceMappingURL=remoteEntry.078864bb09ce68cd283d.js.map