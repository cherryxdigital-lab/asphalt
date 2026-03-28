document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('equipmentImageModal');
    const modalImg = document.getElementById('equipmentImageModalImg');
    const closeBtn = document.getElementById('equipmentImageClose');
    const triggers = document.querySelectorAll('.equipment-image-trigger');

    if (!modal || !modalImg || !closeBtn || !triggers.length) return;

    let lastFocusedElement = null;

    function openModal(src, alt = '', triggerEl = null) {
        lastFocusedElement = triggerEl || document.activeElement;

        modalImg.src = src;
        modalImg.alt = alt;

        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('modal-open');

        requestAnimationFrame(() => {
            closeBtn.focus();
        });
    }

    function closeModal() {
        if (!modal.classList.contains('is-open')) return;

        if (document.activeElement && modal.contains(document.activeElement)) {
            document.activeElement.blur();
        }

        closeBtn.blur();

        modal.classList.remove('is-open');
        document.body.classList.remove('modal-open');

        setTimeout(() => {
            modal.setAttribute('aria-hidden', 'true');
            modalImg.src = '';
            modalImg.alt = '';

            if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
                lastFocusedElement.focus();
            }
        }, 220);
    }

    triggers.forEach(trigger => {
        trigger.addEventListener('click', function () {
            const src = this.dataset.image;
            const alt = this.dataset.alt || '';
            if (src) {
                openModal(src, alt, this);
            }
        });
    });

    closeBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', function (e) {
        if (e.target.hasAttribute('data-close-modal')) {
            closeModal();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('is-open')) {
            closeModal();
        }
    });
});