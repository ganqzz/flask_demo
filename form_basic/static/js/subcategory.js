const category = document.getElementById('category');
const subcategory = document.getElementById('subcategory');

function append_option(id, content) {
  const option = document.createElement('option');
  option.setAttribute('value', id);
  option.text = content;
  subcategory.appendChild(option);
}

function subcategory_change() {
  // GET
  fetch('/category/' + category.value)
    .then((res) => res.json())
    .then((data) => {
      // console.log(data);
      subcategory.textContent = null;
      if (category.classList.contains('category-filter')) {
        append_option(0, '---')
      }

      for (const value of data.subcategories) {
        append_option(value[0], value[1]);
      }
    });
}

category.addEventListener('change', subcategory_change);

document.addEventListener('DOMContentLoaded', subcategory_change, false);
