// Author: João Victor Marques Favero
// Atualiza periodicamente a lista de empréstimos na home (a cada 60s) via fetch.

document.addEventListener('DOMContentLoaded', function () {
    // Container alvo no DOM
    const containerLista = document.getElementById('lista-emprestimos-container');

    // Prossegue apenas se o container existir e se for a página inicial
    if (!containerLista || window.location.pathname !== '/') return;

    // Busca o HTML da lista e injeta no container
    function atualizarListaEmprestimos() {
        console.log('Atualizando lista...');
        fetch('/api/ultimos-emprestimos/', {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
            .then((r) => r.text())
            .then((html) => {
                containerLista.innerHTML = html;
                console.log('Lista atualizada.');
            })
            .catch((e) => console.error('Erro ao atualizar a lista:', e));
    }

    // Atualização automática a cada 60s
    setInterval(atualizarListaEmprestimos, 60000);

    // Opcional: atualização imediata ao carregar
    // atualizarListaEmprestimos();
});
