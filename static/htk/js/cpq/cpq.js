$(function() {
    function handlePDFButton() {
        window.open('?pdf=1');
    }

    function handlePrintButton() {
        window.print();
    }

    function initEventHandlers() {
        $('.pdf-button').click(handlePDFButton);
        $('.print-button').click(handlePrintButton);
    }

    function init() {
    }

    initEventHandlers();
    init();
});
