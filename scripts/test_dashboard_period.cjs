const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, '..', 'dashboard.html'), 'utf8');
const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m => m[1]);
scripts.forEach(source => new vm.Script(source));
const source = scripts.find(s => s.includes('function formatChange'));
const cards = Array.from({length: 4}, () => {
  const elements = {};
  return {elements, querySelector: key => elements[key] ||= {}};
});
const context = vm.createContext({
  window: {location: {origin: 'http://localhost:8090'}},
  document: {querySelectorAll: () => cards},
  console,
});
vm.runInContext(source.slice(0, source.indexOf('        function updateTime()')), context);
assert.equal(context.formatChange(0, 5, true), '0.0%');
assert.equal(context.formatChange(null, 0, true), '无基数');
assert.equal(context.formatChange(null, 3, true), '新增（前期为0）');
assert.equal(context.formatChange(null, 3, false), '待对比');
assert.equal(context.formatChange(-15, 96, true), '-15.0%');
assert.equal(context.changeColor(-15), 'var(--accent-red)');
context.renderSummary({total_sites: 5, ga4_configured: 5, has_real_data: true,
  total_sessions: 96, total_pageviews: 100, total_users: 90,
  comparison_available: true, comparison_period_days: 7,
  sessions_change: -15, pageviews_change: -5});
assert.equal(cards[2].elements['.summary-change'].className, 'summary-change down');
assert.match(cards[2].elements['.summary-change'].innerHTML, /↘.*-15.0%/);
context.renderSummary({total_sites: 5, ga4_configured: 0, has_real_data: false,
  fetch_failed: 5, comparison_available: false});
assert.equal(cards[2].elements['.summary-value'].innerHTML, '—');
assert.match(cards[2].elements['.summary-label'].textContent, /部分/);
assert.match(html, /end_lag_days=/);
assert.match(html, /if \(sequence !== requestSequence\) return null/);
assert.match(html, /id="siteOverviewTitle"/);
console.log('Dashboard period UI: syntax and 14 regression assertions passed');
