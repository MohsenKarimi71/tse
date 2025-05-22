var style = document.createElement('style');
style.setAttribute("id", "select_dropdown_styles");
style.innerHTML = `
.select-dropdown {
  display: inline-block;
  background-color: white;
  position: relative;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: left 1vw center;
  background-size: 16px 16px;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  padding: .375rem .75rem .375rem 2.25rem;
}

.select-dropdown span.placeholder {
  display: inline-block;
}

.select-dropdown span.placeholder {
  margin-right: 20px;
}

.select-dropdown span.selected_item {
  background-color: transparent;
  padding: 5px 10px;
  margin: 0px 5px;
  float: right;
}


.select-dropdown span.placeholder {
  color: #ced4da;
}

.select-dropdown-list-wrapper {
  box-shadow: gray 0 3px 8px;
  z-index: 100;
  border-radius: 10px;
  border: solid 1px #ced4da;
  display: none;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  background: white;
}

.select-dropdown-list-wrapper .select-dropdown-search {
  margin-bottom: 10px;
  margin-top: 0px;
}

.select-dropdown-list {
  overflow-y: auto;
  overflow-x: hidden;
}

.select-dropdown-list div {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
  align-items: center;
  padding: 5px 25px;
  margin: 0 1vw;
}

.select-dropdown-list input {
  width: 20px;
  height: 20px;
}

.select-dropdown-list div.selected {
  border-right: 5px solid rgb(67, 94, 190);
  color: rgb(67, 94, 190);
  font-weight: bold;
  margin: 1vh 2vw;
}

.select-dropdown-list div:hover {
  background-color: rgb(240, 241, 245);
}

`;
document.head.appendChild(style);

function SingleSelectDropdown() {
    var config = {
        txtSearch: "جستجو",
        height: '30vh',
        width: '100%',
        minHeight: '120px',
        placeholder: 'انتخاب نمایید',
    }

    function newEl(tag, attrs) {
        var e = document.createElement(tag);
        if (attrs !== undefined) Object.keys(attrs).forEach(k => {
            if (k === 'class') { Array.isArray(attrs[k]) ? attrs[k].forEach(o => o !== '' ? e.classList.add(o) : 0) : (attrs[k] !== '' ? e.classList.add(attrs[k]) : 0) }
            else if (k === 'style') {
                Object.keys(attrs[k]).forEach(ks => {
                    e.style[ks] = attrs[k][ks];
                });
            }
            else if (k === 'text') { attrs[k] === '' ? e.innerHTML = '&nbsp;' : e.innerText = attrs[k] }
            else e[k] = attrs[k];
        });
        return e;
    }

    document.querySelectorAll("select:not([multiple])").forEach((el, k) => {

        var div = newEl('div', {
            class: 'select-dropdown',
            style: { width: config.width } 
        });
        el.style.display = 'none';

        div.appendChild(newEl('span', {
            class: 'placeholder',
            text: config.placeholder
        }));

        el.parentNode.insertBefore(div, el.nextSibling);
        var listWrap = newEl('div', { class: 'select-dropdown-list-wrapper' });
        var list = newEl('div', {
            class: 'select-dropdown-list',
            style: { height: config.height, minHeight: config.minHeight}
        });
        var search = newEl('input', {
            class: ['select-dropdown-search'].concat([config.searchInput?.class ?? 'form-control']),
            style: { width: '100%', display: el.attributes['select-search']?.value === 'true' ? 'block' : 'none' },
            placeholder: config.txtSearch });
        listWrap.appendChild(search);
        div.appendChild(listWrap);
        listWrap.appendChild(list);

        el.loadOptions = () => {
            list.innerHTML = '';

            Array.from(el.options).forEach((o, k) => {
                if (k > 0) {
                    var op = newEl('div', { optEl: o })
                    op.appendChild(newEl('label', { text: o.text }));

                    op.addEventListener('click', () => {
                        if (!op.classList.contains('selected')) {
                            list.querySelectorAll("div").forEach((e, k) => {
                                e.classList.remove('selected');
                            })

                            op.classList.toggle('selected');
                            op.optEl.selected = !op.optEl.selected;
                            el.dispatchEvent(new Event('change'));
                        }
                    });

                    o.listitemEl = op;
                    list.appendChild(op);
                }
            })

            div.refresh = () => {
                if (div.querySelector('span.selected_item')) {
                    div.removeChild(div.querySelector('span.selected_item'));
                }

                if (el.selectedIndex !== 0) {
                    if (div.querySelector('span.placeholder')) {
                        div.removeChild(div.querySelector('span.placeholder'));
                    }

                    var selected_item = el.options[el.selectedIndex];
                    var selected_span = newEl('span', {
                        class: 'selected_item',
                        text: selected_item.text,
                        srcOption: selected_item
                    })
                    div.appendChild(selected_span);
                }

            };
        }

        el.loadOptions();
        
        search.addEventListener('input', () => {
            list.querySelectorAll(":scope > div").forEach(d => {
                var txt = d.querySelector("label").innerText.toUpperCase();
                d.style.display = txt.includes(search.value.toUpperCase()) ? 'flex' : 'none';
            });
        });

        div.addEventListener('click', () => {
            listWrap.style.display = 'block';
            search.focus();
            search.select();
        });

        document.addEventListener('click', function (event) {
            if (!div.contains(event.target)) {
                listWrap.style.display = 'none';
                div.refresh();
            }
        });
    })

}

window.addEventListener('load', () => {
    SingleSelectDropdown();
});
