// Author: João Victor Marques Favero

document.addEventListener('DOMContentLoaded', function () {
    
    // --- Lógica 1: Atualização da lista de empréstimos (Sem alterações) ---
    const containerLista = document.getElementById('lista-emprestimos-staff');
    if (containerLista && window.location.pathname === '/') {
        function atualizarListaEmprestimos() {
            // ... (código de atualização da lista) ...
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
        setInterval(atualizarListaEmprestimos, 60000);
    }
    
    // --- Lógica 2: Script de Upload de Imagem (Sem alterações) ---
    const scanFormUpload = document.getElementById('form-scan-upload');
    const scanInputUpload = document.getElementById('qr_image_input');
    const scanLoadingMessage = document.getElementById('scan-loading-message');

    if (scanFormUpload && scanInputUpload && scanLoadingMessage) {
        scanInputUpload.addEventListener('change', function() {
            if (scanInputUpload.files.length > 0) {
                scanLoadingMessage.style.display = 'block';
                scanFormUpload.submit();
            }
        });
    }

    // --- Lógica 3: Script de Scan por Vídeo (Com MODIFICAÇÕES) ---
    const btnIniciarScan = document.getElementById('btn-iniciar-scan-video');
    const btnCancelarScan = document.getElementById('btn-cancelar-scan');
    const scannerContainer = document.getElementById('qr-reader-container');
    const statusEl = document.getElementById('qr-reader-status');
    const actionsContainer = document.getElementById('scan-actions-container');

    // Só executa esta lógica se os elementos do scanner de vídeo existirem
    if (btnIniciarScan && btnCancelarScan && scannerContainer && statusEl && actionsContainer) {
        
        let html5QrcodeScanner = null; // Guarda a instância do scanner
        let redirectionDone = false;
        let isScannerRunning = false; // Flag para evitar múltiplas chamadas

        // Função chamada no SUCESSO do scan de vídeo
        function onScanSuccess(decodedText, decodedResult) {
            if (decodedText && !redirectionDone) {
                redirectionDone = true;
                statusEl.innerHTML = `QR Code detectado! Redirecionando...`;
                
                if (html5QrcodeScanner && isScannerRunning) {
                    html5QrcodeScanner.clear().catch(error => {
                        console.error("Falha ao limpar o scanner.", error);
                    });
                    isScannerRunning = false;
                }
                window.location.href = decodedText;
            }
        }

        // Função chamada na FALHA (frame não encontrado)
        function onScanFailure(error) {
            // Apenas "não encontrado", não é um erro real.
        }

        function iniciarScannerVideo() {
            // Se o scanner já estiver rodando, não faz nada
            if (isScannerRunning) {
                return;
            }

            // Esconde os botões de ação
            actionsContainer.style.display = 'none';

            // Mostra o container do scanner
            scannerContainer.style.display = 'block';
            statusEl.innerHTML = "Iniciando câmera...";
            
            // Configura e inicia o scanner
            const scannerConfig = {
                fps: 10,
                qrbox: { width: 250, height: 250 },
                rememberLastUsedCamera: true,
                supportedScanTypes: [
                    Html5QrcodeScanType.SCAN_TYPE_CAMERA
                ],
                camera: { facingMode: "environment" } // Pede a câmera traseira
            };

            if (!html5QrcodeScanner) {
                html5QrcodeScanner = new Html5QrcodeScanner(
                    "qr-reader",     // ID do Div
                    scannerConfig,   // Configurações
                    /* verbose= */ false
                );
            }
            
            redirectionDone = false; // Reseta o flag
            html5QrcodeScanner.render(onScanSuccess, onScanFailure);
            isScannerRunning = true; // Marca que o scanner está ativo
            statusEl.innerHTML = "Posicione o QR Code na área de leitura.";
        }

        // 2. Clicar em "Cancelar" (no scanner de vídeo)
        btnCancelarScan.addEventListener('click', function() {
            if (html5QrcodeScanner && isScannerRunning) {
                html5QrcodeScanner.clear().catch(error => {
                    console.error("Falha ao parar o scanner.", error);
                });
                isScannerRunning = false;
            }
            scannerContainer.style.display = 'none';
            actionsContainer.style.display = 'block';
        });
        
        btnIniciarScan.addEventListener('click', iniciarScannerVideo);

        // Verifica se o navegador suporta a API de Permissões
        if (navigator.permissions && navigator.permissions.query) {
            navigator.permissions.query({ name: 'camera' })
                .then(function(permissionStatus) {
                    
                    // Se a permissão JÁ FOI DADA anteriormente
                    if (permissionStatus.state === 'granted') {
                        // Inicia o scanner automaticamente
                        iniciarScannerVideo();
                    }
                    // Se o estado for 'prompt' (precisa perguntar) ou 'denied' (negado),
                    // não faz nada. O usuário terá que clicar no botão.
                    
                    // Lidar com permissão negada
                    if (permissionStatus.state === 'denied') {
                        statusEl.innerHTML = "Permissão da câmera negada. Habilite nas configurações.";
                    }
                })
                .catch(function(error) {
                    // Erro ao checar permissões (ex: API não suportada)
                    // Não faz nada, apenas loga o aviso.
                    console.warn("Não foi possível checar permissão da câmera:", error);
                });
        }

    } // Fim do if (btnIniciarScan...)

}); // Fim do DOMContentLoaded
