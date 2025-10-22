// Crie este arquivo em: static/js/main.js

document.addEventListener('DOMContentLoaded', function() {

    // --- Lógica de Auto-Atualização da Tela Inicial ---
    const containerLista = document.getElementById('lista-emprestimos-container');

    if (containerLista) {
        
        // Verifica se estamos na Tela Inicial (pela URL)
        // Só queremos auto-atualização na Tela Inicial (URL '/')
        const isPaginaInicial = window.location.pathname === '/';

        if (isPaginaInicial) {
            function atualizarListaEmprestimos() {
                console.log("Buscando atualizações...");
                
                // Chama a URL da API definida em 'principal/urls.py'
                fetch('/api/ultimos-emprestimos/', {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.text())
                .then(html => {
                    containerLista.innerHTML = html;
                    console.log("Lista atualizada.");
                })
                .catch(error => {
                    console.error('Erro ao atualizar a lista:', error);
                });
            }

            // Atualiza a cada 60 segundos
            setInterval(atualizarListaEmprestimos, 60000);
        }
    }

});