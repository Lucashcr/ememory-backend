const form = document.getElementById('reset-password-confirm-form');
form.addEventListener('submit', function (event) {
    event.preventDefault();

    const regex = /\/auth\/reset_password\/([a-zA-Z0-9_-]+)\/([a-zA-Z0-9_-]+)\//;
    const match = window.location.pathname.match(regex);

    const uid = match[1];
    const token = match[2];
    const newPassword = document.querySelector('input[name="new_password"]').value;
    const confirmPassword = document.querySelector('input[name="re_new_password"]').value;

    const csrftoken = getCookie('csrftoken');

    console.log({
        uid: uid,
        token: token,
        new_password: newPassword,
        re_new_password: confirmPassword,
    })

    fetch(`/auth/users/reset_password_confirm/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            uid: uid,
            token: token,
            new_password: newPassword,
            re_new_password: confirmPassword,
        })
    })
        .then(response => {
            if (response.ok) {
                alert("Sua senha foi alterada com sucesso!");
            } else {
                return response.json().then(data => {
                    const message = data.new_password ? data.new_password.join("\n") : "Erro desconhecido";
                    throw new Error(message);
                });
            }
        })
        .catch(error => {
            alert(`Ocorreu um erro ao alterar a senha:\n${error.message}`);
        });
});
