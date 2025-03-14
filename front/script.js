document.getElementById("registerForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const formData = {
        name: document.getElementById("name").value,
        phone: document.getElementById("phone").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/api/users", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        document.getElementById("responseMessage").innerText = "Resposta da API: " + JSON.stringify(data);
    } catch (error) {
        document.getElementById("responseMessage").innerText = "Erro ao enviar os dados.";
    }
});
