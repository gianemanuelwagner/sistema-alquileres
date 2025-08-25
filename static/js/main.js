// Custom JavaScript for Alquileres Pro

document.addEventListener('DOMContentLoaded', function() {
    
    // Set current date and time for last update
    const lastUpdateElement = document.getElementById('last-update');
    if (lastUpdateElement) {
        moment.locale('es');
        lastUpdateElement.textContent = moment().format('DD/MM/YYYY HH:mm');
    }
    
    // Calculate remaining days for contracts
    const diasRestantesElements = document.querySelectorAll('.dias-restantes');
    diasRestantesElements.forEach(element => {
        const fechaFin = element.getAttribute('data-fecha-fin');
        if (fechaFin) {
            const fechaFinMoment = moment(fechaFin);
            const hoy = moment();
            const diasRestantes = fechaFinMoment.diff(hoy, 'days');
            
            const badge = element.querySelector('.badge');
            if (diasRestantes > 30) {
                badge.className = 'badge bg-success';
                badge.textContent = `${diasRestantes} días`;
            } else if (diasRestantes > 7) {
                badge.className = 'badge bg-warning';
                badge.textContent = `${diasRestantes} días`;
            } else if (diasRestantes > 0) {
                badge.className = 'badge bg-danger';
                badge.textContent = `${diasRestantes} días`;
            } else {
                badge.className = 'badge bg-secondary';
                badge.textContent = 'Vencido';
            }
        }
    });
    
    // Load contracts about to expire
    const contratosPorVencerContainer = document.getElementById('contratos-por-vencer');
    if (contratosPorVencerContainer) {
        const contratosActivos = document.querySelectorAll('tbody tr');
        let contratosPorVencerHTML = '';
        
        contratosActivos.forEach(row => {
            const estado = row.querySelector('.status-badge')?.textContent.trim();
            if (estado && estado.toLowerCase().includes('activo')) {
                const fechaFinElement = row.querySelector('.dias-restantes');
                if (fechaFinElement) {
                    const fechaFin = fechaFinElement.getAttribute('data-fecha-fin');
                    const fechaFinMoment = moment(fechaFin);
                    const hoy = moment();
                    const diasRestantes = fechaFinMoment.diff(hoy, 'days');
                    
                    if (diasRestantes <= 30 && diasRestantes > 0) {
                        const id = row.querySelector('td:first-child')?.textContent.trim();
                        const direccion = row.querySelector('td:nth-child(2)')?.textContent.trim();
                        const inquilino = row.querySelector('td:nth-child(3)')?.textContent.trim();
                        
                        const alertClass = diasRestantes <= 7 ? 'danger' : 'warning';
                        
                        contratosPorVencerHTML += `
                            <div class="col-md-6 mb-3">
                                <div class="alert alert-${alertClass} d-flex align-items-center">
                                    <i class="bi bi-exclamation-triangle me-2"></i>
                                    <div>
                                        <strong>Contrato #${id}</strong><br>
                                        <small>${direccion} - ${inquilino}</small><br>
                                        <small>Vence en ${diasRestantes} días (${fechaFin})</small>
                                    </div>
                                </div>
                            </div>
                        `;
                    }
                }
            }
        });
        
        if (contratosPorVencerHTML) {
            contratosPorVencerContainer.innerHTML = contratosPorVencerHTML;
        } else {
            contratosPorVencerContainer.innerHTML = `
                <div class="col-12">
                    <div class="text-center text-muted py-3">
                        <i class="bi bi-check-circle display-4"></i>
                        <p class="mt-2">No hay contratos próximos a vencer</p>
                    </div>
                </div>
            `;
        }
    }
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar este elemento? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Price formatting
    const priceInputs = document.querySelectorAll('.price-input');
    priceInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = value.toFixed(2);
            }
        });
    });

    // Date validation for contracts
    const startDateInputs = document.querySelectorAll('.start-date');
    const endDateInputs = document.querySelectorAll('.end-date');
    
    // Set minimum date to today for start date inputs
    const today = moment().format('YYYY-MM-DD');
    startDateInputs.forEach(input => {
        input.min = today;
    });
    
    startDateInputs.forEach((startInput, index) => {
        const endInput = endDateInputs[index];
        if (endInput) {
            startInput.addEventListener('change', function() {
                endInput.min = this.value;
            });
        }
    });

    // Search functionality for tables
    const searchInputs = document.querySelectorAll('.table-search');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const table = this.closest('.card').querySelector('table');
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // Status badge updates
    const statusBadges = document.querySelectorAll('.status-badge');
    statusBadges.forEach(badge => {
        const status = badge.textContent.toLowerCase();
        badge.className = 'badge status-badge';
        
        if (status.includes('disponible') || status.includes('activo')) {
            badge.classList.add('bg-success');
        } else if (status.includes('alquilada') || status.includes('pendiente')) {
            badge.classList.add('bg-warning');
        } else if (status.includes('inactivo') || status.includes('cancelado')) {
            badge.classList.add('bg-danger');
        } else {
            badge.classList.add('bg-secondary');
        }
    });

    // Loading states for buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.form && this.form.checkValidity()) {
                this.innerHTML = '<span class="loading"></span> Procesando...';
                this.disabled = true;
            }
        });
    });

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-clipboard-text');
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Show success feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check"></i> Copiado';
                this.classList.add('btn-success');
                this.classList.remove('btn-outline-secondary');
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('btn-success');
                    this.classList.add('btn-outline-secondary');
                }, 2000);
            });
        });
    });

    // Responsive table enhancements
    const tables = document.querySelectorAll('.table-responsive');
    tables.forEach(table => {
        const wrapper = table.parentElement;
        if (wrapper && wrapper.classList.contains('card')) {
            wrapper.style.overflow = 'hidden';
        }
    });

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Phone number formatting
    const phoneInputs = document.querySelectorAll('.phone-input');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 0) {
                value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
            }
            this.value = value;
        });
    });

    // DNI formatting
    const dniInputs = document.querySelectorAll('.dni-input');
    dniInputs.forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 8) {
                value = value.substring(0, 8);
            }
            this.value = value;
        });
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Print functionality
    const printButtons = document.querySelectorAll('.btn-print');
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // Export functionality (placeholder)
    const exportButtons = document.querySelectorAll('.btn-export');
    exportButtons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Función de exportación en desarrollo');
        });
    });

    // Dark mode toggle (if implemented)
    const darkModeToggle = document.querySelector('#darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDark);
        });
    }

    // Initialize dark mode from localStorage
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }

    // Auto-save form data (basic implementation)
    const autoSaveForms = document.querySelectorAll('.auto-save');
    autoSaveForms.forEach(form => {
        const formId = form.id || 'form_' + Math.random().toString(36).substr(2, 9);
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                const formData = new FormData(form);
                const data = {};
                for (let [key, value] of formData.entries()) {
                    data[key] = value;
                }
                localStorage.setItem('form_' + formId, JSON.stringify(data));
            });
        });

        // Restore form data on page load
        const savedData = localStorage.getItem('form_' + formId);
        if (savedData) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = data[key];
                }
            });
        }
    });

    // Notification system
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(notification);
            bsAlert.close();
        }, 5000);
    }

    // Global notification function
    window.showNotification = showNotification;

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + N for new item
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            const newButton = document.querySelector('.btn-new');
            if (newButton) {
                newButton.click();
            }
        }
        
        // Ctrl/Cmd + S for save
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const submitButton = document.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.click();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });

    console.log('Alquileres Pro - JavaScript loaded successfully!');
});
