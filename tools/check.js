#!/usr/bin/env node
/* Static checks for the single-file app.
   Runs in CI and locally: `node tools/check.js`
   Catches the mistakes that actually reach production here: a broken script,
   a duplicate id, a getElementById typo, a missing asset. */
const fs = require("fs");
const vm = require("vm");
const path = require("path");

const root = path.resolve(__dirname, "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const ok = [];
const fail = [];

// 1. every inline script must parse
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map(m => m[1]);
if (!scripts.length) fail.push("no inline scripts found");
scripts.forEach((code, i) => {
  try { new vm.Script(code); ok.push(`inline script ${i} parses`); }
  catch (e) { fail.push(`inline script ${i} syntax error: ${e.message}`); }
});

// 2. no duplicate ids
const idMatches = [...html.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]);
const counts = idMatches.reduce((m, id) => m.set(id, (m.get(id) || 0) + 1), new Map());
for (const [id, n] of counts) if (n > 1) fail.push(`duplicate id "${id}" appears ${n} times`);
ok.push(`${counts.size} unique ids`);

// 3. every getElementById target exists somewhere in the file
const refs = [...html.matchAll(/getElementById\("([^"]+)"\)/g)].map(m => m[1]);
const missing = [...new Set(refs)].filter(id => !counts.has(id));
missing.forEach(id => fail.push(`getElementById("${id}") has no matching element`));
ok.push(`${new Set(refs).size} id references resolved`);

// 4. referenced local assets exist on disk
const assets = [...html.matchAll(/(?:src|href)="(?!data:|https?:|#|\/\/)([^"]+)"/g)]
  .map(m => m[1])
  .filter(a => !a.includes("${"));
for (const a of new Set(assets)) {
  const p = path.join(root, a.replace(/^\.\//, ""));
  if (!fs.existsSync(p)) fail.push(`missing asset: ${a}`);
}
ok.push(`${new Set(assets).size} local assets checked`);

// 5. the self-test suite must still be wired up
if (!/function runSelfTests\s*\(/.test(html)) fail.push("runSelfTests() disappeared");
if (!/selftest/.test(html)) fail.push("?selftest gate disappeared");

if (fail.length) {
  console.error("FAILED\n" + fail.map(f => "  x " + f).join("\n"));
  console.error("\n" + ok.map(o => "  . " + o).join("\n"));
  process.exit(1);
}
console.log("All checks passed");
ok.forEach(o => console.log("  . " + o));
