# Student Table: Alpine.js Filters + Pagination

## Files to modify

### 1. `dashboard/views.py`

After `students_data` is built, add JSON serialization for Alpine and guild names to context.

Add after line 133 (`alerts = _build_alerts(guilds, all_students, total_grimoires)`):

```python
students_for_json = [{
    'id': s['student'].pk,
    'name': s['student'].user.get_full_name() or s['student'].user.username,
    'initial': (s['student'].user.get_full_name() or s['student'].user.username)[0].upper(),
    'guild': s['guild_name'],
    'level': s['level'],
    'mana': s['mana'],
    'grimoires': s['grimoires_completed'],
    'total_grimoires': s['total_grimoires'],
    'spells': s['spells_completed'],
    'progress': s['progress'],
} for s in students_data]
```

Update context to add:
```python
'students_json': json.dumps(students_for_json, ensure_ascii=False),
'guild_names': [g.name for g in guilds],
```

`json` is already imported at the top of the file (line 7).

### 2. `templates/dashboard/teacher_dashboard.html`

Replace lines 130-173 (the static student table section) with the Alpine-powered version:

```html
          <!-- Student table -->
          <section class="teacher-section">
            <div class="teacher-section__header">
              <h2 class="teacher-section__title">Alunos — visão geral</h2>
            </div>

            <div x-data="{
              page: 1,
              perPage: 10,
              search: '',
              guildFilter: '',
              students: [],
              init() {
                this.students = JSON.parse(this.\$el.getAttribute('data-students'));
                this.\$watch('search', () => this.page = 1);
                this.\$watch('guildFilter', () => this.page = 1);
              },
              get filtered() {
                return this.students.filter(s => {
                  const okSearch = !this.search || this.search.length < 3
                    || s.name.toLowerCase().includes(this.search.toLowerCase());
                  const okGuild = !this.guildFilter || s.guild === this.guildFilter;
                  return okSearch && okGuild;
                });
              },
              get paginated() {
                const start = (this.page - 1) * this.perPage;
                return this.filtered.slice(start, start + this.perPage);
              },
              get totalPages() {
                return Math.max(1, Math.ceil(this.filtered.length / this.perPage));
              },
              prevPage() { if (this.page > 1) this.page--; },
              nextPage() { if (this.page < this.totalPages) this.page++; },
              barClass(pct) {
                if (pct >= 70) return 'teacher-bar__fill--purple';
                if (pct >= 40) return 'teacher-bar__fill--gold';
                return 'teacher-bar__fill--cyan';
              }
            }" data-students='{{ students_json|safe }}'>

              <!-- Filters -->
              <div class="teacher-progress-filters">
                <div class="teacher-progress-search">
                  <svg class="teacher-progress-search__icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                  <input type="text" x-model="search" placeholder="Buscar aluno…" class="teacher-progress-search__input">
                </div>
                <div class="teacher-progress-filter-select">
                  <select x-model="guildFilter" class="teacher-progress-filter-select__input">
                    <option value="">Guilda: Todas</option>
                    {% for name in guild_names %}
                      <option value="{{ name }}">{{ name }}</option>
                    {% endfor %}
                  </select>
                  <svg class="teacher-progress-filter-select__chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
                </div>
                <span class="teacher-progress-filter-count" x-text="filtered.length + ' aluno' + (filtered.length !== 1 ? 's' : '')"></span>
              </div>

              <!-- Table -->
              <div class="teacher-table">
                <div class="teacher-table__header">
                  <span>Aluno</span>
                  <span>Guilda</span>
                  <span>Nível</span>
                  <span>Mana</span>
                  <span>Grimórios</span>
                  <span>Feitiços</span>
                  <span>Progresso</span>
                </div>
                <template x-for="s in paginated" :key="s.id">
                  <div class="teacher-table__row">
                    <div class="teacher-table__cell teacher-table__cell--name">
                      <span class="teacher-table__avatar" x-text="s.initial"></span>
                      <span x-text="s.name"></span>
                    </div>
                    <span class="teacher-table__cell teacher-table__cell--guild" x-text="s.guild"></span>
                    <span class="teacher-table__cell teacher-table__cell--num" x-text="s.level"></span>
                    <span class="teacher-table__cell teacher-table__cell--mana" x-text="s.mana"></span>
                    <span class="teacher-table__cell teacher-table__cell--num" x-text="s.grimoires + '/' + s.total_grimoires"></span>
                    <span class="teacher-table__cell teacher-table__cell--num" x-text="s.spells"></span>
                    <div class="teacher-table__cell teacher-table__cell--bar">
                      <div class="teacher-bar">
                        <div class="teacher-bar__fill" :class="barClass(s.progress)" :style="'width:' + s.progress + '%'"></div>
                      </div>
                    </div>
                  </div>
                </template>
              </div>

              <template x-if="filtered.length === 0">
                <p class="teacher-empty">Nenhum aluno encontrado.</p>
              </template>

              <!-- Pagination -->
              <div class="teacher-pagination" x-show="totalPages > 1">
                <button class="teacher-pagination__btn" @click="prevPage" :disabled="page === 1">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
                  Anterior
                </button>
                <span class="teacher-pagination__info" x-text="'Página ' + page + ' de ' + totalPages"></span>
                <button class="teacher-pagination__btn" @click="nextPage" :disabled="page === totalPages">
                  Próxima
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
                </button>
              </div>
            </div>
          </section>
```

### 3. `static/css/teacher.css`

Add at end of file:

```css
.teacher-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
}

.teacher-pagination__btn {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
  font-family: 'Inter', system-ui, sans-serif;
  color: #c4b5fd;
  background: #16112e;
  border: 1px solid rgba(124, 58, 237, 0.25);
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background 0.15s;
}

.teacher-pagination__btn:hover:not(:disabled) {
  background: rgba(124, 58, 237, 0.12);
}

.teacher-pagination__btn:disabled {
  opacity: 0.35;
  cursor: default;
}

.teacher-pagination__info {
  font-size: 0.75rem;
  color: #8b7db8;
  font-family: 'Inter', system-ui, sans-serif;
}
```

## Summary

| File | Change |
|---|---|
| `dashboard/views.py` | Add `students_json` and `guild_names` to context |
| `teacher_dashboard.html` | Replace static table with Alpine x-data block (filters + pagination) |
| `teacher.css` | Add `.teacher-pagination` and `.teacher-pagination__btn` styles |
