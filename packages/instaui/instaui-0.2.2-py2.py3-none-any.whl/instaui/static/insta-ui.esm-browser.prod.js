var Wn = Object.defineProperty;
var Un = (e, t, n) => t in e ? Wn(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var F = (e, t, n) => Un(e, typeof t != "symbol" ? t + "" : t, n);
import * as Gn from "vue";
import { toRaw as Kt, customRef as De, toValue as q, unref as D, watch as K, nextTick as Ae, isRef as zt, shallowRef as X, ref as H, watchEffect as Qt, computed as W, readonly as qn, provide as Te, inject as Z, shallowReactive as Hn, defineComponent as L, reactive as Kn, h as A, getCurrentInstance as Jt, normalizeStyle as zn, normalizeClass as Ce, toDisplayString as Me, onUnmounted as dt, Fragment as Fe, vModelDynamic as Qn, vShow as Jn, resolveDynamicComponent as Yn, normalizeProps as Xn, withDirectives as Zn, onErrorCaptured as er, openBlock as re, createElementBlock as fe, createElementVNode as tr, createVNode as nr, withCtx as rr, renderList as or, createBlock as sr, createCommentVNode as ir, TransitionGroup as Yt, KeepAlive as ar } from "vue";
let Xt;
function cr(e) {
  Xt = e;
}
function Ze() {
  return Xt;
}
function $e() {
  const { queryPath: e, pathParams: t, queryParams: n } = Ze();
  return {
    path: e,
    ...t === void 0 ? {} : { params: t },
    ...n === void 0 ? {} : { queryParams: n }
  };
}
class ur extends Map {
  constructor(t) {
    super(), this.factory = t;
  }
  getOrDefault(t) {
    if (!this.has(t)) {
      const n = this.factory();
      return this.set(t, n), n;
    }
    return super.get(t);
  }
}
function Oe(e) {
  return new ur(e);
}
function bt(e, t) {
  Object.entries(e).forEach(([n, r]) => t(r, n));
}
function Be(e, t) {
  return Zt(e, {
    valueFn: t
  });
}
function Zt(e, t) {
  const { valueFn: n, keyFn: r } = t;
  return Object.fromEntries(
    Object.entries(e).map(([o, i], s) => [
      r ? r(o, i) : o,
      n(i, o, s)
    ])
  );
}
function en(e, t, n) {
  if (Array.isArray(t)) {
    const [o, ...i] = t;
    switch (o) {
      case "!":
        return !e;
      case "+":
        return e + i[0];
      case "~+":
        return i[0] + e;
    }
  }
  const r = tn(t, n);
  return e[r];
}
function tn(e, t) {
  if (typeof e == "string" || typeof e == "number")
    return e;
  if (!Array.isArray(e))
    throw new Error(`Invalid path ${e}`);
  const [n, ...r] = e;
  switch (n) {
    case "bind":
      if (!t)
        throw new Error("No bindable function provided");
      return t(r[0]);
    default:
      throw new Error(`Invalid flag ${n} in array at ${e}`);
  }
}
function Re(e, t, n) {
  return t.reduce(
    (r, o) => en(r, o, n),
    e
  );
}
function et(e, t, n, r) {
  t.reduce((o, i, s) => {
    if (s === t.length - 1)
      o[tn(i, r)] = n;
    else
      return en(o, i, r);
  }, e);
}
function lr(e, t, n) {
  t.reduce((r, o, i) => {
    if (i === t.length - 1)
      r[o] = n;
    else
      return r[o];
  }, e);
}
function fr(e, t) {
  return t.reduce((n, r) => n[r], e);
}
const dr = structuredClone || ((e) => JSON.parse(JSON.stringify(e)));
function nn(e) {
  return typeof e == "function" ? e : dr(Kt(e));
}
class hr {
  toString() {
    return "";
  }
}
const Se = new hr();
function be(e) {
  return Kt(e) === Se;
}
function Ot(e, t, n) {
  const { paths: r, getBindableValueFn: o } = t, { paths: i, getBindableValueFn: s } = t;
  return r === void 0 || r.length === 0 ? e : De(() => ({
    get() {
      try {
        return Re(
          q(e),
          r,
          o
        );
      } catch {
        return;
      }
    },
    set(c) {
      et(
        q(e),
        i || r,
        c,
        s
      );
    }
  }));
}
function ht(e) {
  return De((t, n) => ({
    get() {
      return t(), e;
    },
    set(r) {
      !be(e) && JSON.stringify(r) === JSON.stringify(e) || (e = r, n());
    }
  }));
}
function ve(e) {
  return typeof e == "function" ? e() : D(e);
}
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const tt = () => {
};
function nt(e, t = !1, n = "Timeout") {
  return new Promise((r, o) => {
    setTimeout(t ? () => o(n) : r, e);
  });
}
function rt(e, t = !1) {
  function n(a, { flush: f = "sync", deep: h = !1, timeout: v, throwOnTimeout: p } = {}) {
    let g = null;
    const _ = [new Promise((b) => {
      g = K(
        e,
        (R) => {
          a(R) !== t && (g ? g() : Ae(() => g == null ? void 0 : g()), b(R));
        },
        {
          flush: f,
          deep: h,
          immediate: !0
        }
      );
    })];
    return v != null && _.push(
      nt(v, p).then(() => ve(e)).finally(() => g == null ? void 0 : g())
    ), Promise.race(_);
  }
  function r(a, f) {
    if (!zt(a))
      return n((R) => R === a, f);
    const { flush: h = "sync", deep: v = !1, timeout: p, throwOnTimeout: g } = f ?? {};
    let y = null;
    const b = [new Promise((R) => {
      y = K(
        [e, a],
        ([$, G]) => {
          t !== ($ === G) && (y ? y() : Ae(() => y == null ? void 0 : y()), R($));
        },
        {
          flush: h,
          deep: v,
          immediate: !0
        }
      );
    })];
    return p != null && b.push(
      nt(p, g).then(() => ve(e)).finally(() => (y == null || y(), ve(e)))
    ), Promise.race(b);
  }
  function o(a) {
    return n((f) => !!f, a);
  }
  function i(a) {
    return r(null, a);
  }
  function s(a) {
    return r(void 0, a);
  }
  function c(a) {
    return n(Number.isNaN, a);
  }
  function l(a, f) {
    return n((h) => {
      const v = Array.from(h);
      return v.includes(a) || v.includes(ve(a));
    }, f);
  }
  function d(a) {
    return u(1, a);
  }
  function u(a = 1, f) {
    let h = -1;
    return n(() => (h += 1, h >= a), f);
  }
  return Array.isArray(ve(e)) ? {
    toMatch: n,
    toContains: l,
    changed: d,
    changedTimes: u,
    get not() {
      return rt(e, !t);
    }
  } : {
    toMatch: n,
    toBe: r,
    toBeTruthy: o,
    toBeNull: i,
    toBeNaN: c,
    toBeUndefined: s,
    changed: d,
    changedTimes: u,
    get not() {
      return rt(e, !t);
    }
  };
}
function pr(e) {
  return rt(e);
}
function mr(e, t, n) {
  let r;
  zt(n) ? r = {
    evaluating: n
  } : r = n || {};
  const {
    lazy: o = !1,
    evaluating: i = void 0,
    shallow: s = !0,
    onError: c = tt
  } = r, l = H(!o), d = s ? X(t) : H(t);
  let u = 0;
  return Qt(async (a) => {
    if (!l.value)
      return;
    u++;
    const f = u;
    let h = !1;
    i && Promise.resolve().then(() => {
      i.value = !0;
    });
    try {
      const v = await e((p) => {
        a(() => {
          i && (i.value = !1), h || p();
        });
      });
      f === u && (d.value = v);
    } catch (v) {
      c(v);
    } finally {
      i && f === u && (i.value = !1), h = !0;
    }
  }), o ? W(() => (l.value = !0, d.value)) : d;
}
function gr(e, t, n) {
  const {
    immediate: r = !0,
    delay: o = 0,
    onError: i = tt,
    onSuccess: s = tt,
    resetOnExecute: c = !0,
    shallow: l = !0,
    throwError: d
  } = {}, u = l ? X(t) : H(t), a = H(!1), f = H(!1), h = X(void 0);
  async function v(y = 0, ..._) {
    c && (u.value = t), h.value = void 0, a.value = !1, f.value = !0, y > 0 && await nt(y);
    const b = typeof e == "function" ? e(..._) : e;
    try {
      const R = await b;
      u.value = R, a.value = !0, s(R);
    } catch (R) {
      if (h.value = R, i(R), d)
        throw R;
    } finally {
      f.value = !1;
    }
    return u.value;
  }
  r && v(o);
  const p = {
    state: u,
    isReady: a,
    isLoading: f,
    error: h,
    execute: v
  };
  function g() {
    return new Promise((y, _) => {
      pr(f).toBe(!1).then(() => y(p)).catch(_);
    });
  }
  return {
    ...p,
    then(y, _) {
      return g().then(y, _);
    }
  };
}
function B(e, t) {
  t = t || {};
  const n = [...Object.keys(t), "__Vue"], r = [...Object.values(t), Gn];
  try {
    return new Function(...n, `return (${e})`)(...r);
  } catch (o) {
    throw new Error(o + " in function code: " + e);
  }
}
function vr(e) {
  if (e.startsWith(":")) {
    e = e.slice(1);
    try {
      return B(e);
    } catch (t) {
      throw new Error(t + " in function code: " + e);
    }
  }
}
function rn(e) {
  return e.constructor.name === "AsyncFunction";
}
function yr(e, t) {
  const { deepCompare: n = !1 } = e;
  return n ? ht(e.value) : H(e.value);
}
function wr(e, t, n) {
  const { bind: r = {}, code: o, const: i = [] } = e, s = Object.values(r).map((u, a) => i[a] === 1 ? u : t.getVueRefObjectOrValue(u));
  if (rn(new Function(o)))
    return mr(
      async () => {
        const u = Object.fromEntries(
          Object.keys(r).map((a, f) => [a, s[f]])
        );
        return await B(o, u)();
      },
      null,
      { lazy: !0 }
    );
  const c = Object.fromEntries(
    Object.keys(r).map((u, a) => [u, s[a]])
  ), l = B(o, c);
  return W(l);
}
function Er(e, t, n) {
  const {
    inputs: r = [],
    code: o,
    slient: i,
    data: s,
    asyncInit: c = null,
    deepEqOnInput: l = 0
  } = e, d = i || Array(r.length).fill(0), u = s || Array(r.length).fill(0), a = r.filter((g, y) => d[y] === 0 && u[y] === 0).map((g) => t.getVueRefObject(g));
  function f() {
    return r.map(
      (g, y) => u[y] === 1 ? g : t.getObjectToValue(g)
    );
  }
  const h = B(o), v = l === 0 ? X(Se) : ht(Se), p = { immediate: !0, deep: !0 };
  return rn(h) ? (v.value = c, K(
    a,
    async () => {
      f().some(be) || (v.value = await h(...f()));
    },
    p
  )) : K(
    a,
    () => {
      const g = f();
      g.some(be) || (v.value = h(...g));
    },
    p
  ), qn(v);
}
function _r() {
  return [];
}
const Ve = Oe(_r);
function Sr(e, t) {
  var i, s, c, l, d;
  const n = Ve.getOrDefault(e.id), r = /* @__PURE__ */ new Map();
  n.push(r), t.replaceSnapshot({
    scopeSnapshot: on()
  });
  const o = (u, a) => {
    r.set(u.id, a);
  };
  return (i = e.refs) == null || i.forEach((u) => {
    o(u, yr(u));
  }), (s = e.web_computed) == null || s.forEach((u) => {
    const { init: a } = u, f = u.deepEqOnInput === void 0 ? X(a ?? Se) : ht(a ?? Se);
    o(u, f);
  }), (c = e.vue_computed) == null || c.forEach((u) => {
    o(
      u,
      wr(u, t)
    );
  }), (l = e.js_computed) == null || l.forEach((u) => {
    o(
      u,
      Er(u, t)
    );
  }), (d = e.data) == null || d.forEach((u) => {
    o(u, u.value);
  }), n.length - 1;
}
function on() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Ve) {
    const o = r[r.length - 1];
    e.set(n, [o]);
  }
  function t(n) {
    return sn(n, e);
  }
  return {
    getVueRef: t
  };
}
function br(e) {
  return sn(e, Ve);
}
function sn(e, t) {
  const n = t.get(e.sid);
  if (!n)
    throw new Error(`Scope ${e.sid} not found`);
  const o = n[n.length - 1].get(e.id);
  if (!o)
    throw new Error(`Var ${e.id} not found in scope ${e.sid}`);
  return o;
}
function Or(e) {
  Ve.delete(e);
}
function Rr(e, t) {
  const n = Ve.get(e);
  n && n.splice(t, 1);
}
const pt = Oe(() => []);
function Vr(e) {
  var r;
  const t = /* @__PURE__ */ new Map(), n = pt.getOrDefault(e.id).push(t);
  return (r = e.eRefs) == null || r.forEach((o) => {
    const i = X();
    t.set(o.id, i);
  }), n;
}
function Pr(e, t) {
  const n = pt.get(e);
  n && n.splice(t, 1);
}
function an() {
  const e = new Map(
    Array.from(pt.entries()).map(([n, r]) => [
      n,
      r[r.length - 1]
    ])
  );
  function t(n) {
    return e.get(n.sid).get(n.id);
  }
  return {
    getRef: t
  };
}
var N;
((e) => {
  function t(a) {
    return a.type === "var";
  }
  e.isVar = t;
  function n(a) {
    return a.type === "routePar";
  }
  e.isRouterParams = n;
  function r(a) {
    return a.type === "routeAct";
  }
  e.isRouterAction = r;
  function o(a) {
    return a.type === "jsFn";
  }
  e.isJsFn = o;
  function i(a) {
    return a.type === "vf";
  }
  e.isVForItem = i;
  function s(a) {
    return a.type === "vf-i";
  }
  e.isVForIndex = s;
  function c(a) {
    return a.type === "sp";
  }
  e.isSlotProp = c;
  function l(a) {
    return a.type === "event";
  }
  e.isEventContext = l;
  function d(a) {
    return a.type === "ele_ref";
  }
  e.isElementRef = d;
  function u(a) {
    return a.type !== void 0;
  }
  e.IsBinding = u;
})(N || (N = {}));
const Le = Oe(() => []);
function kr(e) {
  const t = Le.getOrDefault(e);
  return t.push(X({})), t.length - 1;
}
function Nr(e, t, n) {
  Le.get(e)[t].value = n;
}
function Ir(e) {
  Le.delete(e);
}
function Tr() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Le) {
    const o = r[r.length - 1];
    e.set(n, o);
  }
  function t(n) {
    return e.get(n.id).value[n.name];
  }
  return {
    getPropsValue: t
  };
}
const cn = /* @__PURE__ */ new Map(), mt = Oe(() => /* @__PURE__ */ new Map()), un = /* @__PURE__ */ new Set(), ln = Symbol("vfor");
function Ar(e) {
  const t = fn() ?? {};
  Te(ln, { ...t, [e.fid]: e.key });
}
function fn() {
  return Z(ln, void 0);
}
function Cr() {
  const e = fn(), t = /* @__PURE__ */ new Map();
  return e === void 0 || Object.keys(e).forEach((n) => {
    t.set(n, e[n]);
  }), t;
}
function $r(e, t, n, r) {
  if (r) {
    un.add(e);
    return;
  }
  let o;
  if (n)
    o = new Lr(t);
  else {
    const i = Array.isArray(t) ? t : Object.entries(t).map(([s, c], l) => [c, s, l]);
    o = new Br(i);
  }
  cn.set(e, o);
}
function xr(e, t, n) {
  const r = mt.getOrDefault(e);
  r.has(t) || r.set(t, H(n)), r.get(t).value = n;
}
function jr(e) {
  const t = /* @__PURE__ */ new Set();
  function n(o) {
    t.add(o);
  }
  function r() {
    const o = mt.get(e);
    o !== void 0 && o.forEach((i, s) => {
      t.has(s) || o.delete(s);
    });
  }
  return {
    add: n,
    removeUnusedKeys: r
  };
}
function Dr(e) {
  const t = e, n = Cr();
  function r(o) {
    const i = n.get(o) ?? t;
    return mt.get(o).get(i).value;
  }
  return {
    getVForIndex: r
  };
}
function Mr(e) {
  return cn.get(e.binding.fid).createRefObjectWithPaths(e);
}
function Fr(e) {
  return un.has(e);
}
class Br {
  constructor(t) {
    this.array = t;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { snapshot: r } = t, { path: o = [] } = n, i = [...o], s = r.getVForIndex(n.fid);
    return i.unshift(s), De(() => ({
      get: () => Re(
        this.array,
        i,
        r.getObjectToValue
      ),
      set: () => {
        throw new Error("Cannot set value to a constant array");
      }
    }));
  }
}
class Lr {
  constructor(t) {
    F(this, "_isDictSource");
    this.binding = t;
  }
  isDictSource(t) {
    if (this._isDictSource === void 0) {
      const n = q(t);
      this._isDictSource = n !== null && !Array.isArray(n);
    }
    return this._isDictSource;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { path: r = [] } = n, o = [...r], { snapshot: i } = t, s = i.getVueRefObject(this.binding), c = this.isDictSource(s), l = i.getVForIndex(n.fid), d = c && o.length === 0 ? [0] : [];
    return o.unshift(l, ...d), De(() => ({
      get: () => {
        const u = q(s), a = c ? Object.entries(u).map(([f, h], v) => [
          h,
          f,
          v
        ]) : u;
        try {
          return Re(
            q(a),
            o,
            i.getObjectToValue
          );
        } catch {
          return;
        }
      },
      set: (u) => {
        const a = q(s);
        if (c) {
          const f = Object.keys(a);
          if (l >= f.length)
            throw new Error("Cannot set value to a non-existent key");
          const h = f[l];
          et(
            a,
            [h],
            u,
            i.getObjectToValue
          );
          return;
        }
        et(
          a,
          o,
          u,
          i.getObjectToValue
        );
      }
    }));
  }
}
function Rt(e) {
  return e == null;
}
function Wr() {
  return dn().__VUE_DEVTOOLS_GLOBAL_HOOK__;
}
function dn() {
  return typeof navigator < "u" && typeof window < "u" ? window : typeof globalThis < "u" ? globalThis : {};
}
const Ur = typeof Proxy == "function", Gr = "devtools-plugin:setup", qr = "plugin:settings:set";
let le, ot;
function Hr() {
  var e;
  return le !== void 0 || (typeof window < "u" && window.performance ? (le = !0, ot = window.performance) : typeof globalThis < "u" && (!((e = globalThis.perf_hooks) === null || e === void 0) && e.performance) ? (le = !0, ot = globalThis.perf_hooks.performance) : le = !1), le;
}
function Kr() {
  return Hr() ? ot.now() : Date.now();
}
class zr {
  constructor(t, n) {
    this.target = null, this.targetQueue = [], this.onQueue = [], this.plugin = t, this.hook = n;
    const r = {};
    if (t.settings)
      for (const s in t.settings) {
        const c = t.settings[s];
        r[s] = c.defaultValue;
      }
    const o = `__vue-devtools-plugin-settings__${t.id}`;
    let i = Object.assign({}, r);
    try {
      const s = localStorage.getItem(o), c = JSON.parse(s);
      Object.assign(i, c);
    } catch {
    }
    this.fallbacks = {
      getSettings() {
        return i;
      },
      setSettings(s) {
        try {
          localStorage.setItem(o, JSON.stringify(s));
        } catch {
        }
        i = s;
      },
      now() {
        return Kr();
      }
    }, n && n.on(qr, (s, c) => {
      s === this.plugin.id && this.fallbacks.setSettings(c);
    }), this.proxiedOn = new Proxy({}, {
      get: (s, c) => this.target ? this.target.on[c] : (...l) => {
        this.onQueue.push({
          method: c,
          args: l
        });
      }
    }), this.proxiedTarget = new Proxy({}, {
      get: (s, c) => this.target ? this.target[c] : c === "on" ? this.proxiedOn : Object.keys(this.fallbacks).includes(c) ? (...l) => (this.targetQueue.push({
        method: c,
        args: l,
        resolve: () => {
        }
      }), this.fallbacks[c](...l)) : (...l) => new Promise((d) => {
        this.targetQueue.push({
          method: c,
          args: l,
          resolve: d
        });
      })
    });
  }
  async setRealTarget(t) {
    this.target = t;
    for (const n of this.onQueue)
      this.target.on[n.method](...n.args);
    for (const n of this.targetQueue)
      n.resolve(await this.target[n.method](...n.args));
  }
}
function Qr(e, t) {
  const n = e, r = dn(), o = Wr(), i = Ur && n.enableEarlyProxy;
  if (o && (r.__VUE_DEVTOOLS_PLUGIN_API_AVAILABLE__ || !i))
    o.emit(Gr, e, t);
  else {
    const s = i ? new zr(n, o) : null;
    (r.__VUE_DEVTOOLS_PLUGINS__ = r.__VUE_DEVTOOLS_PLUGINS__ || []).push({
      pluginDescriptor: n,
      setupFn: t,
      proxy: s
    }), s && t(s.proxiedTarget);
  }
}
var O = {};
const Q = typeof document < "u";
function hn(e) {
  return typeof e == "object" || "displayName" in e || "props" in e || "__vccOpts" in e;
}
function Jr(e) {
  return e.__esModule || e[Symbol.toStringTag] === "Module" || // support CF with dynamic imports that do not
  // add the Module string tag
  e.default && hn(e.default);
}
const I = Object.assign;
function Qe(e, t) {
  const n = {};
  for (const r in t) {
    const o = t[r];
    n[r] = U(o) ? o.map(e) : e(o);
  }
  return n;
}
const _e = () => {
}, U = Array.isArray;
function V(e) {
  const t = Array.from(arguments).slice(1);
  console.warn.apply(console, ["[Vue Router warn]: " + e].concat(t));
}
const pn = /#/g, Yr = /&/g, Xr = /\//g, Zr = /=/g, eo = /\?/g, mn = /\+/g, to = /%5B/g, no = /%5D/g, gn = /%5E/g, ro = /%60/g, vn = /%7B/g, oo = /%7C/g, yn = /%7D/g, so = /%20/g;
function gt(e) {
  return encodeURI("" + e).replace(oo, "|").replace(to, "[").replace(no, "]");
}
function io(e) {
  return gt(e).replace(vn, "{").replace(yn, "}").replace(gn, "^");
}
function st(e) {
  return gt(e).replace(mn, "%2B").replace(so, "+").replace(pn, "%23").replace(Yr, "%26").replace(ro, "`").replace(vn, "{").replace(yn, "}").replace(gn, "^");
}
function ao(e) {
  return st(e).replace(Zr, "%3D");
}
function co(e) {
  return gt(e).replace(pn, "%23").replace(eo, "%3F");
}
function uo(e) {
  return e == null ? "" : co(e).replace(Xr, "%2F");
}
function de(e) {
  try {
    return decodeURIComponent("" + e);
  } catch {
    O.NODE_ENV !== "production" && V(`Error decoding "${e}". Using original value`);
  }
  return "" + e;
}
const lo = /\/$/, fo = (e) => e.replace(lo, "");
function Je(e, t, n = "/") {
  let r, o = {}, i = "", s = "";
  const c = t.indexOf("#");
  let l = t.indexOf("?");
  return c < l && c >= 0 && (l = -1), l > -1 && (r = t.slice(0, l), i = t.slice(l + 1, c > -1 ? c : t.length), o = e(i)), c > -1 && (r = r || t.slice(0, c), s = t.slice(c, t.length)), r = mo(r ?? t, n), {
    fullPath: r + (i && "?") + i + s,
    path: r,
    query: o,
    hash: de(s)
  };
}
function ho(e, t) {
  const n = t.query ? e(t.query) : "";
  return t.path + (n && "?") + n + (t.hash || "");
}
function Vt(e, t) {
  return !t || !e.toLowerCase().startsWith(t.toLowerCase()) ? e : e.slice(t.length) || "/";
}
function Pt(e, t, n) {
  const r = t.matched.length - 1, o = n.matched.length - 1;
  return r > -1 && r === o && ee(t.matched[r], n.matched[o]) && wn(t.params, n.params) && e(t.query) === e(n.query) && t.hash === n.hash;
}
function ee(e, t) {
  return (e.aliasOf || e) === (t.aliasOf || t);
}
function wn(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length)
    return !1;
  for (const n in e)
    if (!po(e[n], t[n]))
      return !1;
  return !0;
}
function po(e, t) {
  return U(e) ? kt(e, t) : U(t) ? kt(t, e) : e === t;
}
function kt(e, t) {
  return U(t) ? e.length === t.length && e.every((n, r) => n === t[r]) : e.length === 1 && e[0] === t;
}
function mo(e, t) {
  if (e.startsWith("/"))
    return e;
  if (O.NODE_ENV !== "production" && !t.startsWith("/"))
    return V(`Cannot resolve a relative location without an absolute path. Trying to resolve "${e}" from "${t}". It should look like "/${t}".`), e;
  if (!e)
    return t;
  const n = t.split("/"), r = e.split("/"), o = r[r.length - 1];
  (o === ".." || o === ".") && r.push("");
  let i = n.length - 1, s, c;
  for (s = 0; s < r.length; s++)
    if (c = r[s], c !== ".")
      if (c === "..")
        i > 1 && i--;
      else
        break;
  return n.slice(0, i).join("/") + "/" + r.slice(s).join("/");
}
const J = {
  path: "/",
  // TODO: could we use a symbol in the future?
  name: void 0,
  params: {},
  query: {},
  hash: "",
  fullPath: "/",
  matched: [],
  meta: {},
  redirectedFrom: void 0
};
var he;
(function(e) {
  e.pop = "pop", e.push = "push";
})(he || (he = {}));
var oe;
(function(e) {
  e.back = "back", e.forward = "forward", e.unknown = "";
})(oe || (oe = {}));
const Ye = "";
function En(e) {
  if (!e)
    if (Q) {
      const t = document.querySelector("base");
      e = t && t.getAttribute("href") || "/", e = e.replace(/^\w+:\/\/[^\/]+/, "");
    } else
      e = "/";
  return e[0] !== "/" && e[0] !== "#" && (e = "/" + e), fo(e);
}
const go = /^[^#]+#/;
function _n(e, t) {
  return e.replace(go, "#") + t;
}
function vo(e, t) {
  const n = document.documentElement.getBoundingClientRect(), r = e.getBoundingClientRect();
  return {
    behavior: t.behavior,
    left: r.left - n.left - (t.left || 0),
    top: r.top - n.top - (t.top || 0)
  };
}
const We = () => ({
  left: window.scrollX,
  top: window.scrollY
});
function yo(e) {
  let t;
  if ("el" in e) {
    const n = e.el, r = typeof n == "string" && n.startsWith("#");
    if (O.NODE_ENV !== "production" && typeof e.el == "string" && (!r || !document.getElementById(e.el.slice(1))))
      try {
        const i = document.querySelector(e.el);
        if (r && i) {
          V(`The selector "${e.el}" should be passed as "el: document.querySelector('${e.el}')" because it starts with "#".`);
          return;
        }
      } catch {
        V(`The selector "${e.el}" is invalid. If you are using an id selector, make sure to escape it. You can find more information about escaping characters in selectors at https://mathiasbynens.be/notes/css-escapes or use CSS.escape (https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape).`);
        return;
      }
    const o = typeof n == "string" ? r ? document.getElementById(n.slice(1)) : document.querySelector(n) : n;
    if (!o) {
      O.NODE_ENV !== "production" && V(`Couldn't find element using selector "${e.el}" returned by scrollBehavior.`);
      return;
    }
    t = vo(o, e);
  } else
    t = e;
  "scrollBehavior" in document.documentElement.style ? window.scrollTo(t) : window.scrollTo(t.left != null ? t.left : window.scrollX, t.top != null ? t.top : window.scrollY);
}
function Nt(e, t) {
  return (history.state ? history.state.position - t : -1) + e;
}
const it = /* @__PURE__ */ new Map();
function wo(e, t) {
  it.set(e, t);
}
function Eo(e) {
  const t = it.get(e);
  return it.delete(e), t;
}
let _o = () => location.protocol + "//" + location.host;
function Sn(e, t) {
  const { pathname: n, search: r, hash: o } = t, i = e.indexOf("#");
  if (i > -1) {
    let c = o.includes(e.slice(i)) ? e.slice(i).length : 1, l = o.slice(c);
    return l[0] !== "/" && (l = "/" + l), Vt(l, "");
  }
  return Vt(n, e) + r + o;
}
function So(e, t, n, r) {
  let o = [], i = [], s = null;
  const c = ({ state: f }) => {
    const h = Sn(e, location), v = n.value, p = t.value;
    let g = 0;
    if (f) {
      if (n.value = h, t.value = f, s && s === v) {
        s = null;
        return;
      }
      g = p ? f.position - p.position : 0;
    } else
      r(h);
    o.forEach((y) => {
      y(n.value, v, {
        delta: g,
        type: he.pop,
        direction: g ? g > 0 ? oe.forward : oe.back : oe.unknown
      });
    });
  };
  function l() {
    s = n.value;
  }
  function d(f) {
    o.push(f);
    const h = () => {
      const v = o.indexOf(f);
      v > -1 && o.splice(v, 1);
    };
    return i.push(h), h;
  }
  function u() {
    const { history: f } = window;
    f.state && f.replaceState(I({}, f.state, { scroll: We() }), "");
  }
  function a() {
    for (const f of i)
      f();
    i = [], window.removeEventListener("popstate", c), window.removeEventListener("beforeunload", u);
  }
  return window.addEventListener("popstate", c), window.addEventListener("beforeunload", u, {
    passive: !0
  }), {
    pauseListeners: l,
    listen: d,
    destroy: a
  };
}
function It(e, t, n, r = !1, o = !1) {
  return {
    back: e,
    current: t,
    forward: n,
    replaced: r,
    position: window.history.length,
    scroll: o ? We() : null
  };
}
function bo(e) {
  const { history: t, location: n } = window, r = {
    value: Sn(e, n)
  }, o = { value: t.state };
  o.value || i(r.value, {
    back: null,
    current: r.value,
    forward: null,
    // the length is off by one, we need to decrease it
    position: t.length - 1,
    replaced: !0,
    // don't add a scroll as the user may have an anchor, and we want
    // scrollBehavior to be triggered without a saved position
    scroll: null
  }, !0);
  function i(l, d, u) {
    const a = e.indexOf("#"), f = a > -1 ? (n.host && document.querySelector("base") ? e : e.slice(a)) + l : _o() + e + l;
    try {
      t[u ? "replaceState" : "pushState"](d, "", f), o.value = d;
    } catch (h) {
      O.NODE_ENV !== "production" ? V("Error with push/replace State", h) : console.error(h), n[u ? "replace" : "assign"](f);
    }
  }
  function s(l, d) {
    const u = I({}, t.state, It(
      o.value.back,
      // keep back and forward entries but override current position
      l,
      o.value.forward,
      !0
    ), d, { position: o.value.position });
    i(l, u, !0), r.value = l;
  }
  function c(l, d) {
    const u = I(
      {},
      // use current history state to gracefully handle a wrong call to
      // history.replaceState
      // https://github.com/vuejs/router/issues/366
      o.value,
      t.state,
      {
        forward: l,
        scroll: We()
      }
    );
    O.NODE_ENV !== "production" && !t.state && V(`history.state seems to have been manually replaced without preserving the necessary values. Make sure to preserve existing history state if you are manually calling history.replaceState:

history.replaceState(history.state, '', url)

You can find more information at https://router.vuejs.org/guide/migration/#Usage-of-history-state`), i(u.current, u, !0);
    const a = I({}, It(r.value, l, null), { position: u.position + 1 }, d);
    i(l, a, !1), r.value = l;
  }
  return {
    location: r,
    state: o,
    push: c,
    replace: s
  };
}
function bn(e) {
  e = En(e);
  const t = bo(e), n = So(e, t.state, t.location, t.replace);
  function r(i, s = !0) {
    s || n.pauseListeners(), history.go(i);
  }
  const o = I({
    // it's overridden right after
    location: "",
    base: e,
    go: r,
    createHref: _n.bind(null, e)
  }, t, n);
  return Object.defineProperty(o, "location", {
    enumerable: !0,
    get: () => t.location.value
  }), Object.defineProperty(o, "state", {
    enumerable: !0,
    get: () => t.state.value
  }), o;
}
function Oo(e = "") {
  let t = [], n = [Ye], r = 0;
  e = En(e);
  function o(c) {
    r++, r !== n.length && n.splice(r), n.push(c);
  }
  function i(c, l, { direction: d, delta: u }) {
    const a = {
      direction: d,
      delta: u,
      type: he.pop
    };
    for (const f of t)
      f(c, l, a);
  }
  const s = {
    // rewritten by Object.defineProperty
    location: Ye,
    // TODO: should be kept in queue
    state: {},
    base: e,
    createHref: _n.bind(null, e),
    replace(c) {
      n.splice(r--, 1), o(c);
    },
    push(c, l) {
      o(c);
    },
    listen(c) {
      return t.push(c), () => {
        const l = t.indexOf(c);
        l > -1 && t.splice(l, 1);
      };
    },
    destroy() {
      t = [], n = [Ye], r = 0;
    },
    go(c, l = !0) {
      const d = this.location, u = (
        // we are considering delta === 0 going forward, but in abstract mode
        // using 0 for the delta doesn't make sense like it does in html5 where
        // it reloads the page
        c < 0 ? oe.back : oe.forward
      );
      r = Math.max(0, Math.min(r + c, n.length - 1)), l && i(this.location, d, {
        direction: u,
        delta: c
      });
    }
  };
  return Object.defineProperty(s, "location", {
    enumerable: !0,
    get: () => n[r]
  }), s;
}
function Ro(e) {
  return e = location.host ? e || location.pathname + location.search : "", e.includes("#") || (e += "#"), O.NODE_ENV !== "production" && !e.endsWith("#/") && !e.endsWith("#") && V(`A hash base must end with a "#":
"${e}" should be "${e.replace(/#.*$/, "#")}".`), bn(e);
}
function xe(e) {
  return typeof e == "string" || e && typeof e == "object";
}
function On(e) {
  return typeof e == "string" || typeof e == "symbol";
}
const at = Symbol(O.NODE_ENV !== "production" ? "navigation failure" : "");
var Tt;
(function(e) {
  e[e.aborted = 4] = "aborted", e[e.cancelled = 8] = "cancelled", e[e.duplicated = 16] = "duplicated";
})(Tt || (Tt = {}));
const Vo = {
  1({ location: e, currentLocation: t }) {
    return `No match for
 ${JSON.stringify(e)}${t ? `
while being at
` + JSON.stringify(t) : ""}`;
  },
  2({ from: e, to: t }) {
    return `Redirected from "${e.fullPath}" to "${ko(t)}" via a navigation guard.`;
  },
  4({ from: e, to: t }) {
    return `Navigation aborted from "${e.fullPath}" to "${t.fullPath}" via a navigation guard.`;
  },
  8({ from: e, to: t }) {
    return `Navigation cancelled from "${e.fullPath}" to "${t.fullPath}" with a new navigation.`;
  },
  16({ from: e, to: t }) {
    return `Avoided redundant navigation to current location: "${e.fullPath}".`;
  }
};
function pe(e, t) {
  return O.NODE_ENV !== "production" ? I(new Error(Vo[e](t)), {
    type: e,
    [at]: !0
  }, t) : I(new Error(), {
    type: e,
    [at]: !0
  }, t);
}
function z(e, t) {
  return e instanceof Error && at in e && (t == null || !!(e.type & t));
}
const Po = ["params", "query", "hash"];
function ko(e) {
  if (typeof e == "string")
    return e;
  if (e.path != null)
    return e.path;
  const t = {};
  for (const n of Po)
    n in e && (t[n] = e[n]);
  return JSON.stringify(t, null, 2);
}
const At = "[^/]+?", No = {
  sensitive: !1,
  strict: !1,
  start: !0,
  end: !0
}, Io = /[.+*?^${}()[\]/\\]/g;
function To(e, t) {
  const n = I({}, No, t), r = [];
  let o = n.start ? "^" : "";
  const i = [];
  for (const d of e) {
    const u = d.length ? [] : [
      90
      /* PathScore.Root */
    ];
    n.strict && !d.length && (o += "/");
    for (let a = 0; a < d.length; a++) {
      const f = d[a];
      let h = 40 + (n.sensitive ? 0.25 : 0);
      if (f.type === 0)
        a || (o += "/"), o += f.value.replace(Io, "\\$&"), h += 40;
      else if (f.type === 1) {
        const { value: v, repeatable: p, optional: g, regexp: y } = f;
        i.push({
          name: v,
          repeatable: p,
          optional: g
        });
        const _ = y || At;
        if (_ !== At) {
          h += 10;
          try {
            new RegExp(`(${_})`);
          } catch (R) {
            throw new Error(`Invalid custom RegExp for param "${v}" (${_}): ` + R.message);
          }
        }
        let b = p ? `((?:${_})(?:/(?:${_}))*)` : `(${_})`;
        a || (b = // avoid an optional / if there are more segments e.g. /:p?-static
        // or /:p?-:p2
        g && d.length < 2 ? `(?:/${b})` : "/" + b), g && (b += "?"), o += b, h += 20, g && (h += -8), p && (h += -20), _ === ".*" && (h += -50);
      }
      u.push(h);
    }
    r.push(u);
  }
  if (n.strict && n.end) {
    const d = r.length - 1;
    r[d][r[d].length - 1] += 0.7000000000000001;
  }
  n.strict || (o += "/?"), n.end ? o += "$" : n.strict && !o.endsWith("/") && (o += "(?:/|$)");
  const s = new RegExp(o, n.sensitive ? "" : "i");
  function c(d) {
    const u = d.match(s), a = {};
    if (!u)
      return null;
    for (let f = 1; f < u.length; f++) {
      const h = u[f] || "", v = i[f - 1];
      a[v.name] = h && v.repeatable ? h.split("/") : h;
    }
    return a;
  }
  function l(d) {
    let u = "", a = !1;
    for (const f of e) {
      (!a || !u.endsWith("/")) && (u += "/"), a = !1;
      for (const h of f)
        if (h.type === 0)
          u += h.value;
        else if (h.type === 1) {
          const { value: v, repeatable: p, optional: g } = h, y = v in d ? d[v] : "";
          if (U(y) && !p)
            throw new Error(`Provided param "${v}" is an array but it is not repeatable (* or + modifiers)`);
          const _ = U(y) ? y.join("/") : y;
          if (!_)
            if (g)
              f.length < 2 && (u.endsWith("/") ? u = u.slice(0, -1) : a = !0);
            else
              throw new Error(`Missing required param "${v}"`);
          u += _;
        }
    }
    return u || "/";
  }
  return {
    re: s,
    score: r,
    keys: i,
    parse: c,
    stringify: l
  };
}
function Ao(e, t) {
  let n = 0;
  for (; n < e.length && n < t.length; ) {
    const r = t[n] - e[n];
    if (r)
      return r;
    n++;
  }
  return e.length < t.length ? e.length === 1 && e[0] === 80 ? -1 : 1 : e.length > t.length ? t.length === 1 && t[0] === 80 ? 1 : -1 : 0;
}
function Rn(e, t) {
  let n = 0;
  const r = e.score, o = t.score;
  for (; n < r.length && n < o.length; ) {
    const i = Ao(r[n], o[n]);
    if (i)
      return i;
    n++;
  }
  if (Math.abs(o.length - r.length) === 1) {
    if (Ct(r))
      return 1;
    if (Ct(o))
      return -1;
  }
  return o.length - r.length;
}
function Ct(e) {
  const t = e[e.length - 1];
  return e.length > 0 && t[t.length - 1] < 0;
}
const Co = {
  type: 0,
  value: ""
}, $o = /[a-zA-Z0-9_]/;
function xo(e) {
  if (!e)
    return [[]];
  if (e === "/")
    return [[Co]];
  if (!e.startsWith("/"))
    throw new Error(O.NODE_ENV !== "production" ? `Route paths should start with a "/": "${e}" should be "/${e}".` : `Invalid path "${e}"`);
  function t(h) {
    throw new Error(`ERR (${n})/"${d}": ${h}`);
  }
  let n = 0, r = n;
  const o = [];
  let i;
  function s() {
    i && o.push(i), i = [];
  }
  let c = 0, l, d = "", u = "";
  function a() {
    d && (n === 0 ? i.push({
      type: 0,
      value: d
    }) : n === 1 || n === 2 || n === 3 ? (i.length > 1 && (l === "*" || l === "+") && t(`A repeatable param (${d}) must be alone in its segment. eg: '/:ids+.`), i.push({
      type: 1,
      value: d,
      regexp: u,
      repeatable: l === "*" || l === "+",
      optional: l === "*" || l === "?"
    })) : t("Invalid state to consume buffer"), d = "");
  }
  function f() {
    d += l;
  }
  for (; c < e.length; ) {
    if (l = e[c++], l === "\\" && n !== 2) {
      r = n, n = 4;
      continue;
    }
    switch (n) {
      case 0:
        l === "/" ? (d && a(), s()) : l === ":" ? (a(), n = 1) : f();
        break;
      case 4:
        f(), n = r;
        break;
      case 1:
        l === "(" ? n = 2 : $o.test(l) ? f() : (a(), n = 0, l !== "*" && l !== "?" && l !== "+" && c--);
        break;
      case 2:
        l === ")" ? u[u.length - 1] == "\\" ? u = u.slice(0, -1) + l : n = 3 : u += l;
        break;
      case 3:
        a(), n = 0, l !== "*" && l !== "?" && l !== "+" && c--, u = "";
        break;
      default:
        t("Unknown state");
        break;
    }
  }
  return n === 2 && t(`Unfinished custom RegExp for param "${d}"`), a(), s(), o;
}
function jo(e, t, n) {
  const r = To(xo(e.path), n);
  if (O.NODE_ENV !== "production") {
    const i = /* @__PURE__ */ new Set();
    for (const s of r.keys)
      i.has(s.name) && V(`Found duplicated params with name "${s.name}" for path "${e.path}". Only the last one will be available on "$route.params".`), i.add(s.name);
  }
  const o = I(r, {
    record: e,
    parent: t,
    // these needs to be populated by the parent
    children: [],
    alias: []
  });
  return t && !o.record.aliasOf == !t.record.aliasOf && t.children.push(o), o;
}
function Do(e, t) {
  const n = [], r = /* @__PURE__ */ new Map();
  t = Dt({ strict: !1, end: !0, sensitive: !1 }, t);
  function o(a) {
    return r.get(a);
  }
  function i(a, f, h) {
    const v = !h, p = xt(a);
    O.NODE_ENV !== "production" && Lo(p, f), p.aliasOf = h && h.record;
    const g = Dt(t, a), y = [p];
    if ("alias" in a) {
      const R = typeof a.alias == "string" ? [a.alias] : a.alias;
      for (const $ of R)
        y.push(
          // we need to normalize again to ensure the `mods` property
          // being non enumerable
          xt(I({}, p, {
            // this allows us to hold a copy of the `components` option
            // so that async components cache is hold on the original record
            components: h ? h.record.components : p.components,
            path: $,
            // we might be the child of an alias
            aliasOf: h ? h.record : p
            // the aliases are always of the same kind as the original since they
            // are defined on the same record
          }))
        );
    }
    let _, b;
    for (const R of y) {
      const { path: $ } = R;
      if (f && $[0] !== "/") {
        const G = f.record.path, x = G[G.length - 1] === "/" ? "" : "/";
        R.path = f.record.path + ($ && x + $);
      }
      if (O.NODE_ENV !== "production" && R.path === "*")
        throw new Error(`Catch all routes ("*") must now be defined using a param with a custom regexp.
See more at https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes.`);
      if (_ = jo(R, f, g), O.NODE_ENV !== "production" && f && $[0] === "/" && Uo(_, f), h ? (h.alias.push(_), O.NODE_ENV !== "production" && Bo(h, _)) : (b = b || _, b !== _ && b.alias.push(_), v && a.name && !jt(_) && (O.NODE_ENV !== "production" && Wo(a, f), s(a.name))), Vn(_) && l(_), p.children) {
        const G = p.children;
        for (let x = 0; x < G.length; x++)
          i(G[x], _, h && h.children[x]);
      }
      h = h || _;
    }
    return b ? () => {
      s(b);
    } : _e;
  }
  function s(a) {
    if (On(a)) {
      const f = r.get(a);
      f && (r.delete(a), n.splice(n.indexOf(f), 1), f.children.forEach(s), f.alias.forEach(s));
    } else {
      const f = n.indexOf(a);
      f > -1 && (n.splice(f, 1), a.record.name && r.delete(a.record.name), a.children.forEach(s), a.alias.forEach(s));
    }
  }
  function c() {
    return n;
  }
  function l(a) {
    const f = Go(a, n);
    n.splice(f, 0, a), a.record.name && !jt(a) && r.set(a.record.name, a);
  }
  function d(a, f) {
    let h, v = {}, p, g;
    if ("name" in a && a.name) {
      if (h = r.get(a.name), !h)
        throw pe(1, {
          location: a
        });
      if (O.NODE_ENV !== "production") {
        const b = Object.keys(a.params || {}).filter((R) => !h.keys.find(($) => $.name === R));
        b.length && V(`Discarded invalid param(s) "${b.join('", "')}" when navigating. See https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md#414-2022-08-22 for more details.`);
      }
      g = h.record.name, v = I(
        // paramsFromLocation is a new object
        $t(
          f.params,
          // only keep params that exist in the resolved location
          // only keep optional params coming from a parent record
          h.keys.filter((b) => !b.optional).concat(h.parent ? h.parent.keys.filter((b) => b.optional) : []).map((b) => b.name)
        ),
        // discard any existing params in the current location that do not exist here
        // #1497 this ensures better active/exact matching
        a.params && $t(a.params, h.keys.map((b) => b.name))
      ), p = h.stringify(v);
    } else if (a.path != null)
      p = a.path, O.NODE_ENV !== "production" && !p.startsWith("/") && V(`The Matcher cannot resolve relative paths but received "${p}". Unless you directly called \`matcher.resolve("${p}")\`, this is probably a bug in vue-router. Please open an issue at https://github.com/vuejs/router/issues/new/choose.`), h = n.find((b) => b.re.test(p)), h && (v = h.parse(p), g = h.record.name);
    else {
      if (h = f.name ? r.get(f.name) : n.find((b) => b.re.test(f.path)), !h)
        throw pe(1, {
          location: a,
          currentLocation: f
        });
      g = h.record.name, v = I({}, f.params, a.params), p = h.stringify(v);
    }
    const y = [];
    let _ = h;
    for (; _; )
      y.unshift(_.record), _ = _.parent;
    return {
      name: g,
      path: p,
      params: v,
      matched: y,
      meta: Fo(y)
    };
  }
  e.forEach((a) => i(a));
  function u() {
    n.length = 0, r.clear();
  }
  return {
    addRoute: i,
    resolve: d,
    removeRoute: s,
    clearRoutes: u,
    getRoutes: c,
    getRecordMatcher: o
  };
}
function $t(e, t) {
  const n = {};
  for (const r of t)
    r in e && (n[r] = e[r]);
  return n;
}
function xt(e) {
  const t = {
    path: e.path,
    redirect: e.redirect,
    name: e.name,
    meta: e.meta || {},
    aliasOf: e.aliasOf,
    beforeEnter: e.beforeEnter,
    props: Mo(e),
    children: e.children || [],
    instances: {},
    leaveGuards: /* @__PURE__ */ new Set(),
    updateGuards: /* @__PURE__ */ new Set(),
    enterCallbacks: {},
    // must be declared afterwards
    // mods: {},
    components: "components" in e ? e.components || null : e.component && { default: e.component }
  };
  return Object.defineProperty(t, "mods", {
    value: {}
  }), t;
}
function Mo(e) {
  const t = {}, n = e.props || !1;
  if ("component" in e)
    t.default = n;
  else
    for (const r in e.components)
      t[r] = typeof n == "object" ? n[r] : n;
  return t;
}
function jt(e) {
  for (; e; ) {
    if (e.record.aliasOf)
      return !0;
    e = e.parent;
  }
  return !1;
}
function Fo(e) {
  return e.reduce((t, n) => I(t, n.meta), {});
}
function Dt(e, t) {
  const n = {};
  for (const r in e)
    n[r] = r in t ? t[r] : e[r];
  return n;
}
function ct(e, t) {
  return e.name === t.name && e.optional === t.optional && e.repeatable === t.repeatable;
}
function Bo(e, t) {
  for (const n of e.keys)
    if (!n.optional && !t.keys.find(ct.bind(null, n)))
      return V(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
  for (const n of t.keys)
    if (!n.optional && !e.keys.find(ct.bind(null, n)))
      return V(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
}
function Lo(e, t) {
  t && t.record.name && !e.name && !e.path && V(`The route named "${String(t.record.name)}" has a child without a name and an empty path. Using that name won't render the empty path child so you probably want to move the name to the child instead. If this is intentional, add a name to the child route to remove the warning.`);
}
function Wo(e, t) {
  for (let n = t; n; n = n.parent)
    if (n.record.name === e.name)
      throw new Error(`A route named "${String(e.name)}" has been added as a ${t === n ? "child" : "descendant"} of a route with the same name. Route names must be unique and a nested route cannot use the same name as an ancestor.`);
}
function Uo(e, t) {
  for (const n of t.keys)
    if (!e.keys.find(ct.bind(null, n)))
      return V(`Absolute path "${e.record.path}" must have the exact same param named "${n.name}" as its parent "${t.record.path}".`);
}
function Go(e, t) {
  let n = 0, r = t.length;
  for (; n !== r; ) {
    const i = n + r >> 1;
    Rn(e, t[i]) < 0 ? r = i : n = i + 1;
  }
  const o = qo(e);
  return o && (r = t.lastIndexOf(o, r - 1), O.NODE_ENV !== "production" && r < 0 && V(`Finding ancestor route "${o.record.path}" failed for "${e.record.path}"`)), r;
}
function qo(e) {
  let t = e;
  for (; t = t.parent; )
    if (Vn(t) && Rn(e, t) === 0)
      return t;
}
function Vn({ record: e }) {
  return !!(e.name || e.components && Object.keys(e.components).length || e.redirect);
}
function Ho(e) {
  const t = {};
  if (e === "" || e === "?")
    return t;
  const r = (e[0] === "?" ? e.slice(1) : e).split("&");
  for (let o = 0; o < r.length; ++o) {
    const i = r[o].replace(mn, " "), s = i.indexOf("="), c = de(s < 0 ? i : i.slice(0, s)), l = s < 0 ? null : de(i.slice(s + 1));
    if (c in t) {
      let d = t[c];
      U(d) || (d = t[c] = [d]), d.push(l);
    } else
      t[c] = l;
  }
  return t;
}
function Mt(e) {
  let t = "";
  for (let n in e) {
    const r = e[n];
    if (n = ao(n), r == null) {
      r !== void 0 && (t += (t.length ? "&" : "") + n);
      continue;
    }
    (U(r) ? r.map((i) => i && st(i)) : [r && st(r)]).forEach((i) => {
      i !== void 0 && (t += (t.length ? "&" : "") + n, i != null && (t += "=" + i));
    });
  }
  return t;
}
function Ko(e) {
  const t = {};
  for (const n in e) {
    const r = e[n];
    r !== void 0 && (t[n] = U(r) ? r.map((o) => o == null ? null : "" + o) : r == null ? r : "" + r);
  }
  return t;
}
const zo = Symbol(O.NODE_ENV !== "production" ? "router view location matched" : ""), Ft = Symbol(O.NODE_ENV !== "production" ? "router view depth" : ""), Ue = Symbol(O.NODE_ENV !== "production" ? "router" : ""), vt = Symbol(O.NODE_ENV !== "production" ? "route location" : ""), ut = Symbol(O.NODE_ENV !== "production" ? "router view location" : "");
function ye() {
  let e = [];
  function t(r) {
    return e.push(r), () => {
      const o = e.indexOf(r);
      o > -1 && e.splice(o, 1);
    };
  }
  function n() {
    e = [];
  }
  return {
    add: t,
    list: () => e.slice(),
    reset: n
  };
}
function Y(e, t, n, r, o, i = (s) => s()) {
  const s = r && // name is defined if record is because of the function overload
  (r.enterCallbacks[o] = r.enterCallbacks[o] || []);
  return () => new Promise((c, l) => {
    const d = (f) => {
      f === !1 ? l(pe(4, {
        from: n,
        to: t
      })) : f instanceof Error ? l(f) : xe(f) ? l(pe(2, {
        from: t,
        to: f
      })) : (s && // since enterCallbackArray is truthy, both record and name also are
      r.enterCallbacks[o] === s && typeof f == "function" && s.push(f), c());
    }, u = i(() => e.call(r && r.instances[o], t, n, O.NODE_ENV !== "production" ? Qo(d, t, n) : d));
    let a = Promise.resolve(u);
    if (e.length < 3 && (a = a.then(d)), O.NODE_ENV !== "production" && e.length > 2) {
      const f = `The "next" callback was never called inside of ${e.name ? '"' + e.name + '"' : ""}:
${e.toString()}
. If you are returning a value instead of calling "next", make sure to remove the "next" parameter from your function.`;
      if (typeof u == "object" && "then" in u)
        a = a.then((h) => d._called ? h : (V(f), Promise.reject(new Error("Invalid navigation guard"))));
      else if (u !== void 0 && !d._called) {
        V(f), l(new Error("Invalid navigation guard"));
        return;
      }
    }
    a.catch((f) => l(f));
  });
}
function Qo(e, t, n) {
  let r = 0;
  return function() {
    r++ === 1 && V(`The "next" callback was called more than once in one navigation guard when going from "${n.fullPath}" to "${t.fullPath}". It should be called exactly one time in each navigation guard. This will fail in production.`), e._called = !0, r === 1 && e.apply(null, arguments);
  };
}
function Xe(e, t, n, r, o = (i) => i()) {
  const i = [];
  for (const s of e) {
    O.NODE_ENV !== "production" && !s.components && !s.children.length && V(`Record with path "${s.path}" is either missing a "component(s)" or "children" property.`);
    for (const c in s.components) {
      let l = s.components[c];
      if (O.NODE_ENV !== "production") {
        if (!l || typeof l != "object" && typeof l != "function")
          throw V(`Component "${c}" in record with path "${s.path}" is not a valid component. Received "${String(l)}".`), new Error("Invalid route component");
        if ("then" in l) {
          V(`Component "${c}" in record with path "${s.path}" is a Promise instead of a function that returns a Promise. Did you write "import('./MyPage.vue')" instead of "() => import('./MyPage.vue')" ? This will break in production if not fixed.`);
          const d = l;
          l = () => d;
        } else l.__asyncLoader && // warn only once per component
        !l.__warnedDefineAsync && (l.__warnedDefineAsync = !0, V(`Component "${c}" in record with path "${s.path}" is defined using "defineAsyncComponent()". Write "() => import('./MyPage.vue')" instead of "defineAsyncComponent(() => import('./MyPage.vue'))".`));
      }
      if (!(t !== "beforeRouteEnter" && !s.instances[c]))
        if (hn(l)) {
          const u = (l.__vccOpts || l)[t];
          u && i.push(Y(u, n, r, s, c, o));
        } else {
          let d = l();
          O.NODE_ENV !== "production" && !("catch" in d) && (V(`Component "${c}" in record with path "${s.path}" is a function that does not return a Promise. If you were passing a functional component, make sure to add a "displayName" to the component. This will break in production if not fixed.`), d = Promise.resolve(d)), i.push(() => d.then((u) => {
            if (!u)
              throw new Error(`Couldn't resolve component "${c}" at "${s.path}"`);
            const a = Jr(u) ? u.default : u;
            s.mods[c] = u, s.components[c] = a;
            const h = (a.__vccOpts || a)[t];
            return h && Y(h, n, r, s, c, o)();
          }));
        }
    }
  }
  return i;
}
function Bt(e) {
  const t = Z(Ue), n = Z(vt);
  let r = !1, o = null;
  const i = W(() => {
    const u = D(e.to);
    return O.NODE_ENV !== "production" && (!r || u !== o) && (xe(u) || (r ? V(`Invalid value for prop "to" in useLink()
- to:`, u, `
- previous to:`, o, `
- props:`, e) : V(`Invalid value for prop "to" in useLink()
- to:`, u, `
- props:`, e)), o = u, r = !0), t.resolve(u);
  }), s = W(() => {
    const { matched: u } = i.value, { length: a } = u, f = u[a - 1], h = n.matched;
    if (!f || !h.length)
      return -1;
    const v = h.findIndex(ee.bind(null, f));
    if (v > -1)
      return v;
    const p = Lt(u[a - 2]);
    return (
      // we are dealing with nested routes
      a > 1 && // if the parent and matched route have the same path, this link is
      // referring to the empty child. Or we currently are on a different
      // child of the same parent
      Lt(f) === p && // avoid comparing the child with its parent
      h[h.length - 1].path !== p ? h.findIndex(ee.bind(null, u[a - 2])) : v
    );
  }), c = W(() => s.value > -1 && es(n.params, i.value.params)), l = W(() => s.value > -1 && s.value === n.matched.length - 1 && wn(n.params, i.value.params));
  function d(u = {}) {
    if (Zo(u)) {
      const a = t[D(e.replace) ? "replace" : "push"](
        D(e.to)
        // avoid uncaught errors are they are logged anyway
      ).catch(_e);
      return e.viewTransition && typeof document < "u" && "startViewTransition" in document && document.startViewTransition(() => a), a;
    }
    return Promise.resolve();
  }
  if (O.NODE_ENV !== "production" && Q) {
    const u = Jt();
    if (u) {
      const a = {
        route: i.value,
        isActive: c.value,
        isExactActive: l.value,
        error: null
      };
      u.__vrl_devtools = u.__vrl_devtools || [], u.__vrl_devtools.push(a), Qt(() => {
        a.route = i.value, a.isActive = c.value, a.isExactActive = l.value, a.error = xe(D(e.to)) ? null : 'Invalid "to" value';
      }, { flush: "post" });
    }
  }
  return {
    route: i,
    href: W(() => i.value.href),
    isActive: c,
    isExactActive: l,
    navigate: d
  };
}
function Jo(e) {
  return e.length === 1 ? e[0] : e;
}
const Yo = /* @__PURE__ */ L({
  name: "RouterLink",
  compatConfig: { MODE: 3 },
  props: {
    to: {
      type: [String, Object],
      required: !0
    },
    replace: Boolean,
    activeClass: String,
    // inactiveClass: String,
    exactActiveClass: String,
    custom: Boolean,
    ariaCurrentValue: {
      type: String,
      default: "page"
    }
  },
  useLink: Bt,
  setup(e, { slots: t }) {
    const n = Kn(Bt(e)), { options: r } = Z(Ue), o = W(() => ({
      [Wt(e.activeClass, r.linkActiveClass, "router-link-active")]: n.isActive,
      // [getLinkClass(
      //   props.inactiveClass,
      //   options.linkInactiveClass,
      //   'router-link-inactive'
      // )]: !link.isExactActive,
      [Wt(e.exactActiveClass, r.linkExactActiveClass, "router-link-exact-active")]: n.isExactActive
    }));
    return () => {
      const i = t.default && Jo(t.default(n));
      return e.custom ? i : A("a", {
        "aria-current": n.isExactActive ? e.ariaCurrentValue : null,
        href: n.href,
        // this would override user added attrs but Vue will still add
        // the listener, so we end up triggering both
        onClick: n.navigate,
        class: o.value
      }, i);
    };
  }
}), Xo = Yo;
function Zo(e) {
  if (!(e.metaKey || e.altKey || e.ctrlKey || e.shiftKey) && !e.defaultPrevented && !(e.button !== void 0 && e.button !== 0)) {
    if (e.currentTarget && e.currentTarget.getAttribute) {
      const t = e.currentTarget.getAttribute("target");
      if (/\b_blank\b/i.test(t))
        return;
    }
    return e.preventDefault && e.preventDefault(), !0;
  }
}
function es(e, t) {
  for (const n in t) {
    const r = t[n], o = e[n];
    if (typeof r == "string") {
      if (r !== o)
        return !1;
    } else if (!U(o) || o.length !== r.length || r.some((i, s) => i !== o[s]))
      return !1;
  }
  return !0;
}
function Lt(e) {
  return e ? e.aliasOf ? e.aliasOf.path : e.path : "";
}
const Wt = (e, t, n) => e ?? t ?? n, ts = /* @__PURE__ */ L({
  name: "RouterView",
  // #674 we manually inherit them
  inheritAttrs: !1,
  props: {
    name: {
      type: String,
      default: "default"
    },
    route: Object
  },
  // Better compat for @vue/compat users
  // https://github.com/vuejs/router/issues/1315
  compatConfig: { MODE: 3 },
  setup(e, { attrs: t, slots: n }) {
    O.NODE_ENV !== "production" && rs();
    const r = Z(ut), o = W(() => e.route || r.value), i = Z(Ft, 0), s = W(() => {
      let d = D(i);
      const { matched: u } = o.value;
      let a;
      for (; (a = u[d]) && !a.components; )
        d++;
      return d;
    }), c = W(() => o.value.matched[s.value]);
    Te(Ft, W(() => s.value + 1)), Te(zo, c), Te(ut, o);
    const l = H();
    return K(() => [l.value, c.value, e.name], ([d, u, a], [f, h, v]) => {
      u && (u.instances[a] = d, h && h !== u && d && d === f && (u.leaveGuards.size || (u.leaveGuards = h.leaveGuards), u.updateGuards.size || (u.updateGuards = h.updateGuards))), d && u && // if there is no instance but to and from are the same this might be
      // the first visit
      (!h || !ee(u, h) || !f) && (u.enterCallbacks[a] || []).forEach((p) => p(d));
    }, { flush: "post" }), () => {
      const d = o.value, u = e.name, a = c.value, f = a && a.components[u];
      if (!f)
        return Ut(n.default, { Component: f, route: d });
      const h = a.props[u], v = h ? h === !0 ? d.params : typeof h == "function" ? h(d) : h : null, g = A(f, I({}, v, t, {
        onVnodeUnmounted: (y) => {
          y.component.isUnmounted && (a.instances[u] = null);
        },
        ref: l
      }));
      if (O.NODE_ENV !== "production" && Q && g.ref) {
        const y = {
          depth: s.value,
          name: a.name,
          path: a.path,
          meta: a.meta
        };
        (U(g.ref) ? g.ref.map((b) => b.i) : [g.ref.i]).forEach((b) => {
          b.__vrv_devtools = y;
        });
      }
      return (
        // pass the vnode to the slot as a prop.
        // h and <component :is="..."> both accept vnodes
        Ut(n.default, { Component: g, route: d }) || g
      );
    };
  }
});
function Ut(e, t) {
  if (!e)
    return null;
  const n = e(t);
  return n.length === 1 ? n[0] : n;
}
const ns = ts;
function rs() {
  const e = Jt(), t = e.parent && e.parent.type.name, n = e.parent && e.parent.subTree && e.parent.subTree.type;
  if (t && (t === "KeepAlive" || t.includes("Transition")) && typeof n == "object" && n.name === "RouterView") {
    const r = t === "KeepAlive" ? "keep-alive" : "transition";
    V(`<router-view> can no longer be used directly inside <transition> or <keep-alive>.
Use slot props instead:

<router-view v-slot="{ Component }">
  <${r}>
    <component :is="Component" />
  </${r}>
</router-view>`);
  }
}
function we(e, t) {
  const n = I({}, e, {
    // remove variables that can contain vue instances
    matched: e.matched.map((r) => ps(r, ["instances", "children", "aliasOf"]))
  });
  return {
    _custom: {
      type: null,
      readOnly: !0,
      display: e.fullPath,
      tooltip: t,
      value: n
    }
  };
}
function Ie(e) {
  return {
    _custom: {
      display: e
    }
  };
}
let os = 0;
function ss(e, t, n) {
  if (t.__hasDevtools)
    return;
  t.__hasDevtools = !0;
  const r = os++;
  Qr({
    id: "org.vuejs.router" + (r ? "." + r : ""),
    label: "Vue Router",
    packageName: "vue-router",
    homepage: "https://router.vuejs.org",
    logo: "https://router.vuejs.org/logo.png",
    componentStateTypes: ["Routing"],
    app: e
  }, (o) => {
    typeof o.now != "function" && console.warn("[Vue Router]: You seem to be using an outdated version of Vue Devtools. Are you still using the Beta release instead of the stable one? You can find the links at https://devtools.vuejs.org/guide/installation.html."), o.on.inspectComponent((u, a) => {
      u.instanceData && u.instanceData.state.push({
        type: "Routing",
        key: "$route",
        editable: !1,
        value: we(t.currentRoute.value, "Current Route")
      });
    }), o.on.visitComponentTree(({ treeNode: u, componentInstance: a }) => {
      if (a.__vrv_devtools) {
        const f = a.__vrv_devtools;
        u.tags.push({
          label: (f.name ? `${f.name.toString()}: ` : "") + f.path,
          textColor: 0,
          tooltip: "This component is rendered by &lt;router-view&gt;",
          backgroundColor: Pn
        });
      }
      U(a.__vrl_devtools) && (a.__devtoolsApi = o, a.__vrl_devtools.forEach((f) => {
        let h = f.route.path, v = In, p = "", g = 0;
        f.error ? (h = f.error, v = ls, g = fs) : f.isExactActive ? (v = Nn, p = "This is exactly active") : f.isActive && (v = kn, p = "This link is active"), u.tags.push({
          label: h,
          textColor: g,
          tooltip: p,
          backgroundColor: v
        });
      }));
    }), K(t.currentRoute, () => {
      l(), o.notifyComponentUpdate(), o.sendInspectorTree(c), o.sendInspectorState(c);
    });
    const i = "router:navigations:" + r;
    o.addTimelineLayer({
      id: i,
      label: `Router${r ? " " + r : ""} Navigations`,
      color: 4237508
    }), t.onError((u, a) => {
      o.addTimelineEvent({
        layerId: i,
        event: {
          title: "Error during Navigation",
          subtitle: a.fullPath,
          logType: "error",
          time: o.now(),
          data: { error: u },
          groupId: a.meta.__navigationId
        }
      });
    });
    let s = 0;
    t.beforeEach((u, a) => {
      const f = {
        guard: Ie("beforeEach"),
        from: we(a, "Current Location during this navigation"),
        to: we(u, "Target location")
      };
      Object.defineProperty(u.meta, "__navigationId", {
        value: s++
      }), o.addTimelineEvent({
        layerId: i,
        event: {
          time: o.now(),
          title: "Start of navigation",
          subtitle: u.fullPath,
          data: f,
          groupId: u.meta.__navigationId
        }
      });
    }), t.afterEach((u, a, f) => {
      const h = {
        guard: Ie("afterEach")
      };
      f ? (h.failure = {
        _custom: {
          type: Error,
          readOnly: !0,
          display: f ? f.message : "",
          tooltip: "Navigation Failure",
          value: f
        }
      }, h.status = Ie("❌")) : h.status = Ie("✅"), h.from = we(a, "Current Location during this navigation"), h.to = we(u, "Target location"), o.addTimelineEvent({
        layerId: i,
        event: {
          title: "End of navigation",
          subtitle: u.fullPath,
          time: o.now(),
          data: h,
          logType: f ? "warning" : "default",
          groupId: u.meta.__navigationId
        }
      });
    });
    const c = "router-inspector:" + r;
    o.addInspector({
      id: c,
      label: "Routes" + (r ? " " + r : ""),
      icon: "book",
      treeFilterPlaceholder: "Search routes"
    });
    function l() {
      if (!d)
        return;
      const u = d;
      let a = n.getRoutes().filter((f) => !f.parent || // these routes have a parent with no component which will not appear in the view
      // therefore we still need to include them
      !f.parent.record.components);
      a.forEach(Cn), u.filter && (a = a.filter((f) => (
        // save matches state based on the payload
        lt(f, u.filter.toLowerCase())
      ))), a.forEach((f) => An(f, t.currentRoute.value)), u.rootNodes = a.map(Tn);
    }
    let d;
    o.on.getInspectorTree((u) => {
      d = u, u.app === e && u.inspectorId === c && l();
    }), o.on.getInspectorState((u) => {
      if (u.app === e && u.inspectorId === c) {
        const f = n.getRoutes().find((h) => h.record.__vd_id === u.nodeId);
        f && (u.state = {
          options: as(f)
        });
      }
    }), o.sendInspectorTree(c), o.sendInspectorState(c);
  });
}
function is(e) {
  return e.optional ? e.repeatable ? "*" : "?" : e.repeatable ? "+" : "";
}
function as(e) {
  const { record: t } = e, n = [
    { editable: !1, key: "path", value: t.path }
  ];
  return t.name != null && n.push({
    editable: !1,
    key: "name",
    value: t.name
  }), n.push({ editable: !1, key: "regexp", value: e.re }), e.keys.length && n.push({
    editable: !1,
    key: "keys",
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.keys.map((r) => `${r.name}${is(r)}`).join(" "),
        tooltip: "Param keys",
        value: e.keys
      }
    }
  }), t.redirect != null && n.push({
    editable: !1,
    key: "redirect",
    value: t.redirect
  }), e.alias.length && n.push({
    editable: !1,
    key: "aliases",
    value: e.alias.map((r) => r.record.path)
  }), Object.keys(e.record.meta).length && n.push({
    editable: !1,
    key: "meta",
    value: e.record.meta
  }), n.push({
    key: "score",
    editable: !1,
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.score.map((r) => r.join(", ")).join(" | "),
        tooltip: "Score used to sort routes",
        value: e.score
      }
    }
  }), n;
}
const Pn = 15485081, kn = 2450411, Nn = 8702998, cs = 2282478, In = 16486972, us = 6710886, ls = 16704226, fs = 12131356;
function Tn(e) {
  const t = [], { record: n } = e;
  n.name != null && t.push({
    label: String(n.name),
    textColor: 0,
    backgroundColor: cs
  }), n.aliasOf && t.push({
    label: "alias",
    textColor: 0,
    backgroundColor: In
  }), e.__vd_match && t.push({
    label: "matches",
    textColor: 0,
    backgroundColor: Pn
  }), e.__vd_exactActive && t.push({
    label: "exact",
    textColor: 0,
    backgroundColor: Nn
  }), e.__vd_active && t.push({
    label: "active",
    textColor: 0,
    backgroundColor: kn
  }), n.redirect && t.push({
    label: typeof n.redirect == "string" ? `redirect: ${n.redirect}` : "redirects",
    textColor: 16777215,
    backgroundColor: us
  });
  let r = n.__vd_id;
  return r == null && (r = String(ds++), n.__vd_id = r), {
    id: r,
    label: n.path,
    tags: t,
    children: e.children.map(Tn)
  };
}
let ds = 0;
const hs = /^\/(.*)\/([a-z]*)$/;
function An(e, t) {
  const n = t.matched.length && ee(t.matched[t.matched.length - 1], e.record);
  e.__vd_exactActive = e.__vd_active = n, n || (e.__vd_active = t.matched.some((r) => ee(r, e.record))), e.children.forEach((r) => An(r, t));
}
function Cn(e) {
  e.__vd_match = !1, e.children.forEach(Cn);
}
function lt(e, t) {
  const n = String(e.re).match(hs);
  if (e.__vd_match = !1, !n || n.length < 3)
    return !1;
  if (new RegExp(n[1].replace(/\$$/, ""), n[2]).test(t))
    return e.children.forEach((s) => lt(s, t)), e.record.path !== "/" || t === "/" ? (e.__vd_match = e.re.test(t), !0) : !1;
  const o = e.record.path.toLowerCase(), i = de(o);
  return !t.startsWith("/") && (i.includes(t) || o.includes(t)) || i.startsWith(t) || o.startsWith(t) || e.record.name && String(e.record.name).includes(t) ? !0 : e.children.some((s) => lt(s, t));
}
function ps(e, t) {
  const n = {};
  for (const r in e)
    t.includes(r) || (n[r] = e[r]);
  return n;
}
function ms(e) {
  const t = Do(e.routes, e), n = e.parseQuery || Ho, r = e.stringifyQuery || Mt, o = e.history;
  if (O.NODE_ENV !== "production" && !o)
    throw new Error('Provide the "history" option when calling "createRouter()": https://router.vuejs.org/api/interfaces/RouterOptions.html#history');
  const i = ye(), s = ye(), c = ye(), l = X(J);
  let d = J;
  Q && e.scrollBehavior && "scrollRestoration" in history && (history.scrollRestoration = "manual");
  const u = Qe.bind(null, (m) => "" + m), a = Qe.bind(null, uo), f = (
    // @ts-expect-error: intentionally avoid the type check
    Qe.bind(null, de)
  );
  function h(m, E) {
    let w, S;
    return On(m) ? (w = t.getRecordMatcher(m), O.NODE_ENV !== "production" && !w && V(`Parent route "${String(m)}" not found when adding child route`, E), S = E) : S = m, t.addRoute(S, w);
  }
  function v(m) {
    const E = t.getRecordMatcher(m);
    E ? t.removeRoute(E) : O.NODE_ENV !== "production" && V(`Cannot remove non-existent route "${String(m)}"`);
  }
  function p() {
    return t.getRoutes().map((m) => m.record);
  }
  function g(m) {
    return !!t.getRecordMatcher(m);
  }
  function y(m, E) {
    if (E = I({}, E || l.value), typeof m == "string") {
      const P = Je(n, m, E.path), C = t.resolve({ path: P.path }, E), ne = o.createHref(P.fullPath);
      return O.NODE_ENV !== "production" && (ne.startsWith("//") ? V(`Location "${m}" resolved to "${ne}". A resolved location cannot start with multiple slashes.`) : C.matched.length || V(`No match found for location with path "${m}"`)), I(P, C, {
        params: f(C.params),
        hash: de(P.hash),
        redirectedFrom: void 0,
        href: ne
      });
    }
    if (O.NODE_ENV !== "production" && !xe(m))
      return V(`router.resolve() was passed an invalid location. This will fail in production.
- Location:`, m), y({});
    let w;
    if (m.path != null)
      O.NODE_ENV !== "production" && "params" in m && !("name" in m) && // @ts-expect-error: the type is never
      Object.keys(m.params).length && V(`Path "${m.path}" was passed with params but they will be ignored. Use a named route alongside params instead.`), w = I({}, m, {
        path: Je(n, m.path, E.path).path
      });
    else {
      const P = I({}, m.params);
      for (const C in P)
        P[C] == null && delete P[C];
      w = I({}, m, {
        params: a(P)
      }), E.params = a(E.params);
    }
    const S = t.resolve(w, E), T = m.hash || "";
    O.NODE_ENV !== "production" && T && !T.startsWith("#") && V(`A \`hash\` should always start with the character "#". Replace "${T}" with "#${T}".`), S.params = u(f(S.params));
    const j = ho(r, I({}, m, {
      hash: io(T),
      path: S.path
    })), k = o.createHref(j);
    return O.NODE_ENV !== "production" && (k.startsWith("//") ? V(`Location "${m}" resolved to "${k}". A resolved location cannot start with multiple slashes.`) : S.matched.length || V(`No match found for location with path "${m.path != null ? m.path : m}"`)), I({
      fullPath: j,
      // keep the hash encoded so fullPath is effectively path + encodedQuery +
      // hash
      hash: T,
      query: (
        // if the user is using a custom query lib like qs, we might have
        // nested objects, so we keep the query as is, meaning it can contain
        // numbers at `$route.query`, but at the point, the user will have to
        // use their own type anyway.
        // https://github.com/vuejs/router/issues/328#issuecomment-649481567
        r === Mt ? Ko(m.query) : m.query || {}
      )
    }, S, {
      redirectedFrom: void 0,
      href: k
    });
  }
  function _(m) {
    return typeof m == "string" ? Je(n, m, l.value.path) : I({}, m);
  }
  function b(m, E) {
    if (d !== m)
      return pe(8, {
        from: E,
        to: m
      });
  }
  function R(m) {
    return x(m);
  }
  function $(m) {
    return R(I(_(m), { replace: !0 }));
  }
  function G(m) {
    const E = m.matched[m.matched.length - 1];
    if (E && E.redirect) {
      const { redirect: w } = E;
      let S = typeof w == "function" ? w(m) : w;
      if (typeof S == "string" && (S = S.includes("?") || S.includes("#") ? S = _(S) : (
        // force empty params
        { path: S }
      ), S.params = {}), O.NODE_ENV !== "production" && S.path == null && !("name" in S))
        throw V(`Invalid redirect found:
${JSON.stringify(S, null, 2)}
 when navigating to "${m.fullPath}". A redirect must contain a name or path. This will break in production.`), new Error("Invalid redirect");
      return I({
        query: m.query,
        hash: m.hash,
        // avoid transferring params if the redirect has a path
        params: S.path != null ? {} : m.params
      }, S);
    }
  }
  function x(m, E) {
    const w = d = y(m), S = l.value, T = m.state, j = m.force, k = m.replace === !0, P = G(w);
    if (P)
      return x(
        I(_(P), {
          state: typeof P == "object" ? I({}, T, P.state) : T,
          force: j,
          replace: k
        }),
        // keep original redirectedFrom if it exists
        E || w
      );
    const C = w;
    C.redirectedFrom = E;
    let ne;
    return !j && Pt(r, S, w) && (ne = pe(16, { to: C, from: S }), _t(
      S,
      S,
      // this is a push, the only way for it to be triggered from a
      // history.listen is with a redirect, which makes it become a push
      !0,
      // This cannot be the first navigation because the initial location
      // cannot be manually navigated to
      !1
    )), (ne ? Promise.resolve(ne) : ce(C, S)).catch((M) => z(M) ? (
      // navigation redirects still mark the router as ready
      z(
        M,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? M : He(M)
    ) : (
      // reject any unknown error
      qe(M, C, S)
    )).then((M) => {
      if (M) {
        if (z(
          M,
          2
          /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
        ))
          return O.NODE_ENV !== "production" && // we are redirecting to the same location we were already at
          Pt(r, y(M.to), C) && // and we have done it a couple of times
          E && // @ts-expect-error: added only in dev
          (E._count = E._count ? (
            // @ts-expect-error
            E._count + 1
          ) : 1) > 30 ? (V(`Detected a possibly infinite redirection in a navigation guard when going from "${S.fullPath}" to "${C.fullPath}". Aborting to avoid a Stack Overflow.
 Are you always returning a new location within a navigation guard? That would lead to this error. Only return when redirecting or aborting, that should fix this. This might break in production if not fixed.`), Promise.reject(new Error("Infinite redirect in navigation guard"))) : x(
            // keep options
            I({
              // preserve an existing replacement but allow the redirect to override it
              replace: k
            }, _(M.to), {
              state: typeof M.to == "object" ? I({}, T, M.to.state) : T,
              force: j
            }),
            // preserve the original redirectedFrom if any
            E || C
          );
      } else
        M = wt(C, S, !0, k, T);
      return yt(C, S, M), M;
    });
  }
  function ae(m, E) {
    const w = b(m, E);
    return w ? Promise.reject(w) : Promise.resolve();
  }
  function te(m) {
    const E = Ne.values().next().value;
    return E && typeof E.runWithContext == "function" ? E.runWithContext(m) : m();
  }
  function ce(m, E) {
    let w;
    const [S, T, j] = gs(m, E);
    w = Xe(S.reverse(), "beforeRouteLeave", m, E);
    for (const P of S)
      P.leaveGuards.forEach((C) => {
        w.push(Y(C, m, E));
      });
    const k = ae.bind(null, m, E);
    return w.push(k), ue(w).then(() => {
      w = [];
      for (const P of i.list())
        w.push(Y(P, m, E));
      return w.push(k), ue(w);
    }).then(() => {
      w = Xe(T, "beforeRouteUpdate", m, E);
      for (const P of T)
        P.updateGuards.forEach((C) => {
          w.push(Y(C, m, E));
        });
      return w.push(k), ue(w);
    }).then(() => {
      w = [];
      for (const P of j)
        if (P.beforeEnter)
          if (U(P.beforeEnter))
            for (const C of P.beforeEnter)
              w.push(Y(C, m, E));
          else
            w.push(Y(P.beforeEnter, m, E));
      return w.push(k), ue(w);
    }).then(() => (m.matched.forEach((P) => P.enterCallbacks = {}), w = Xe(j, "beforeRouteEnter", m, E, te), w.push(k), ue(w))).then(() => {
      w = [];
      for (const P of s.list())
        w.push(Y(P, m, E));
      return w.push(k), ue(w);
    }).catch((P) => z(
      P,
      8
      /* ErrorTypes.NAVIGATION_CANCELLED */
    ) ? P : Promise.reject(P));
  }
  function yt(m, E, w) {
    c.list().forEach((S) => te(() => S(m, E, w)));
  }
  function wt(m, E, w, S, T) {
    const j = b(m, E);
    if (j)
      return j;
    const k = E === J, P = Q ? history.state : {};
    w && (S || k ? o.replace(m.fullPath, I({
      scroll: k && P && P.scroll
    }, T)) : o.push(m.fullPath, T)), l.value = m, _t(m, E, w, k), He();
  }
  let ge;
  function Bn() {
    ge || (ge = o.listen((m, E, w) => {
      if (!St.listening)
        return;
      const S = y(m), T = G(S);
      if (T) {
        x(I(T, { replace: !0, force: !0 }), S).catch(_e);
        return;
      }
      d = S;
      const j = l.value;
      Q && wo(Nt(j.fullPath, w.delta), We()), ce(S, j).catch((k) => z(
        k,
        12
        /* ErrorTypes.NAVIGATION_CANCELLED */
      ) ? k : z(
        k,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? (x(
        I(_(k.to), {
          force: !0
        }),
        S
        // avoid an uncaught rejection, let push call triggerError
      ).then((P) => {
        z(
          P,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && !w.delta && w.type === he.pop && o.go(-1, !1);
      }).catch(_e), Promise.reject()) : (w.delta && o.go(-w.delta, !1), qe(k, S, j))).then((k) => {
        k = k || wt(
          // after navigation, all matched components are resolved
          S,
          j,
          !1
        ), k && (w.delta && // a new navigation has been triggered, so we do not want to revert, that will change the current history
        // entry while a different route is displayed
        !z(
          k,
          8
          /* ErrorTypes.NAVIGATION_CANCELLED */
        ) ? o.go(-w.delta, !1) : w.type === he.pop && z(
          k,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && o.go(-1, !1)), yt(S, j, k);
      }).catch(_e);
    }));
  }
  let Ge = ye(), Et = ye(), ke;
  function qe(m, E, w) {
    He(m);
    const S = Et.list();
    return S.length ? S.forEach((T) => T(m, E, w)) : (O.NODE_ENV !== "production" && V("uncaught error during route navigation:"), console.error(m)), Promise.reject(m);
  }
  function Ln() {
    return ke && l.value !== J ? Promise.resolve() : new Promise((m, E) => {
      Ge.add([m, E]);
    });
  }
  function He(m) {
    return ke || (ke = !m, Bn(), Ge.list().forEach(([E, w]) => m ? w(m) : E()), Ge.reset()), m;
  }
  function _t(m, E, w, S) {
    const { scrollBehavior: T } = e;
    if (!Q || !T)
      return Promise.resolve();
    const j = !w && Eo(Nt(m.fullPath, 0)) || (S || !w) && history.state && history.state.scroll || null;
    return Ae().then(() => T(m, E, j)).then((k) => k && yo(k)).catch((k) => qe(k, m, E));
  }
  const Ke = (m) => o.go(m);
  let ze;
  const Ne = /* @__PURE__ */ new Set(), St = {
    currentRoute: l,
    listening: !0,
    addRoute: h,
    removeRoute: v,
    clearRoutes: t.clearRoutes,
    hasRoute: g,
    getRoutes: p,
    resolve: y,
    options: e,
    push: R,
    replace: $,
    go: Ke,
    back: () => Ke(-1),
    forward: () => Ke(1),
    beforeEach: i.add,
    beforeResolve: s.add,
    afterEach: c.add,
    onError: Et.add,
    isReady: Ln,
    install(m) {
      const E = this;
      m.component("RouterLink", Xo), m.component("RouterView", ns), m.config.globalProperties.$router = E, Object.defineProperty(m.config.globalProperties, "$route", {
        enumerable: !0,
        get: () => D(l)
      }), Q && // used for the initial navigation client side to avoid pushing
      // multiple times when the router is used in multiple apps
      !ze && l.value === J && (ze = !0, R(o.location).catch((T) => {
        O.NODE_ENV !== "production" && V("Unexpected error when starting the router:", T);
      }));
      const w = {};
      for (const T in J)
        Object.defineProperty(w, T, {
          get: () => l.value[T],
          enumerable: !0
        });
      m.provide(Ue, E), m.provide(vt, Hn(w)), m.provide(ut, l);
      const S = m.unmount;
      Ne.add(m), m.unmount = function() {
        Ne.delete(m), Ne.size < 1 && (d = J, ge && ge(), ge = null, l.value = J, ze = !1, ke = !1), S();
      }, O.NODE_ENV !== "production" && Q && ss(m, E, t);
    }
  };
  function ue(m) {
    return m.reduce((E, w) => E.then(() => te(w)), Promise.resolve());
  }
  return St;
}
function gs(e, t) {
  const n = [], r = [], o = [], i = Math.max(t.matched.length, e.matched.length);
  for (let s = 0; s < i; s++) {
    const c = t.matched[s];
    c && (e.matched.find((d) => ee(d, c)) ? r.push(c) : n.push(c));
    const l = e.matched[s];
    l && (t.matched.find((d) => ee(d, l)) || o.push(l));
  }
  return [n, r, o];
}
function vs() {
  return Z(Ue);
}
function ys(e) {
  return Z(vt);
}
const $n = /* @__PURE__ */ new Map();
function ws(e) {
  var t;
  (t = e.jsFn) == null || t.forEach((n) => {
    const { immediately: r = !1 } = n;
    let o = B(n.code);
    r && (o = o()), $n.set(n.id, o);
  });
}
function Es(e) {
  return $n.get(e);
}
function se(e) {
  let t = on(), n = Tr(), r = Dr(e), o = an(), i = vs(), s = ys();
  function c(p) {
    p.scopeSnapshot && (t = p.scopeSnapshot), p.slotSnapshot && (n = p.slotSnapshot), p.vforSnapshot && (r = p.vforSnapshot), p.elementRefSnapshot && (o = p.elementRefSnapshot), p.routerSnapshot && (i = p.routerSnapshot);
  }
  function l(p) {
    if (N.isVar(p))
      return q(d(p));
    if (N.isVForItem(p))
      return Fr(p.fid) ? r.getVForIndex(p.fid) : q(d(p));
    if (N.isVForIndex(p))
      return r.getVForIndex(p.fid);
    if (N.isJsFn(p)) {
      const { id: g } = p;
      return Es(g);
    }
    if (N.isSlotProp(p)) {
      const g = n.getPropsValue(p);
      return p.path ? fr(g, p.path) : g;
    }
    if (N.isRouterParams(p))
      return q(d(p));
    throw new Error(`Invalid binding: ${p}`);
  }
  function d(p) {
    if (N.isVar(p)) {
      const g = t.getVueRef(p) || br(p);
      return Ot(g, {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    if (N.isVForItem(p))
      return Mr({
        binding: p,
        snapshot: v
      });
    if (N.isVForIndex(p))
      return () => l(p);
    if (N.isRouterParams(p)) {
      const { prop: g = "params" } = p;
      return Ot(() => s[g], {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    throw new Error(`Invalid binding: ${p}`);
  }
  function u(p) {
    if (N.isVar(p) || N.isVForItem(p))
      return d(p);
    if (N.isVForIndex(p) || N.isJsFn(p))
      return l(p);
    if (N.isRouterParams(p))
      return d(p);
    throw new Error(`Invalid binding: ${p}`);
  }
  function a(p) {
    if (N.isVar(p))
      return {
        sid: p.sid,
        id: p.id
      };
    if (N.isVForItem(p))
      return {
        type: "vf",
        fid: p.fid
      };
    if (N.isVForIndex(p))
      return {
        type: "vf-i",
        fid: p.fid,
        value: null
      };
    if (N.isJsFn(p))
      return l(p);
  }
  function f(p) {
    var g, y;
    (g = p.vars) == null || g.forEach((_) => {
      d({ type: "var", ..._ }).value = _.val;
    }), (y = p.ele_refs) == null || y.forEach((_) => {
      o.getRef({
        sid: _.sid,
        id: _.id
      }).value[_.method](..._.args);
    });
  }
  function h(p, g) {
    if (Rt(g) || Rt(p.values))
      return;
    g = g;
    const y = p.values, _ = p.types ?? new Array(g.length).fill(0);
    g.forEach((b, R) => {
      const $ = _[R];
      if ($ === 1)
        return;
      if (N.isVar(b)) {
        const x = d(b);
        if ($ === 2) {
          y[R].forEach(([te, ce]) => {
            lr(x.value, te, ce);
          });
          return;
        }
        x.value = y[R];
        return;
      }
      if (N.isRouterAction(b)) {
        const x = y[R], ae = i[x.fn];
        ae(...x.args);
        return;
      }
      if (N.isElementRef(b)) {
        const x = o.getRef(b).value, ae = y[R], { method: te, args: ce = [] } = ae;
        x[te](...ce);
        return;
      }
      const G = d(b);
      G.value = y[R];
    });
  }
  const v = {
    getVForIndex: r.getVForIndex,
    getObjectToValue: l,
    getVueRefObject: d,
    getVueRefObjectOrValue: u,
    getBindingServerInfo: a,
    updateRefFromServer: f,
    updateOutputsRefFromServer: h,
    replaceSnapshot: c
  };
  return v;
}
class _s {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: i } = t, s = Ze().webServerInfo, c = i !== void 0 ? { key: i } : {}, l = r === "sync" ? s.event_url : s.event_async_url;
    let d = {};
    const u = await fetch(l, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        bind: n,
        hKey: o,
        ...c,
        page: $e(),
        ...d
      })
    });
    if (!u.ok)
      throw new Error(`HTTP error! status: ${u.status}`);
    return await u.json();
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig, i = Ze().webServerInfo, s = r === "sync" ? i.watch_url : i.watch_async_url, c = t.getServerInputs(), l = {
      key: o,
      input: c,
      page: $e()
    };
    return await (await fetch(s, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(l)
    })).json();
  }
}
class Ss {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: i } = t, s = i !== void 0 ? { key: i } : {};
    let c = {};
    const l = {
      bind: n,
      fType: r,
      hKey: o,
      ...s,
      page: $e(),
      ...c
    };
    return await window.pywebview.api.event_call(l);
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig, i = t.getServerInputs(), s = {
      key: o,
      input: i,
      fType: r,
      page: $e()
    };
    return await window.pywebview.api.watch_call(s);
  }
}
let ft;
function bs(e) {
  switch (e) {
    case "web":
      ft = new _s();
      break;
    case "webview":
      ft = new Ss();
      break;
  }
}
function xn() {
  return ft;
}
function Os(e) {
  const t = {
    type: "var",
    sid: e.sid,
    id: e.id
  };
  return {
    ...e,
    immediate: !0,
    outputs: [t, ...e.outputs || []]
  };
}
function jn(e) {
  const { config: t, snapshot: n } = e;
  if (!t)
    return {
      run: () => {
      },
      tryReset: () => {
      }
    };
  const r = t.map((s) => {
    const c = n.getVueRefObject(s.target);
    return s.type === "const" ? {
      refObj: c,
      preValue: c.value,
      newValue: s.value,
      reset: !0
    } : Rs(c, s, n);
  });
  return {
    run: () => {
      r.forEach((s) => {
        s.newValue !== s.preValue && (s.refObj.value = s.newValue);
      });
    },
    tryReset: () => {
      r.forEach((s) => {
        s.reset && (s.refObj.value = s.preValue);
      });
    }
  };
}
function Rs(e, t, n) {
  const r = B(t.code), o = t.inputs.map(
    (i) => n.getObjectToValue(i)
  );
  return {
    refObj: e,
    preValue: e.value,
    reset: t.reset ?? !0,
    newValue: r(...o)
  };
}
function Vs(e, t, n) {
  return new Ps(e, t, n);
}
class Ps {
  constructor(t, n, r) {
    F(this, "taskQueue", []);
    F(this, "id2TaskMap", /* @__PURE__ */ new Map());
    F(this, "input2TaskIdMap", Oe(() => []));
    this.snapshots = r;
    const o = [], i = (s) => {
      var l;
      const c = new ks(s, r);
      return this.id2TaskMap.set(c.id, c), (l = s.inputs) == null || l.forEach((d, u) => {
        var f, h;
        if (((f = s.data) == null ? void 0 : f[u]) === 0 && ((h = s.slient) == null ? void 0 : h[u]) === 0) {
          const v = `${d.sid}-${d.id}`;
          this.input2TaskIdMap.getOrDefault(v).push(c.id);
        }
      }), c;
    };
    t == null || t.forEach((s) => {
      const c = i(s);
      o.push(c);
    }), n == null || n.forEach((s) => {
      const c = i(
        Os(s)
      );
      o.push(c);
    }), o.forEach((s) => {
      const {
        deep: c = !0,
        once: l,
        flush: d,
        immediate: u = !0
      } = s.watchConfig, a = {
        immediate: u,
        deep: c,
        once: l,
        flush: d
      }, f = this._getWatchTargets(s);
      K(
        f,
        (h) => {
          h.some(be) || (s.modify = !0, this.taskQueue.push(new Ns(s)), this._scheduleNextTick());
        },
        a
      );
    });
  }
  _getWatchTargets(t) {
    if (!t.watchConfig.inputs)
      return [];
    const n = t.slientInputs, r = t.constDataInputs;
    return t.watchConfig.inputs.filter(
      (i, s) => !r[s] && (N.isVar(i) || N.isVForItem(i) || N.isRouterParams(i)) && !n[s]
    ).map((i) => this.snapshots.getVueRefObjectOrValue(i));
  }
  _scheduleNextTick() {
    Ae(() => this._runAllTasks());
  }
  _runAllTasks() {
    const t = this.taskQueue.slice();
    this.taskQueue.length = 0, this._setTaskNodeRelations(t), t.forEach((n) => {
      n.run();
    });
  }
  _setTaskNodeRelations(t) {
    t.forEach((n) => {
      const r = this._findNextNodes(n, t);
      n.appendNextNodes(...r), r.forEach((o) => {
        o.appendPrevNodes(n);
      });
    });
  }
  _findNextNodes(t, n) {
    const r = t.watchTask.watchConfig.outputs;
    if (r && r.length <= 0)
      return [];
    const o = this._getCalculatorTasksByOutput(
      t.watchTask.watchConfig.outputs
    );
    return n.filter(
      (i) => o.has(i.watchTask.id) && i.watchTask.id !== t.watchTask.id
    );
  }
  _getCalculatorTasksByOutput(t) {
    const n = /* @__PURE__ */ new Set();
    return t == null || t.forEach((r) => {
      const o = `${r.sid}-${r.id}`;
      (this.input2TaskIdMap.get(o) || []).forEach((s) => n.add(s));
    }), n;
  }
}
class ks {
  constructor(t, n) {
    F(this, "modify", !0);
    F(this, "_running", !1);
    F(this, "id");
    F(this, "_runningPromise", null);
    F(this, "_runningPromiseResolve", null);
    F(this, "_inputInfos");
    this.watchConfig = t, this.snapshot = n, this.id = Symbol(t.debug), this._inputInfos = this.createInputInfos();
  }
  createInputInfos() {
    const { inputs: t = [] } = this.watchConfig, n = this.watchConfig.data || new Array(t.length).fill(0), r = this.watchConfig.slient || new Array(t.length).fill(0);
    return {
      const_data: n,
      slients: r
    };
  }
  get slientInputs() {
    return this._inputInfos.slients;
  }
  get constDataInputs() {
    return this._inputInfos.const_data;
  }
  getServerInputs() {
    const { const_data: t } = this._inputInfos;
    return this.watchConfig.inputs ? this.watchConfig.inputs.map((n, r) => t[r] === 0 ? this.snapshot.getObjectToValue(n) : n) : [];
  }
  get running() {
    return this._running;
  }
  get runningPromise() {
    return this._runningPromise;
  }
  /**
   * setRunning
   */
  setRunning() {
    this._running = !0, this._runningPromise = new Promise((t) => {
      this._runningPromiseResolve = t;
    }), this._trySetRunningRef(!0);
  }
  /**
   * taskDone
   */
  taskDone() {
    this._running = !1, this._runningPromiseResolve && (this._runningPromiseResolve(), this._runningPromiseResolve = null), this._trySetRunningRef(!1);
  }
  _trySetRunningRef(t) {
    if (this.watchConfig.running) {
      const n = this.snapshot.getVueRefObject(
        this.watchConfig.running
      );
      n.value = t;
    }
  }
}
class Ns {
  /**
   *
   */
  constructor(t) {
    F(this, "prevNodes", []);
    F(this, "nextNodes", []);
    F(this, "_runningPrev", !1);
    this.watchTask = t;
  }
  /**
   * appendPrevNodes
   */
  appendPrevNodes(...t) {
    this.prevNodes.push(...t);
  }
  /**
   *
   */
  appendNextNodes(...t) {
    this.nextNodes.push(...t);
  }
  /**
   * hasNextNodes
   */
  hasNextNodes() {
    return this.nextNodes.length > 0;
  }
  /**
   * run
   */
  async run() {
    if (this.prevNodes.length > 0 && !this._runningPrev)
      try {
        this._runningPrev = !0, await Promise.all(this.prevNodes.map((t) => t.run()));
      } finally {
        this._runningPrev = !1;
      }
    if (this.watchTask.running) {
      await this.watchTask.runningPromise;
      return;
    }
    if (this.watchTask.modify) {
      this.watchTask.modify = !1, this.watchTask.setRunning();
      try {
        await Is(this.watchTask);
      } finally {
        this.watchTask.taskDone();
      }
    }
  }
}
async function Is(e) {
  const { snapshot: t } = e, { outputs: n, preSetup: r } = e.watchConfig, o = jn({
    config: r,
    snapshot: t
  });
  try {
    o.run();
    const i = await xn().watchSend(e);
    if (!i)
      return;
    t.updateOutputsRefFromServer(i, n);
  } finally {
    o.tryReset();
  }
}
function Ts(e, t) {
  const {
    on: n,
    code: r,
    immediate: o,
    deep: i,
    once: s,
    flush: c,
    bind: l = {},
    onData: d,
    bindData: u
  } = e, a = d || new Array(n.length).fill(0), f = u || new Array(Object.keys(l).length).fill(0), h = Be(
    l,
    (g, y, _) => f[_] === 0 ? t.getVueRefObject(g) : g
  ), v = B(r, h), p = n.length === 1 ? Gt(a[0] === 1, n[0], t) : n.map(
    (g, y) => Gt(a[y] === 1, g, t)
  );
  return K(p, v, { immediate: o, deep: i, once: s, flush: c });
}
function Gt(e, t, n) {
  return e ? () => t : n.getVueRefObject(t);
}
function As(e, t) {
  const {
    inputs: n = [],
    outputs: r,
    slient: o,
    data: i,
    code: s,
    immediate: c = !0,
    deep: l,
    once: d,
    flush: u
  } = e, a = o || new Array(n.length).fill(0), f = i || new Array(n.length).fill(0), h = B(s), v = n.filter((g, y) => a[y] === 0 && f[y] === 0).map((g) => t.getVueRefObject(g));
  function p() {
    return n.map((g, y) => f[y] === 0 ? nn(q(t.getVueRefObject(g))) : g);
  }
  K(
    v,
    () => {
      let g = h(...p());
      if (!r)
        return;
      const _ = r.length === 1 ? [g] : g, b = _.map((R) => R === void 0 ? 1 : 0);
      t.updateOutputsRefFromServer(
        { values: _, types: b },
        r
      );
    },
    { immediate: c, deep: l, once: d, flush: u }
  );
}
function Cs(e, t) {
  return Object.assign(
    {},
    ...Object.entries(e ?? {}).map(([n, r]) => {
      const o = r.map((c) => {
        if (c.type === "web") {
          const l = $s(c.bind, t);
          return xs(c, l, t);
        } else {
          if (c.type === "vue")
            return Ds(c, t);
          if (c.type === "js")
            return js(c, t);
        }
        throw new Error(`unknown event type ${c}`);
      }), s = B(
        " (...args)=> Promise.all(promises(...args))",
        {
          promises: (...c) => o.map(async (l) => {
            await l(...c);
          })
        }
      );
      return { [n]: s };
    })
  );
}
function $s(e, t) {
  return (...n) => (e ?? []).map((r) => {
    if (N.isEventContext(r)) {
      if (r.path.startsWith(":")) {
        const o = r.path.slice(1);
        return B(o)(...n);
      }
      return Re(n[0], r.path.split("."));
    }
    return N.IsBinding(r) ? t.getObjectToValue(r) : r;
  });
}
function xs(e, t, n) {
  async function r(...o) {
    const i = t(...o), s = jn({
      config: e.preSetup,
      snapshot: n
    });
    try {
      s.run();
      const c = await xn().eventSend(e, i);
      if (!c)
        return;
      n.updateOutputsRefFromServer(c, e.set);
    } finally {
      s.tryReset();
    }
  }
  return r;
}
function js(e, t) {
  const { code: n, inputs: r = [], set: o } = e, i = B(n);
  function s(...c) {
    const l = (r ?? []).map((u) => {
      if (N.isEventContext(u)) {
        if (u.path.startsWith(":")) {
          const a = u.path.slice(1);
          return B(a)(...c);
        }
        return Re(c[0], u.path.split("."));
      }
      return N.IsBinding(u) ? nn(t.getObjectToValue(u)) : u;
    }), d = i(...l);
    if (o !== void 0) {
      const a = o.length === 1 ? [d] : d, f = a.map((h) => h === void 0 ? 1 : 0);
      t.updateOutputsRefFromServer({ values: a, types: f }, o);
    }
  }
  return s;
}
function Ds(e, t) {
  const { code: n, bind: r = {}, bindData: o } = e, i = o || new Array(Object.keys(r).length).fill(0), s = Be(
    r,
    (d, u, a) => i[a] === 0 ? t.getVueRefObject(d) : d
  ), c = B(n, s);
  function l(...d) {
    c(...d);
  }
  return l;
}
function Ms(e, t) {
  const n = [];
  (e.bStyle || []).forEach((i) => {
    Array.isArray(i) ? n.push(
      ...i.map((s) => t.getObjectToValue(s))
    ) : n.push(
      Be(
        i,
        (s) => t.getObjectToValue(s)
      )
    );
  });
  const r = zn([e.style || {}, n]);
  return {
    hasStyle: r && Object.keys(r).length > 0,
    styles: r
  };
}
function Fs(e, t) {
  const n = e.classes;
  if (!n)
    return null;
  if (typeof n == "string")
    return Ce(n);
  const { str: r, map: o, bind: i } = n, s = [];
  return r && s.push(r), o && s.push(
    Be(
      o,
      (c) => t.getObjectToValue(c)
    )
  ), i && s.push(...i.map((c) => t.getObjectToValue(c))), Ce(s);
}
function je(e, t = !0) {
  if (!(typeof e != "object" || e === null)) {
    if (Array.isArray(e)) {
      t && e.forEach((n) => je(n, !0));
      return;
    }
    for (const [n, r] of Object.entries(e))
      if (n.startsWith(":"))
        try {
          e[n.slice(1)] = new Function(`return (${r})`)(), delete e[n];
        } catch (o) {
          console.error(
            `Error while converting ${n} attribute to function:`,
            o
          );
        }
      else
        t && je(r, !0);
  }
}
function Bs(e, t) {
  const n = e.startsWith(":");
  return n && (e = e.slice(1), t = B(t)), { name: e, value: t, isFunc: n };
}
function Ls(e, t, n) {
  var o;
  const r = {};
  return bt(e.bProps || {}, (i, s) => {
    const c = n.getObjectToValue(i);
    be(c) || (je(c), r[s] = Ws(c, s));
  }), (o = e.proxyProps) == null || o.forEach((i) => {
    const s = n.getObjectToValue(i);
    typeof s == "object" && bt(s, (c, l) => {
      const { name: d, value: u } = Bs(l, c);
      r[d] = u;
    });
  }), { ...t || {}, ...r };
}
function Ws(e, t) {
  return t === "innerText" ? Me(e) : e;
}
function Us(e, { slots: t }) {
  const { id: n, use: r } = e.propsInfo, o = kr(n);
  return dt(() => {
    Ir(n);
  }), () => {
    const i = e.propsValue;
    return Nr(
      n,
      o,
      Object.fromEntries(
        r.map((s) => [s, i[s]])
      )
    ), A(Fe, null, t.default());
  };
}
const Gs = L(Us, {
  props: ["propsInfo", "propsValue"]
}), Dn = /* @__PURE__ */ new Map();
function qs(e) {
  var t;
  (t = e.scopes) == null || t.forEach((n) => {
    Dn.set(n.id, n);
  });
}
function me(e) {
  return Dn.get(e);
}
function Hs(e, t) {
  if (!e.slots)
    return null;
  const n = e.slots ?? {};
  return Array.isArray(n) ? t ? Ee(n) : () => Ee(n) : Zt(n, { keyFn: (s) => s === ":" ? "default" : s, valueFn: (s) => {
    const { items: c } = s;
    return (l) => {
      if (s.scopeId) {
        const d = () => s.props ? qt(s.props, l, c) : Ee(c);
        return A(
          Pe,
          { scope: me(s.scopeId) },
          d
        );
      }
      return s.props ? qt(s.props, l, c) : Ee(c);
    };
  } });
}
function qt(e, t, n) {
  return A(
    Gs,
    { propsInfo: e, propsValue: t },
    () => Ee(n)
  );
}
function Ee(e) {
  const t = (e ?? []).map((n) => A(ie, {
    component: n
  }));
  return t.length <= 0 ? null : t;
}
function Ks(e, t) {
  const n = {}, r = [];
  return (e || []).forEach((o) => {
    const { sys: i, name: s, arg: c, value: l, mf: d } = o;
    if (s === "vmodel") {
      const u = t.getVueRefObject(l);
      if (n[`onUpdate:${c}`] = (a) => {
        u.value = a;
      }, i === 1) {
        const a = d ? Object.fromEntries(d.map((f) => [f, !0])) : {};
        r.push([Qn, u.value, void 0, a]);
      } else
        n[c] = u.value;
    } else if (s === "vshow") {
      const u = t.getVueRefObject(l);
      r.push([Jn, u.value]);
    } else
      console.warn(`Directive ${s} is not supported yet`);
  }), {
    newProps: n,
    directiveArray: r
  };
}
function zs(e, t) {
  const { eRef: n } = e;
  return n === void 0 ? {} : { ref: t.getRef(n) };
}
function Qs(e) {
  const t = se(), n = an(), r = e.component.props ?? {};
  return je(r, !0), () => {
    const { tag: o } = e.component, i = N.IsBinding(o) ? t.getObjectToValue(o) : o, s = Yn(i), c = typeof s == "string", l = Fs(e.component, t), { styles: d, hasStyle: u } = Ms(e.component, t), a = Cs(e.component.events ?? {}, t), f = Hs(e.component, c), h = Ls(e.component, r, t), { newProps: v, directiveArray: p } = Ks(
      e.component.dir,
      t
    ), g = zs(
      e.component,
      n
    ), y = Xn({
      ...h,
      ...a,
      ...v,
      ...g
    }) || {};
    u && (y.style = d), l && (y.class = l);
    const _ = A(s, { ...y }, f);
    return p.length > 0 ? Zn(
      // @ts-ignore
      _,
      p
    ) : _;
  };
}
const ie = L(Qs, {
  props: ["component"]
});
function Mn(e, t) {
  var n, r;
  if (e) {
    const o = Vr(e), i = Sr(e, se(t)), s = se(t);
    Vs(e.py_watch, e.web_computed, s), (n = e.vue_watch) == null || n.forEach((c) => Ts(c, s)), (r = e.js_watch) == null || r.forEach((c) => As(c, s)), dt(() => {
      Rr(e.id, i), Pr(e.id, o);
    });
  }
}
function Js(e, { slots: t }) {
  const { scope: n } = e;
  return Mn(n), () => A(Fe, null, t.default());
}
const Pe = L(Js, {
  props: ["scope"]
}), Ys = L(
  (e) => {
    const { scope: t, items: n, vforInfo: r } = e;
    return Ar(r), Mn(t, r.key), n.length === 1 ? () => A(ie, {
      component: n[0]
    }) : () => n.map(
      (i) => A(ie, {
        component: i
      })
    );
  },
  {
    props: ["scope", "items", "vforInfo"]
  }
);
function Xs(e, t) {
  const { state: n, isReady: r, isLoading: o } = gr(async () => {
    let i = e;
    const s = t;
    if (!i && !s)
      throw new Error("Either config or configUrl must be provided");
    if (!i && s && (i = await (await fetch(s)).json()), !i)
      throw new Error("Failed to load config");
    return i;
  }, {});
  return { config: n, isReady: r, isLoading: o };
}
function Zs(e) {
  const t = H(!1), n = H("");
  function r(o, i) {
    let s;
    return i.component ? s = `Error captured from component:tag: ${i.component.tag} ; id: ${i.component.id} ` : s = "Error captured from app init", console.group(s), console.error("Component:", i.component), console.error("Error:", o), console.groupEnd(), e && (t.value = !0, n.value = `${s} ${o.message}`), !1;
  }
  return er(r), { hasError: t, errorMessage: n };
}
const ei = {
  class: "app-box insta-themes",
  "data-scaling": "100%"
}, ti = {
  key: 0,
  style: { position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }
}, ni = {
  key: 0,
  style: { color: "red", "font-size": "1.2em", margin: "1rem", border: "1px dashed red", padding: "1rem" }
}, ri = /* @__PURE__ */ L({
  __name: "App",
  props: {
    config: {},
    meta: {},
    configUrl: {}
  },
  setup(e) {
    const t = e, { debug: n = !1 } = t.meta, { config: r, isLoading: o } = Xs(
      t.config,
      t.configUrl
    );
    let i = null;
    K(r, (l) => {
      i = l, l.url && (cr({
        mode: t.meta.mode,
        version: t.meta.version,
        queryPath: l.url.path,
        pathParams: l.url.params,
        webServerInfo: l.webInfo
      }), bs(t.meta.mode)), qs(l), ws(l);
    });
    const { hasError: s, errorMessage: c } = Zs(n);
    return (l, d) => (re(), fe("div", ei, [
      D(o) ? (re(), fe("div", ti, d[0] || (d[0] = [
        tr("p", { style: { margin: "auto" } }, "Loading ...", -1)
      ]))) : (re(), fe("div", {
        key: 1,
        class: Ce(["insta-main", D(r).class])
      }, [
        nr(D(Pe), {
          scope: D(me)(D(i).scopeId)
        }, {
          default: rr(() => [
            (re(!0), fe(Fe, null, or(D(i).items, (u) => (re(), sr(D(ie), { component: u }, null, 8, ["component"]))), 256))
          ]),
          _: 1
        }, 8, ["scope"]),
        D(s) ? (re(), fe("div", ni, Me(D(c)), 1)) : ir("", !0)
      ], 2))
    ]));
  }
});
function oi(e) {
  const { on: t, scopeId: n, items: r } = e, o = me(n), i = se();
  return () => {
    const s = typeof t == "boolean" ? t : i.getObjectToValue(t);
    return A(Pe, { scope: o }, () => s ? r.map(
      (l) => A(ie, { component: l })
    ) : void 0);
  };
}
const si = L(oi, {
  props: ["on", "scopeId", "items"]
});
function ii(e) {
  const { start: t = 0, end: n, step: r = 1 } = e;
  let o = [];
  if (r > 0)
    for (let i = t; i < n; i += r)
      o.push(i);
  else
    for (let i = t; i > n; i += r)
      o.push(i);
  return o;
}
function ai(e) {
  const { array: t, bArray: n, items: r, fkey: o, fid: i, scopeId: s, num: c, tsGroup: l = {} } = e, d = t === void 0, u = c !== void 0, a = d ? n : t, f = se();
  $r(i, a, d, u);
  const v = di(o ?? "index");
  dt(() => {
    Or(s);
  });
  const p = me(s);
  return () => {
    const g = ui(
      u,
      d,
      a,
      f,
      c
    ), y = jr(i), _ = g.map((b, R) => {
      const $ = v(b, R);
      return y.add($), xr(i, $, R), A(Ys, {
        scope: p,
        items: r,
        vforInfo: {
          fid: i,
          key: $
        },
        key: $
      });
    });
    return y.removeUnusedKeys(), l && Object.keys(l).length > 0 ? A(Yt, l, {
      default: () => _
    }) : _;
  };
}
const ci = L(ai, {
  props: [
    "array",
    "items",
    "fid",
    "bArray",
    "scopeId",
    "num",
    "fkey",
    "tsGroup"
  ]
});
function ui(e, t, n, r, o) {
  if (e) {
    let s = 0;
    return typeof o == "number" ? s = o : s = r.getObjectToValue(o) ?? 0, ii({
      end: Math.max(0, s)
    });
  }
  const i = t ? r.getObjectToValue(n) || [] : n;
  return typeof i == "object" ? Object.values(i) : i;
}
const li = (e) => e, fi = (e, t) => t;
function di(e) {
  const t = vr(e);
  return typeof t == "function" ? t : e === "item" ? li : fi;
}
function hi(e) {
  const { scopeId: t, items: n } = e, r = me(t);
  return () => {
    const o = n.map((i) => A(ie, { component: i }));
    return A(Pe, { scope: r }, () => o);
  };
}
const Ht = L(hi, {
  props: ["scopeId", "items"]
});
function pi(e) {
  const { on: t, case: n, default: r } = e, o = se();
  return () => {
    const i = o.getObjectToValue(t), s = n.map((c) => {
      const { value: l, items: d, scopeId: u } = c.props;
      if (i === l)
        return A(Ht, {
          scopeId: u,
          items: d,
          key: ["case", l].join("-")
        });
    }).filter((c) => c);
    if (r && !s.length) {
      const { items: c, scopeId: l } = r.props;
      s.push(A(Ht, { scopeId: l, items: c, key: "default" }));
    }
    return A(Fe, s);
  };
}
const mi = L(pi, {
  props: ["case", "on", "default"]
});
function gi(e, { slots: t }) {
  const { name: n = "fade", tag: r } = e;
  return () => A(
    Yt,
    { name: n, tag: r },
    {
      default: t.default
    }
  );
}
const vi = L(gi, {
  props: ["name", "tag"]
});
function yi(e) {
  const { content: t, r: n = 0 } = e, r = se(), o = n === 1 ? () => r.getObjectToValue(t) : () => t;
  return () => Me(o());
}
const wi = L(yi, {
  props: ["content", "r"]
});
function Ei(e) {
  return `i-size-${e}`;
}
function _i(e) {
  return e ? `i-weight-${e}` : "";
}
function Si(e) {
  return e ? `i-text-align-${e}` : "";
}
const bi = /* @__PURE__ */ L({
  __name: "Heading",
  props: {
    text: {},
    size: {},
    weight: {},
    align: {}
  },
  setup(e) {
    const t = e, n = W(() => [
      Ei(t.size ?? "6"),
      _i(t.weight),
      Si(t.align)
    ]);
    return (r, o) => (re(), fe("h1", {
      class: Ce(["insta-Heading", n.value])
    }, Me(r.text), 3));
  }
});
function Oi(e) {
  if (!e.router)
    throw new Error("Router config is not provided.");
  const { routes: t, kAlive: n = !1 } = e.router;
  return t.map(
    (o) => Fn(o, n)
  );
}
function Fn(e, t) {
  var l;
  const { server: n = !1, vueItem: r, scopeId: o } = e, i = () => {
    if (n)
      throw new Error("Server-side rendering is not supported yet.");
    return Promise.resolve(
      Ri(r, me(o), t)
    );
  }, s = (l = r.children) == null ? void 0 : l.map(
    (d) => Fn(d, t)
  ), c = {
    ...r,
    children: s,
    component: i
  };
  return r.component.length === 0 && delete c.component, s === void 0 && delete c.children, c;
}
function Ri(e, t, n) {
  const { path: r, component: o } = e, i = A(
    Pe,
    { scope: t, key: r },
    () => o.map((c) => A(ie, { component: c }))
  );
  return n ? A(ar, null, () => i) : i;
}
function Vi(e, t) {
  const { mode: n = "hash" } = t.router, r = n === "hash" ? Ro() : n === "memory" ? Oo() : bn();
  e.use(
    ms({
      history: r,
      routes: Oi(t)
    })
  );
}
function Ni(e, t) {
  e.component("insta-ui", ri), e.component("vif", si), e.component("vfor", ci), e.component("match", mi), e.component("ts-group", vi), e.component("content", wi), e.component("heading", bi), t.router && Vi(e, t);
}
export {
  je as convertDynamicProperties,
  Ni as install
};
//# sourceMappingURL=insta-ui.js.map
