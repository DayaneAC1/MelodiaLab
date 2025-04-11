function verificarSenhas() {
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmar_senha').value;
    
    if (senha !== confirmarSenha) {
        alert("As senhas não são iguais.");
        return false;  // Impede o envio do formulário
    }
    return true;  // Permite o envio do formulário
}