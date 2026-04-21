const input = document.querySelector('#note');
const save = document.querySelector('#save');
const notes = document.querySelector('#notes');

function loadNotes() {
  return JSON.parse(localStorage.getItem('notes') || '[]');
}

function render() {
  notes.innerHTML = loadNotes().map(note => `<div class="note">${note}</div>`).join('');
}

save.addEventListener('click', () => {
  const value = input.value.trim();
  if (!value) return;
  localStorage.setItem('notes', JSON.stringify([value, ...loadNotes()]));
  input.value = '';
  render();
});

render();
