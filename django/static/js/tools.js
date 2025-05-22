function ajaxPost(url, data, csrftoken, onSuccessCallback=null, onErrorCallback=null) {
  $.ajax({
    url: url,
    data: data,
    type: "POST",
    processData: false, // important
    contentType: false, // important
    dataType : 'json',
    headers: {"X-CSRFToken": csrftoken},
    success: (result, status) => {
      if (onSuccessCallback != null) {
        onSuccessCallback(result);
      }
    },
    error: (xhr) => {
      if (onErrorCallback != null) {
        onErrorCallback();
      }
      if (xhr.status == 400) {
        warningAlert(xhr.responseText);
      }
      else if (xhr.status == 401) {
        warningAlert("ابتدا وارد حساب کاربری خود شوید");
      }
      else if (xhr.status == 403) {
        warningAlert("شما دسترسی انجام این کار را ندارید");
      }
      else if (xhr.status == 404) {
        warningAlert("آدرس وارد شده صحیح نیست");
      }
      else if (xhr.status == 405) {
        warningAlert("متد مورد استفاده مجاز نیست");
      }
      else {
        warningAlert("خطایی رخ داده است: " + " (" + xhr.statusText + ")");
      }
    },
  });
}


function ajaxPut(url, data, csrftoken, onSuccessCallback=null, onErrorCallback=null) {
  $.ajax({
    url: url,
    data: data,
    type: "PUT",
    processData: false, // important
    contentType: false, // important
    dataType : 'json',
    headers: {"X-CSRFToken": csrftoken},
    success: (result, status) => {
      if (onSuccessCallback != null) {
        onSuccessCallback(result);
      }
    },
    error: (xhr) => {
      if (onSuccessCallback != null) {
        onErrorCallback();
      }
      if (xhr.status == 400) {
        warningAlert(xhr.responseText);
      }
      else if (xhr.status == 401) {
        warningAlert("ابتدا وارد حساب کاربری خود شوید");
      }
      else if (xhr.status == 403) {
        warningAlert("شما دسترسی انجام این کار را ندارید");
      }
      else if (xhr.status == 404) {
        warningAlert("آدرس وارد شده صحیح نیست");
      }
      else if (xhr.status == 405) {
        warningAlert("متد مورد استفاده مجاز نیست");
      }
      else {
        warningAlert("خطایی رخ داده است: " + " (" + xhr.statusText + ")");
      }
    },
  });
}


function ajaxGet(url, data, onSuccessCallback=null, onErrorCallback=null) {
  $.ajax({
    url: url,
    type: "GET",
    data: data,
    dataType : 'json',
    success: (result, status) => {
      if (onSuccessCallback != null) {
        onSuccessCallback(result);
      }
    },
    error: (xhr) => {
      if (onErrorCallback != null) {
        onErrorCallback();
      }
      if (xhr.status == 400) {
        warningAlert(xhr.responseText);
      }
      else if (xhr.status == 401) {
        warningAlert("ابتدا وارد حساب کاربری خود شوید");
      }
      else if (xhr.status == 403) {
        warningAlert("شما دسترسی انجام این کار را ندارید");
      }
      else if (xhr.status == 404) {
        warningAlert("آدرس وارد شده صحیح نیست");
      }
      else if (xhr.status == 405) {
        warningAlert("متد مورد استفاده مجاز نیست");
      }
      else {
        warningAlert("خطایی رخ داده است: " + " (" + xhr.statusText + ")");
      }
    },
  });
}


const warningAlert = (msg) => {
  Toastify({
    text: msg,
    duration: 5000,
    destination: "", // link
    newWindow: true,
    close: true,
    gravity: "top", // `top` or `bottom`
    position: "left", // `left`, `center` or `right`
    stopOnFocus: true, // Prevents dismissing of toast on hover
    style: {
      background: "linear-gradient(to right, #bb2244, #ff1166)",
    },
    onClick: function () {}, // Callback after click
  }).showToast();
};


const successAlert = (msg) => {
  Toastify({
    text: msg,
    duration: 5000,
    destination: "", // link
    newWindow: true,
    close: true,
    gravity: "top", // `top` or `bottom`
    position: "left", // `left`, `center` or `right`
    stopOnFocus: true, // Prevents dismissing of toast on hover
    style: {
      background: "linear-gradient(to right, #22bb44, #11ff66)",
    },
    onClick: function () {}, // Callback after click
  }).showToast();
};
