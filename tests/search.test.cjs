const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const file = path.join(__dirname, '../docs/javascripts/docs.js');
test('exact service alias ranks its guide before incidental mentions', () => {
  assert.ok(fs.existsSync(file), 'docs search module must exist');
  const { rankGuides } = require(file);
  const guides = [
    {title:'Access Pi-hole via Nginx Proxy Manager', description:'Use NPM for DNS services', aliases:[],tags:['dns'],url:'pihole-on-npm/'},
    {title:'Nginx Proxy Manager', description:'Add HTTPS to your services', aliases:['npm'],tags:['reverse-proxy'],url:'npm/'}
  ];
  assert.equal(rankGuides(guides, 'NPM')[0].url, 'npm/');
  assert.equal(rankGuides(guides, 'nginx proxy manager')[0].url, 'npm/');
});
test('catalogue filters combine topic, type and normalised query', () => {
  const { matchesGuide } = require(file);
  assert.equal(typeof matchesGuide, 'function', 'catalogue filter must exist');
  const guide = { topic:'networking', type:'tutorial', search:'Pi-hole DNS with NPM' };
  assert.equal(matchesGuide(guide, {topic:'networking', type:'tutorial', q:'pi hole'}), true);
  assert.equal(matchesGuide(guide, {topic:'storage', type:'', q:''}), false);
  assert.equal(matchesGuide(guide, {topic:'', type:'series', q:'npm'}), false);
  assert.equal(matchesGuide(guide, {topic:'', type:'', q:'missing app'}), false);
});
