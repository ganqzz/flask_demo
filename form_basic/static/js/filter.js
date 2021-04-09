const cardWrapper = document.querySelector('.card-wrapper');

document.querySelector('.filter-form')
  .addEventListener('submit', function(e) { // not arrow function
    e.preventDefault();
    // console.log(this);
    const form = this;
    const form_serialized = new URLSearchParams(new FormData(form)).toString()

    // browser location
    if (history.pushState) {
      history.replaceState("", "", "/?" + form_serialized);
    }

    // Formのデータにajaxフラグを付けて送信する
    fetch(form.getAttribute('action') + '?' + form_serialized + '&ajax=1', {
      method: 'GET',
      headers: {'Content-type': 'application/x-www-form-urlencoded'},
    }).then((res) => res.text())
      .then((data) => {
        // console.log(data);
        cardWrapper.innerHTML = data; // 書き換え
      });
  });
