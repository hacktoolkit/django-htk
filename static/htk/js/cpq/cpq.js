$(function() {
    var CPQ_TOTAL = 0;

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = $.cookie('csrftoken');
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    function handlePDFButton() {
        window.open('?pdf=1');
    }

    function handlePrintButton() {
        window.print();
    }

    function formatCurrency(total) {
        var neg = false;
        if (total < 0) {
            neg = true;
            total = Math.abs(total);
        }
        return (neg ? "-$" : '$') + parseFloat(total, 10).toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, "$1,").toString();
    }

    function handleCPQFormCheckboxChanged(e) {
        var subtotal = 0;
        var approvedCheckboxes = $('.cpq-form input.approve:checkbox:checked');
        _.each(approvedCheckboxes, function(checkbox) {
            var value = parseFloat($(checkbox).val());
            subtotal += value;
        });
        CPQ_TOTAL = subtotal;
        $('.stripe-pay-button').attr('data:amount', parseInt(CPQ_TOTAL * 100));
        $('.cpq-approval-amount').html(formatCurrency(CPQ_TOTAL));
        updateApproveAndPayButtonState();
    }

    function updateApproveAndPayButtonState() {
        if ($('.cpq-approval:checkbox:checked').length > 0 && CPQ_TOTAL > 0) {
            $('.stripe-pay-button').removeClass('pure-button-disabled');
        } else {
            $('.stripe-pay-button').addClass('pure-button-disabled');
        }
    }

    function handleStripePayButton(e) {
        var target = e.target;
        e.preventDefault();
        var amount = $(target).attr('data:amount');
        var handler = StripeCheckout.configure({
            key: STRIPE_KEY,
            image: GRAVATAR_IMG,
            token: createTransactionProcessorCallback(amount)
        });
        handler.open({
            name: '',
            description: 'Rayco Energy',
            amount: amount,
            panelLabel: 'Pay {{amount}}'
        });
    }

    /**
     * createTransactionProcessorCallback
     *
     * Creates the callback function to create the charge on the server using `token`
     *
     */
    function createTransactionProcessorCallback(amount) {
        var callback = function(token) {
            var uri = CPQ_PAYMENT_URI;
            var data = {
                stripeToken : token.id,
                email : token.email,
                amount : amount
            } ;
            $.ajax(
                uri,
                {
                    method: 'POST',
                    data: data
                }
            ).done(function(data) {
                console.log('Transaction complete');
                window.location = window.location;
            }).fail(function(data) {
                console.log('Failed to charge payment card');
            }).always(function(data) {
                // nothing for now
            });
        };
        return callback;
    }

    function initEventHandlers() {
        $('.pdf-button').click(handlePDFButton);
        $('.print-button').click(handlePrintButton);
        $('.stripe-pay-button').click(handleStripePayButton);
        $('.cpq-form input:checkbox').change(handleCPQFormCheckboxChanged);
        $('.cpq-approval:checkbox').change(updateApproveAndPayButtonState);
    }

    function init() {
    }

    initEventHandlers();
    init();
});
