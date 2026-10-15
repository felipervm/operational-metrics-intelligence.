(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('payload').textContent);
  const one = selector => document.querySelector(selector);
  const all = selector => Array.from(document.querySelectorAll(selector));
  const set = (selector, value) => { one(selector).textContent = value; };
  const percentage = value => value.toFixed(1);
  const number = (selector, value) => {
    const symbol = document.createElement('span'); symbol.textContent = '%';
    one(selector).replaceChildren(document.createTextNode(percentage(value)), symbol);
  };
  const overall = data.comparison['IT dashboard'];
  const critical = data.comparison['Security dashboard'];
  number('#overall', overall.value); number('#critical', critical.value);
  set('#overall-fraction', `${overall.numerator} resolved / ${overall.denominator} created`);
  set('#critical-fraction', `${critical.numerator} within target / ${critical.denominator} critical tickets`);
  one('#overall-bar').style.width = `${overall.value}%`;
  one('#critical-bar').style.width = `${critical.value}%`;
  set('#record-count', data.counts.records); set('#open-count', data.counts.open);

  const targets = { critical: 72, high: 120, medium: 168, low: 336 };
  const prompts = {
    critical: 'What explains the late critical completions, and does routing need review?',
    high: 'Which high-severity handoffs should be checked before the next operational review?',
    medium: 'What context do the open medium-severity tickets need before escalation?',
    low: 'Does on-time completion alone tell us whether the low-severity backlog is acceptable?'
  };
  const tabs = all('[data-severity]');
  function renderSeverity(severity) {
    const cohort = data.severity.find(item => item.severity === severity);
    const onTime = cohort.resolved - cohort.late_resolved;
    tabs.forEach(tab => {
      const active = tab.dataset.severity === severity;
      tab.setAttribute('aria-selected', String(active)); tab.tabIndex = active ? 0 : -1;
    });
    one('#cohort-panel').setAttribute('aria-labelledby', `tab-${severity}`);
    set('#cohort-title', `${severity[0].toUpperCase()}${severity.slice(1)} cohort`);
    number('#tier-rate', cohort.sla_met_pct);
    set('#cohort-description', `${onTime} of ${cohort.total} tickets completed within the sample target.`);
    set('#target-hours', `${targets[severity]}-hour illustrative target`);
    set('#tier-ontime', onTime); set('#tier-late', cohort.late_resolved); set('#tier-open', cohort.open);
    set('#cohort-prompt', prompts[severity]);
    const counts = [['ontime', onTime], ['late', cohort.late_resolved], ['open', cohort.open]];
    const fragment = document.createDocumentFragment();
    let index = 0;
    counts.forEach(([category, count]) => {
      one(`#stack-${category}`).style.width = `${100 * count / cohort.total}%`;
      for (let i = 0; i < count; i += 1) {
        const tile = document.createElement('span'); tile.className = `ticket-dot ${category}`;
        tile.style.setProperty('--i', index++); fragment.append(tile);
      }
    });
    one('#dot-grid').replaceChildren(fragment);
    one('#cohort-stack').setAttribute('aria-label', `${severity} tickets: ${onTime} within target, ${cohort.late_resolved} resolved late, ${cohort.open} still open. ${cohort.total} total.`);
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => renderSeverity(tab.dataset.severity));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault(); renderSeverity(tabs[next].dataset.severity); tabs[next].focus();
    });
  });
  renderSeverity('critical');

  const reviewTitles = ['Review the critical exceptions first.', 'Agree on what each KPI means.', 'Give every review a next action.'];
  function renderReview(index) {
    const item = data.findings[index];
    all('[data-review]').forEach(button => {
      const active = Number(button.dataset.review) === index;
      button.classList.toggle('active', active); button.setAttribute('aria-pressed', String(active));
    });
    set('#brief-title', reviewTitles[index]); set('#brief-priority', item.priority);
    set('#brief-observation', item.observation); set('#brief-decision', item.decision);
    set('#brief-owner', item.proposed_owner); set('#brief-validation', item.validation);
  }
  all('[data-review]').forEach(button => button.addEventListener('click', () => renderReview(Number(button.dataset.review))));
  renderReview(0);

  const menuButton = one('.menu-toggle'); const navigation = one('#navigation');
  function closeMenu() { navigation.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); }
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    navigation.classList.toggle('open', open); menuButton.setAttribute('aria-expanded', String(open));
  });
  navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') { closeMenu(); menuButton.focus(); }
  });
  document.addEventListener('click', event => { if (!one('.site-header').contains(event.target)) closeMenu(); });
  window.matchMedia('(min-width: 761px)').addEventListener('change', closeMenu);

  if ('IntersectionObserver' in window) {
    document.body.classList.add('js');
    const revealObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); revealObserver.unobserve(entry.target); }
    }), { threshold: 0.08 });
    all('.reveal').forEach(element => revealObserver.observe(element));
    const navLinks = all('#navigation a');
    const sectionObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navLinks.forEach(link => {
        if (link.getAttribute('href') === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }), { rootMargin: '-20% 0px -65% 0px' });
    all('main section[id]').forEach(element => sectionObserver.observe(element));
  }
  document.body.dataset.ready = 'operational-v2';
})();
