// JavaScript для лендинга по асфальтированию

document.addEventListener('DOMContentLoaded', function() {
    const sections = Array.from(document.querySelectorAll('section'));
    const anchorLinks = Array.from(document.querySelectorAll('a[href*="#"]'));
    const topScrollLinks = Array.from(document.querySelectorAll('.brand, .footer-logo'));

    // Анимация появления секций
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (!entry.isIntersecting) return;
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
                observer.unobserve(entry.target);
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        sections.forEach((section) => {
            if (section.id === 'hero') {
                return;
            }
            section.style.opacity = '0';
            section.style.transform = 'translateY(30px)';
            section.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            observer.observe(section);
        });
    }

    function scrollToHashTarget(hash) {
        if (!hash) return false;
        const targetId = hash.replace(/^#/, '');
        const targetElement = document.getElementById(targetId);
        if (!targetElement) return false;
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        return true;
    }

    // Плавная прокрутка к внутренним якорям на текущей странице
    anchorLinks.forEach((link) => {
        link.addEventListener('click', function(e) {
            const href = link.getAttribute('href') || '';
            if (!href.includes('#')) return;

            try {
                const url = new URL(href, window.location.origin);
                const isSamePage = url.pathname === window.location.pathname;
                if (!isSamePage || !url.hash) return;

                if (scrollToHashTarget(url.hash)) {
                    e.preventDefault();
                }
            } catch (err) {
                if (href.startsWith('#') && scrollToHashTarget(href)) {
                    e.preventDefault();
                }
            }
        });
    });

    topScrollLinks.forEach((link) => {
        link.addEventListener('click', function(e) {
            const href = link.getAttribute('href') || '';
            if (!href.endsWith('#top')) return;

            try {
                const url = new URL(href, window.location.origin);
                if (url.pathname !== window.location.pathname) return;
            } catch (err) {
                return;
            }

            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });

    // Fullscreen navigation (burger)
    const navToggle = document.querySelector('[data-nav-toggle]');
    const navOverlay = document.getElementById('navOverlay');
    const navClose = document.getElementById('navClose');
    const navOverlayLinks = navOverlay ? Array.from(navOverlay.querySelectorAll('a')) : [];

    function openNav() {
        document.body.classList.add('nav-open');
        if (navOverlay) {
            navOverlay.setAttribute('aria-hidden', 'false');
        }
        navToggle.setAttribute('aria-expanded', 'true');
    }

    function closeNav() {
        document.body.classList.remove('nav-open');
        if (navOverlay) {
            navOverlay.setAttribute('aria-hidden', 'true');
        }
        navToggle.setAttribute('aria-expanded', 'false');
    }

    if (navToggle && navOverlay) {
        navToggle.addEventListener('click', function() {
            const opened = document.body.classList.contains('nav-open');
            if (opened) closeNav(); else openNav();
        });
        navClose && navClose.addEventListener('click', closeNav);
        navOverlayLinks.forEach((link) => {
            link.addEventListener('click', function() {
                closeNav();
            });
        });

        // Close when clicking outside nav content
        navOverlay.addEventListener('click', function(e) {
            if (e.target === navOverlay) closeNav();
        });
    }

    let formStatusTimer = null;
    const nameField = document.getElementById('name');
    const phoneField = document.getElementById('phone');
    const messageField = document.getElementById('message');

    function normalizeName(value) {
        return String(value || '')
            .replace(/[^A-Za-zА-Яа-яІіЇїЄєҐґ'\-\s]/g, '')
            .replace(/\s{2,}/g, ' ')
            .trimStart();
    }

    function isValidName(value) {
        return /^[A-Za-zА-Яа-яІіЇїЄєҐґ'\-\s]+$/.test(value) && value.trim().length >= 2;
    }

    function extractPhoneDigits(value) {
        let digits = String(value || '').replace(/\D/g, '');
        if (digits.startsWith('380')) {
            return digits.slice(0, 12);
        }
        if (digits.startsWith('80')) {
            return (`3${digits}`).slice(0, 12);
        }
        if (digits.startsWith('0')) {
            return (`38${digits}`).slice(0, 12);
        }
        return (`380${digits}`).slice(0, 12);
    }

    function formatPhoneValue(value) {
        const digits = extractPhoneDigits(value);
        let result = '+380';

        if (digits.length > 3) result += ` (${digits.slice(3, 5)}`;
        if (digits.length >= 5) result += ')';
        if (digits.length > 5) result += ` ${digits.slice(5, 8)}`;
        if (digits.length > 8) result += `-${digits.slice(8, 10)}`;
        if (digits.length > 10) result += `-${digits.slice(10, 12)}`;

        return result;
    }

    function isValidPhone(value) {
        return extractPhoneDigits(value).length === 12;
    }

    function showFormStatus(message, kind) {
        const statusEl = document.getElementById('contact-form-status');
        if (!statusEl) return;

        statusEl.textContent = message;
        statusEl.className = `form-status form-status--${kind || 'info'}`;
        statusEl.hidden = false;

        if (formStatusTimer) {
            window.clearTimeout(formStatusTimer);
        }

        formStatusTimer = window.setTimeout(() => {
            statusEl.hidden = true;
            statusEl.textContent = '';
            statusEl.className = 'form-status';
        }, 10000);
    }

    if (nameField) {
        nameField.addEventListener('input', function() {
            const normalized = normalizeName(nameField.value);
            if (nameField.value !== normalized) {
                nameField.value = normalized;
            }
        });
    }

    if (phoneField) {
        phoneField.value = '+380';
        phoneField.addEventListener('focus', function() {
            if (!phoneField.value.trim()) {
                phoneField.value = '+380';
            }
        });
        phoneField.addEventListener('input', function() {
            phoneField.value = formatPhoneValue(phoneField.value);
        });
        phoneField.addEventListener('keydown', function(e) {
            if ((e.key === 'Backspace' || e.key === 'Delete') && (phoneField.selectionStart || 0) <= 4) {
                e.preventDefault();
                return;
            }
            if (e.key === 'Backspace' && phoneField.selectionStart === phoneField.selectionEnd) {
                const cursor = phoneField.selectionStart || 0;
                const previousChar = phoneField.value[cursor - 1] || '';
                if (/[^\d]/.test(previousChar)) {
                    e.preventDefault();
                    const chars = phoneField.value.split('');
                    let indexToRemove = cursor - 2;
                    while (indexToRemove >= 0 && /[^\d]/.test(chars[indexToRemove])) {
                        indexToRemove -= 1;
                    }
                    if (indexToRemove >= 4) {
                        chars.splice(indexToRemove, 1);
                        phoneField.value = formatPhoneValue(chars.join(''));
                        const newCursor = Math.max(indexToRemove, 4);
                        window.requestAnimationFrame(() => {
                            phoneField.setSelectionRange(newCursor, newCursor);
                        });
                    }
                }
            }
        });
    }

    // Форма заявки без перезавантаження
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const name = normalizeName(nameField?.value || '').trim();
            const phone = (phoneField?.value || '').trim();
            const message = (messageField?.value || '').trim();
            const button = contactForm.querySelector('button[type="submit"]');
            const csrfToken = contactForm.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

            if (!name || !phone || !message) {
                showFormStatus('Заповніть ім’я, телефон і опис задачі.', 'error');
                return;
            }

            if (!isValidName(name)) {
                showFormStatus('Ім’я може містити лише літери, пробіли, апостроф та дефіс.', 'error');
                if (nameField) nameField.focus();
                return;
            }

            if (!isValidPhone(phone)) {
                showFormStatus('Вкажіть коректний номер у форматі +380 (XX) XXX-XX-XX.', 'error');
                if (phoneField) phoneField.focus();
                return;
            }

            if (message.length < 10) {
                showFormStatus('Опишіть задачу щонайменше 10 символами.', 'error');
                if (messageField) messageField.focus();
                return;
            }

            if (nameField) nameField.value = name;
            if (phoneField) phoneField.value = formatPhoneValue(phone);

            if (button) {
                button.textContent = 'Відправка...';
                button.disabled = true;
            }

            try {
                const response = await fetch(contactForm.action, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken || '',
                    },
                    body: new FormData(contactForm),
                });

                const data = await response.json().catch(() => null);
                if (!response.ok || !data?.ok) {
                    showFormStatus(data?.message || 'Не вдалося відправити заявку. Спробуйте ще раз.', 'error');
                    return;
                }

                contactForm.reset();
                if (phoneField) {
                    phoneField.value = '+380';
                }
                showFormStatus(data.message || 'Заявку відправлено.', 'success');
            } catch (err) {
                showFormStatus('Помилка мережі. Спробуйте ще раз.', 'error');
            } finally {
                if (button) {
                    button.textContent = 'Надіслати заявку';
                    button.disabled = false;
                }
            }
        });
    }

    // --- Калькулятор ---
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => Array.from(document.querySelectorAll(sel));
    const calcModeBtns = $$('.mode-btn');
    const asphaltOptions = $$('.calc-asphalt-options .option');
    const equipmentOptions = $$('.calc-equipment-options .option');
    const calcArea = $('#calc-area');
    const calcBtn = $('#calc-calc');
    const calcOrder = $('#calc-order');
    const calcSummary = $('#calc-summary');
    const calcSelectedEquipment = $('#calc-selected-equipment');
    const selectedEquipmentState = new Map();
    const MAX_CALC_DIGITS = 10;

    function formatPrice(n) {
        if (!n || isNaN(n)) return '0 грн';
        return n.toLocaleString('uk-UA') + ' грн';
    }

    function readOptionData(el, key) {
        if (!el) return 0;
        const v = el.getAttribute('data-' + key);
        return v === null ? 0 : parseFloat(v || 0);
    }

    function getSelectedOption(list) {
        return list.find(el => el.classList.contains('selected')) || null;
    }

    function getUnitLabel(unit) {
        const normalized = String(unit || '').toLowerCase();
        if (normalized.includes('shift') || normalized.includes('зм') || normalized.includes('смен')) {
            return 'Кількість змін';
        }
        return 'Тривалість (годин)';
    }

    function sanitizeNumericInputValue(value) {
        const stringValue = String(value || '');
        const isNegative = stringValue.trim().startsWith('-');
        const digits = stringValue.replace(/\D/g, '').slice(0, MAX_CALC_DIGITS);

        if (isNegative) {
            return '0';
        }

        return digits;
    }

    function normalizeCalcNumber(value, minimum = 0) {
        const sanitized = sanitizeNumericInputValue(value);
        if (!sanitized) return minimum;

        const number = parseInt(sanitized, 10);
        if (Number.isNaN(number)) return minimum;

        return Math.max(minimum, number);
    }

    function bindNumericFieldGuards(input, { minimum = 0, blurMinimum = minimum, onChange } = {}) {
        if (!input || input.dataset.calcGuardBound === 'true') return;

        input.dataset.calcGuardBound = 'true';
        input.setAttribute('inputmode', 'numeric');

        input.addEventListener('keydown', function(e) {
            if (
                e.ctrlKey || e.metaKey || e.altKey ||
                ['Backspace', 'Delete', 'Tab', 'Escape', 'Enter', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)
            ) {
                return;
            }

            if (!/^\d$/.test(e.key)) {
                e.preventDefault();
                return;
            }

            const selectionStart = input.selectionStart ?? input.value.length;
            const selectionEnd = input.selectionEnd ?? input.value.length;
            const nextLength = input.value.length - (selectionEnd - selectionStart) + 1;

            if (nextLength > MAX_CALC_DIGITS) {
                e.preventDefault();
            }
        });

        input.addEventListener('input', function() {
            const sanitized = sanitizeNumericInputValue(input.value);
            if (input.value !== sanitized) {
                input.value = sanitized;
            }
            if (typeof onChange === 'function') {
                onChange('input', input);
            }
        });

        input.addEventListener('blur', function() {
            input.value = String(normalizeCalcNumber(input.value, blurMinimum));
            if (typeof onChange === 'function') {
                onChange('blur', input);
            }
        });
    }

    function renderSelectedEquipment() {
        if (!calcSelectedEquipment) return;

        const selected = equipmentOptions.filter(el => el.classList.contains('selected'));
        if (!selected.length) {
            calcSelectedEquipment.innerHTML = '<p class="muted">Оберіть одну або кілька позицій техніки, і тут з’являться години або зміни для кожної.</p>';
            return;
        }

        calcSelectedEquipment.innerHTML = selected.map((opt) => {
            const id = opt.getAttribute('data-id');
            const name = opt.getAttribute('data-name') || 'Техніка';
            const unit = opt.getAttribute('data-unit') || '';
            const minHours = readOptionData(opt, 'min-hours') || 1;
            const price = readOptionData(opt, 'price');
            const state = selectedEquipmentState.get(id) || { duration: Math.max(1, minHours), quantity: 1 };

            return `
                <div class="calc-selected-card" data-selected-id="${id}">
                    <div class="calc-selected-head">
                        <div class="calc-selected-title">${name}</div>
                        <button type="button" class="calc-selected-remove" data-remove-equipment="${id}">Прибрати</button>
                    </div>
                    <div class="calc-selected-grid">
                        <div>
                            <label for="calc-duration-${id}">${getUnitLabel(unit)}</label>
                            <input type="number" id="calc-duration-${id}" data-config-id="${id}" data-config-field="duration" min="0" step="1" value="${state.duration}" inputmode="numeric">
                        </div>
                        <div>
                            <label for="calc-quantity-${id}">Кількість одиниць</label>
                            <input type="number" id="calc-quantity-${id}" data-config-id="${id}" data-config-field="quantity" min="0" step="1" value="${state.quantity}" inputmode="numeric">
                        </div>
                    </div>
                    <div class="calc-selected-meta">Ставка: ${formatPrice(price)}${unit ? ` / ${unit}` : ''}</div>
                </div>
            `;
        }).join('');

        calcSelectedEquipment.querySelectorAll('input[type="number"]').forEach((input) => {
            const field = input.getAttribute('data-config-field');
            const configId = input.getAttribute('data-config-id');
            const option = equipmentOptions.find((item) => item.getAttribute('data-id') === configId);
            const minHours = readOptionData(option, 'min-hours') || 0;
            const blurMinimum = field === 'duration' ? Math.max(1, minHours) : 1;

            bindNumericFieldGuards(input, {
                minimum: 0,
                blurMinimum,
                onChange: () => calculate(),
            });
        });
    }

    function calculate() {
        const mode = getSelectedMode() || 'asphalt';

        let asphaltTotal = 0;
        let equipmentTotal = 0;

        if ((mode === 'asphalt' || mode === 'both') && calcArea) {
            const aOpt = getSelectedOption(asphaltOptions);
            const pricePerSq = readOptionData(aOpt, 'price');
            const area = parseFloat(calcArea.value) || 0;
            asphaltTotal = pricePerSq * area;
        }

        if (mode === 'equipment' || mode === 'both') {
            equipmentOptions.filter(el => el.classList.contains('selected')).forEach((eOpt) => {
                const id = eOpt.getAttribute('data-id');
                const state = selectedEquipmentState.get(id) || { duration: 1, quantity: 1 };
                const price = readOptionData(eOpt, 'price');
                const minHours = readOptionData(eOpt, 'min-hours') || 0;
                const duration = Math.max(parseFloat(state.duration) || 0, Math.max(1, minHours));
                const qty = Math.max(parseInt(state.quantity, 10) || 1, 1);
                equipmentTotal += price * duration * qty;
            });
        }

        const total = Math.round((asphaltTotal + equipmentTotal) * 1); // round

        // Build summary
        let html = '';
        if (asphaltTotal) {
            html += `<div class="calc-line"><strong>Асфальт:</strong> ${formatPrice(Math.round(asphaltTotal))}</div>`;
        } else if (mode === 'asphalt') {
            html += `<div class="muted">Оберіть тип асфальту та площу.</div>`;
        }

        if (equipmentTotal) {
            equipmentOptions.filter(el => el.classList.contains('selected')).forEach((eOpt) => {
                const id = eOpt.getAttribute('data-id');
                const ename = eOpt.getAttribute('data-name') || eOpt.textContent;
                const state = selectedEquipmentState.get(id) || { duration: 1, quantity: 1 };
                const minHours = readOptionData(eOpt, 'min-hours') || 0;
                const duration = Math.max(parseFloat(state.duration) || 0, Math.max(1, minHours));
                const qty = Math.max(parseInt(state.quantity, 10) || 1, 1);
                const lineTotal = readOptionData(eOpt, 'price') * duration * qty;
                html += `<div class="calc-line"><strong>Оренда (${ename}):</strong> ${formatPrice(Math.round(lineTotal))}</div>`;
            });
        } else if (mode === 'equipment') {
            html += `<div class="muted">Оберіть техніку та тривалість.</div>`;
        }

        html += `<hr /><div class="calc-line calc-total"><strong>Усього:</strong> ${formatPrice(total)}</div>`;

        calcSummary.innerHTML = html;
        return { asphaltTotal, equipmentTotal, total };
    }

    // UI show/hide based on mode
    function updateVisibility(mode) {
        const m = mode || (getSelectedMode() || 'asphalt');
        const asphaltRows = document.querySelectorAll('.calc-asphalt-row, .calc-area-row');
        const equipmentRows = document.querySelectorAll('.calc-equipment-row, .calc-selected-row');

        asphaltRows.forEach(r => r.style.display = (m === 'asphalt' || m === 'both') ? '' : 'none');
        equipmentRows.forEach(r => r.style.display = (m === 'equipment' || m === 'both') ? '' : 'none');
    }

    function clearSelected(list) { list.forEach(el => el.classList.remove('selected')); }
    function getSelectedMode() {
        const btn = calcModeBtns.find(b => b.classList.contains('selected'));
        return btn ? btn.getAttribute('data-mode') : null;
    }

    // mode button handlers
    calcModeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            clearSelected(calcModeBtns);
            btn.classList.add('selected');
            updateVisibility(btn.getAttribute('data-mode'));
            calculate();
        });
    });

    // option click handlers
    asphaltOptions.forEach(opt => {
        opt.addEventListener('click', function() { clearSelected(asphaltOptions); opt.classList.add('selected'); calculate(); });
    });

    equipmentOptions.forEach(opt => {
        opt.addEventListener('click', function() {
            const id = opt.getAttribute('data-id');
            const minHours = readOptionData(opt, 'min-hours') || 0;
            if (opt.classList.contains('selected')) {
                opt.classList.remove('selected');
                selectedEquipmentState.delete(id);
            } else {
                opt.classList.add('selected');
                selectedEquipmentState.set(id, {
                    duration: Math.max(1, minHours),
                    quantity: 1,
                });
            }
            renderSelectedEquipment();
            calculate();
        });
    });

    if (calcArea) {
        bindNumericFieldGuards(calcArea, {
            minimum: 0,
            onChange: () => calculate(),
        });
    }
    if (calcSelectedEquipment) {
        calcSelectedEquipment.addEventListener('input', function(e) {
            const target = e.target;
            const configId = target.getAttribute('data-config-id');
            const field = target.getAttribute('data-config-field');
            if (!configId || !field || !selectedEquipmentState.has(configId)) return;

            const option = equipmentOptions.find((item) => item.getAttribute('data-id') === configId);
            const minHours = readOptionData(option, 'min-hours') || 0;
            const state = selectedEquipmentState.get(configId);

            if (field === 'duration') {
                if (target.value === '') {
                    state.duration = '';
                } else {
                    state.duration = Math.max(parseFloat(target.value) || 0, 0);
                }
            }
            if (field === 'quantity') {
                if (target.value === '') {
                    state.quantity = '';
                } else {
                    state.quantity = Math.max(parseInt(target.value, 10) || 0, 0);
                }
            }

            selectedEquipmentState.set(configId, state);
            calculate();
        });

        calcSelectedEquipment.addEventListener('focusout', function(e) {
            const target = e.target;
            if (!(target instanceof HTMLInputElement)) return;

            const configId = target.getAttribute('data-config-id');
            const field = target.getAttribute('data-config-field');
            if (!configId || !field || !selectedEquipmentState.has(configId)) return;

            const option = equipmentOptions.find((item) => item.getAttribute('data-id') === configId);
            const minHours = readOptionData(option, 'min-hours') || 0;
            const state = selectedEquipmentState.get(configId);

            if (field === 'duration') {
                state.duration = Math.max(parseFloat(target.value) || 0, Math.max(1, minHours));
            }
            if (field === 'quantity') {
                state.quantity = Math.max(parseInt(target.value, 10) || 0, 1);
            }

            selectedEquipmentState.set(configId, state);
            calculate();
        });

        calcSelectedEquipment.addEventListener('click', function(e) {
            const removeId = e.target.getAttribute('data-remove-equipment');
            if (!removeId) return;
            selectedEquipmentState.delete(removeId);
            const option = equipmentOptions.find((item) => item.getAttribute('data-id') === removeId);
            if (option) option.classList.remove('selected');
            renderSelectedEquipment();
            calculate();
        });
    }

    if (calcBtn) calcBtn.addEventListener('click', function(e) { e.preventDefault(); calculate(); });

    if (calcOrder) calcOrder.addEventListener('click', function() {
        const result = calculate();
        const messageField = document.getElementById('message');
        if (messageField) {
            let lines = [];
            const aOpt = getSelectedOption(asphaltOptions);
            if (aOpt && result.asphaltTotal) {
                const aname = aOpt.getAttribute('data-name') || '';
                lines.push(`Прохання прорахувати асфальт: ${aname}. Прибл. ${calcArea.value || 0} м².`);
            }
            equipmentOptions.filter(el => el.classList.contains('selected')).forEach((eOpt) => {
                const id = eOpt.getAttribute('data-id');
                const ename = eOpt.getAttribute('data-name') || '';
                const unit = (eOpt.getAttribute('data-unit') || '').toLowerCase();
                const state = selectedEquipmentState.get(id) || { duration: 1, quantity: 1 };
                const used = Math.max(parseFloat(state.duration) || 0, Math.max(1, readOptionData(eOpt, 'min-hours')));
                const quantity = Math.max(parseInt(state.quantity, 10) || 1, 1);
                const unitLabel = (unit.includes('shift') || unit.includes('зм') || unit.includes('смен')) ? 'змін' : 'год.';
                lines.push(`Потрібна оренда: ${ename}, ${quantity} од., ${used} ${unitLabel}`);
            });
            lines.push(`Орієнтовна сума: ${formatPrice(result.total)}`);
            messageField.value = lines.join('\n');
        }
        const contacts = document.getElementById('contacts');
        if (contacts) contacts.scrollIntoView({ behavior: 'smooth', block: 'start' });
        const nameField = document.getElementById('name'); if (nameField) nameField.focus();
    });

    // initialize
    updateVisibility();
    renderSelectedEquipment();
});
