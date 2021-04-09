const comment_form = document.querySelector('.comment-form');
const content = document.getElementById('content');
const comments = document.querySelector('.comments');
const comment_error = document.querySelector('.comment-error');

comment_form.addEventListener('submit', function(e) {
  e.preventDefault();
  const formData = new FormData(comment_form);
  formData.append('ajax', '1'); // Formのデータにajaxフラグを付ける
  const form_serialized = new URLSearchParams(formData).toString()

  fetch(comment_form.getAttribute('action'), {
    method: 'POST',
    headers: {'Content-type': 'application/x-www-form-urlencoded'},
    body: form_serialized,
  }).then((res) => {
    if (!res.ok) throw res;
    return res.text()
  }).then((data) => {
    content.value = '';
    comment_error.textContent = '';
    // console.log(data);
    comments.innerHTML = data + comments.innerHTML; // 最前に追記
  }).catch((error) => {
    content.value = '';
    error.text()  // Promise
      .then((error_msg) => comment_error.textContent = error_msg);
  });
});
