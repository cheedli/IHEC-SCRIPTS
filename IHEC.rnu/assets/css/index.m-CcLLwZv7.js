import{s as q,p as A,f as Z}from"./parse-B3pZ8sEA.js";var T=q,U=A,F=Z,$={formats:F,parse:U,stringify:T};function _(c,a){for(var t=0;t<a.length;t++){var n=a[t];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(c,typeof(s=function(e,i){if(typeof e!="object"||e===null)return e;var r=e[Symbol.toPrimitive];if(r!==void 0){var o=r.call(e,"string");if(typeof o!="object")return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return String(e)}(n.key))=="symbol"?s:String(s),n)}var s}function k(c,a,t){return a&&_(c.prototype,a),t&&_(c,t),Object.defineProperty(c,"prototype",{writable:!1}),c}function v(){return v=Object.assign?Object.assign.bind():function(c){for(var a=1;a<arguments.length;a++){var t=arguments[a];for(var n in t)Object.prototype.hasOwnProperty.call(t,n)&&(c[n]=t[n])}return c},v.apply(this,arguments)}function j(c){return j=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(a){return a.__proto__||Object.getPrototypeOf(a)},j(c)}function w(c,a){return w=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(t,n){return t.__proto__=n,t},w(c,a)}function P(c,a,t){return P=function(){if(typeof Reflect>"u"||!Reflect.construct||Reflect.construct.sham)return!1;if(typeof Proxy=="function")return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],function(){})),!0}catch{return!1}}()?Reflect.construct.bind():function(n,s,e){var i=[null];i.push.apply(i,s);var r=new(Function.bind.apply(n,i));return e&&w(r,e.prototype),r},P.apply(null,arguments)}function S(c){var a=typeof Map=="function"?new Map:void 0;return S=function(t){if(t===null||Function.toString.call(t).indexOf("[native code]")===-1)return t;if(typeof t!="function")throw new TypeError("Super expression must either be null or a function");if(a!==void 0){if(a.has(t))return a.get(t);a.set(t,n)}function n(){return P(t,arguments,j(this).constructor)}return n.prototype=Object.create(t.prototype,{constructor:{value:n,enumerable:!1,writable:!0,configurable:!0}}),w(n,t)},S(c)}var O=function(){function c(t,n,s){var e,i;this.name=t,this.definition=n,this.bindings=(e=n.bindings)!=null?e:{},this.wheres=(i=n.wheres)!=null?i:{},this.config=s}var a=c.prototype;return a.matchesUrl=function(t){var n=this;if(!this.definition.methods.includes("GET"))return!1;var s=this.template.replace(/(\/?){([^}?]*)(\??)}/g,function(h,f,g,p){var l,y="(?<"+g+">"+(((l=n.wheres[g])==null?void 0:l.replace(/(^\^)|(\$$)/g,""))||"[^/?]+")+")";return p?"("+f+y+")?":""+f+y}).replace(/^\w+:\/\//,""),e=t.replace(/^\w+:\/\//,"").split("?"),i=e[0],r=e[1],o=new RegExp("^"+s+"/?$").exec(decodeURI(i));if(o){for(var u in o.groups)o.groups[u]=typeof o.groups[u]=="string"?decodeURIComponent(o.groups[u]):o.groups[u];return{params:o.groups,query:$.parse(r)}}return!1},a.compile=function(t){var n=this;return this.parameterSegments.length?this.template.replace(/{([^}?]+)(\??)}/g,function(s,e,i){var r,o;if(!i&&[null,void 0].includes(t[e]))throw new Error("Ziggy error: '"+e+"' parameter is required for route '"+n.name+"'.");if(n.wheres[e]&&!new RegExp("^"+(i?"("+n.wheres[e]+")?":n.wheres[e])+"$").test((o=t[e])!=null?o:""))throw new Error("Ziggy error: '"+e+"' parameter does not match required format '"+n.wheres[e]+"' for route '"+n.name+"'.");return encodeURI((r=t[e])!=null?r:"").replace(/%7C/g,"|").replace(/%25/g,"%").replace(/\$/g,"%24")}).replace(this.origin+"//",this.origin+"/").replace(/\/+$/,""):this.template},k(c,[{key:"template",get:function(){var t=(this.origin+"/"+this.definition.uri).replace(/\/+$/,"");return t===""?"/":t}},{key:"origin",get:function(){return this.config.absolute?this.definition.domain?""+this.config.url.match(/^\w+:\/\//)[0]+this.definition.domain+(this.config.port?":"+this.config.port:""):this.config.url:""}},{key:"parameterSegments",get:function(){var t,n;return(t=(n=this.template.match(/{[^}?]+\??}/g))==null?void 0:n.map(function(s){return{name:s.replace(/{|\??}/g,""),required:!/\?}$/.test(s)}}))!=null?t:[]}}]),c}(),I=function(c){var a,t;function n(e,i,r,o){var u;if(r===void 0&&(r=!0),(u=c.call(this)||this).t=o??(typeof Ziggy<"u"?Ziggy:globalThis==null?void 0:globalThis.Ziggy),u.t=v({},u.t,{absolute:r}),e){if(!u.t.routes[e])throw new Error("Ziggy error: route '"+e+"' is not in the route list.");u.i=new O(e,u.t.routes[e],u.t),u.u=u.o(i)}return u}t=c,(a=n).prototype=Object.create(t.prototype),a.prototype.constructor=a,w(a,t);var s=n.prototype;return s.toString=function(){var e=this,i=Object.keys(this.u).filter(function(r){return!e.i.parameterSegments.some(function(o){return o.name===r})}).filter(function(r){return r!=="_query"}).reduce(function(r,o){var u;return v({},r,((u={})[o]=e.u[o],u))},{});return this.i.compile(this.u)+$.stringify(v({},i,this.u._query),{addQueryPrefix:!0,arrayFormat:"indices",encodeValuesOnly:!0,skipNulls:!0,encoder:function(r,o){return typeof r=="boolean"?Number(r):o(r)}})},s.l=function(e){var i=this;e?this.t.absolute&&e.startsWith("/")&&(e=this.v().host+e):e=this.h();var r={},o=Object.entries(this.t.routes).find(function(u){return r=new O(u[0],u[1],i.t).matchesUrl(e)})||[void 0,void 0];return v({name:o[0]},r,{route:o[1]})},s.h=function(){var e=this.v(),i=e.pathname,r=e.search;return(this.t.absolute?e.host+i:i.replace(this.t.url.replace(/^\w*:\/\/[^/]+/,""),"").replace(/^\/+/,"/"))+r},s.current=function(e,i){var r=this.l(),o=r.name,u=r.params,h=r.query,f=r.route;if(!e)return o;var g=new RegExp("^"+e.replace(/\./g,"\\.").replace(/\*/g,".*")+"$").test(o);if([null,void 0].includes(i)||!g)return g;var p=new O(o,f,this.t);i=this.o(i,p);var l=v({},u,h);return!(!Object.values(i).every(function(y){return!y})||Object.values(l).some(function(y){return y!==void 0}))||function y(E,m){return Object.entries(E).every(function(R){var d=R[0],b=R[1];return Array.isArray(b)&&Array.isArray(m[d])?b.every(function(x){return m[d].includes(x)}):typeof b=="object"&&typeof m[d]=="object"&&b!==null&&m[d]!==null?y(b,m[d]):m[d]==b})}(i,l)},s.v=function(){var e,i,r,o,u,h,f=typeof window<"u"?window.location:{},g=f.host,p=f.pathname,l=f.search;return{host:(e=(i=this.t.location)==null?void 0:i.host)!=null?e:g===void 0?"":g,pathname:(r=(o=this.t.location)==null?void 0:o.pathname)!=null?r:p===void 0?"":p,search:(u=(h=this.t.location)==null?void 0:h.search)!=null?u:l===void 0?"":l}},s.has=function(e){return Object.keys(this.t.routes).includes(e)},s.o=function(e,i){var r=this;e===void 0&&(e={}),i===void 0&&(i=this.i),e!=null||(e={}),e=["string","number"].includes(typeof e)?[e]:e;var o=i.parameterSegments.filter(function(h){return!r.t.defaults[h.name]});if(Array.isArray(e))e=e.reduce(function(h,f,g){var p,l;return v({},h,o[g]?((p={})[o[g].name]=f,p):typeof f=="object"?f:((l={})[f]="",l))},{});else if(o.length===1&&!e[o[0].name]&&(e.hasOwnProperty(Object.values(i.bindings)[0])||e.hasOwnProperty("id"))){var u;(u={})[o[0].name]=e,e=u}return v({},this.g(i),this.p(e,i))},s.g=function(e){var i=this;return e.parameterSegments.filter(function(r){return i.t.defaults[r.name]}).reduce(function(r,o,u){var h,f=o.name;return v({},r,((h={})[f]=i.t.defaults[f],h))},{})},s.p=function(e,i){var r=i.bindings,o=i.parameterSegments;return Object.entries(e).reduce(function(u,h){var f,g,p=h[0],l=h[1];if(!l||typeof l!="object"||Array.isArray(l)||!o.some(function(y){return y.name===p}))return v({},u,((g={})[p]=l,g));if(!l.hasOwnProperty(r[p])){if(!l.hasOwnProperty("id"))throw new Error("Ziggy error: object passed as '"+p+"' parameter is missing route model binding key '"+r[p]+"'.");r[p]="id"}return v({},u,((f={})[p]=l[r[p]],f))},{})},s.valueOf=function(){return this.toString()},s.check=function(e){return this.has(e)},k(n,[{key:"params",get:function(){var e=this.l();return v({},e.params,e.query)}}]),n}(S(String));function C(c,a,t,n){var s=new I(c,a,t,n);return c?s.toString():s}export{C as l};